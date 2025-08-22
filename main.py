import argparse
from datetime import date, datetime

import json
import logging
import tabulate
from typing import Union

logger = logging.getLogger(__name__)


def configuration_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)d] %(module)-10s:%(lineno)3d "
               "%(levelname)7s - %(message)s"
    )


def validate_date(target_date: Union[None, str, date]):
    if target_date is None:
        return None
    try:
        if isinstance(target_date, str):
            target_date = datetime.fromisoformat(target_date).date()
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Invalid date format. Expected format - 'YYYY-MM-DD"
        )
    return target_date


class HandlerLogsFile:

    def __init__(self, paths: list, report_type: str, target_date: date = None):
        self.path = paths
        self.report_type = report_type
        self.target_date = target_date
        self.report_handlers = {
            "average": self.run_average_handling,
            "user-agent": None
        }

    def generate_report(self):
        """
        Основной метод для запуска генерации отчётов
        """
        return self.show_report(self.report_type)

    def run_average_handling(self):
        """
        Обрабатываем данные, формируем список кортежей с данными для отчета с
        типом average
        """
        log_data = self.parse_log_data(self.path)

        pre_result = dict()
        table_data = [("", "handler", "total", "avg_response_time")]

        for row in log_data:
            try:
                if row["url"] not in pre_result:
                    pre_result[row["url"]] = {
                        "total": 0, "avg_response_time": 0
                    }
                pre_result[row["url"]]["total"] += 1
                pre_result[row["url"]]["avg_response_time"] += row[
                    "response_time"
                ]
            except KeyError:
                logger.error(
                    "Row contains unexpected key - %s", row
                )

        count = 0

        for key, value in pre_result.items():
            average = 0
            if value["total"] > 0:
                average = round(value["avg_response_time"] / value["total"], 3)
            table_data.append((count, key, value["total"], average))
            count += 1

        return table_data

    def show_report(self, report_type):
        """
        Отображаем данные в зависимости от выбранного типа отчёта
        """
        report_handler = self.report_handlers.get(report_type, None)
        if report_handler is None:
            return f"Unknown type of report - {report_type}"
        data_to_show = report_handler()
        return tabulate.tabulate(tabular_data=data_to_show, headers="firstrow")

    def parse_log_data(self, paths: list):
        """
        Забираем все данные с файла, так как этот метод можно будет применять
        для других отчетов, где могут потребоваться строки отличные от average
        и в задании указано, что файл небольшой максимальный размер - 100мб.
        """
        log_data = list()
        for path in paths:
            try:
                with open(path, "r", encoding="utf-8") as file:
                    for row in file:
                        deserialized_line = json.loads(row)
                        if self.target_date:
                            try:
                                if validate_date(
                                        deserialized_line["@timestamp"]
                                ) == self.target_date:
                                    log_data.append(deserialized_line)
                            except KeyError:
                                logger.error(
                                    "Row does not contain key argument - %s",
                                    row
                                )
                            except argparse.ArgumentTypeError:
                                logger.error(
                                    "Incorrect date format found in %s", row
                                )
                        else:
                            log_data.append(deserialized_line)
            except FileNotFoundError:
                logger.error("File was not found in the path %s", path)
        return log_data


def main():
    parser = argparse.ArgumentParser(description="Handling a log File")
    parser.add_argument("--file", nargs="+", required=True, help="Path to file")
    parser.add_argument(
        "--report", type=str, required=True, help="Type of report"
    )
    parser.add_argument("--date", required=False, type=validate_date)

    args = parser.parse_args()

    report_handler = HandlerLogsFile(
        paths=args.file, report_type=args.report, target_date=args.date
    )

    print(report_handler.generate_report())


if __name__ == "__main__":
    configuration_logging()
    main()
