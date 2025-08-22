import pytest
from unittest.mock import mock_open, patch, Mock

import json
from contextlib import nullcontext as does_not_raise
from datetime import datetime
import argparse

from main import HandlerLogsFile, validate_date


@pytest.fixture
def custom_logs():
    custom_logs = [
        {
            "@timestamp": "2025-08-20T13:57:32+00:00",
            "url": "/api/context/...", "response_time": 0.02
        },
        {
            "@timestamp": "2025-08-23T13:57:32+00:00",
            "url": "/api/context/...", "response_time": 0.02
        },
        {
            "@timestamp": "2025-08-21T13:57:32+00:00",
            "url": "/api/homeworks/...", "response_time": 0.03
        },
        {
            "@timestamp": "2025-08-21T13:57:32+00:00",
            "url": "/api/specializations/...", "response_time": 0.03
        },
        {
            "@timestamp": "2025-08-20T13:57:32+00:00",
            "url": "/api/specializations/...", "response_time": 0.03
        },
        {
            "@timestamp": "32+00:00",
            "url": "/api/specializations/...", "response_time": 0.03
        }
    ]
    return custom_logs


@pytest.fixture
def create_handler():
    path = ["test1.logs"]
    report_type = "test_type"
    target_date = datetime.fromisoformat("2025-08-21").date()

    handler = HandlerLogsFile(
        paths=path,
        report_type=report_type,
        target_date=target_date
    )
    return handler


@pytest.mark.parametrize(
    "custom_date, expectation",
    [
        ("2025-12-12", does_not_raise()),
        ("2025", pytest.raises(argparse.ArgumentTypeError)),
        ("22-12-2025", pytest.raises(argparse.ArgumentTypeError)),
        (None, does_not_raise())
    ]
)
def test_validation_date(custom_date, expectation):
    if custom_date is None:
        assert validate_date(custom_date) is None
    else:
        with expectation:
            assert validate_date(custom_date) == datetime.fromisoformat(
                custom_date
            ).date()


def test_parse_log_data(custom_logs, create_handler):
    handler = create_handler
    json_logs = "\n".join([json.dumps(log) for log in custom_logs])
    incorrect_data = [
        {
            "incorrect_test": "test_info",
            "timestamp": "2025-06-22T13:57:32+00:00"
        },
        {
            "incorrect_test2": "test_info",
            "@timestamp": "2025-08-21T13:57:32+00:00"
        }
    ]
    incorrect_logs = "\n".join([json.dumps(log) for log in incorrect_data])

    mock = mock_open(read_data=json_logs)

    """
    Один файл и условие по дате
    Логи соотвествуют указанной дате. Лог с некорректной датой не остановил 
    выполнение скрипта
    """
    with patch("builtins.open", mock):
        result = handler.parse_log_data(handler.path)
        assert len(result) == 2
        assert all(
            validate_date(row["@timestamp"]) == handler.target_date
            for row in result
        )

    """
    Файлы без указания даты
    Один файл
    """
    with patch.object(handler, "target_date", None):
        with patch("builtins.open", mock):
            result = handler.parse_log_data(handler.path)
            assert len(result) == 6

        # Два файла
        with patch.object(handler, "path", handler.path + ["test2.log"]):
            with patch("builtins.open", mock):
                result = handler.parse_log_data(handler.path)
                assert len(result) == 12

        # Файл, которого нет в системе
        result = handler.parse_log_data(handler.path)
        assert len(result) == 0

    mock_incorrect_data = mock_open(read_data=incorrect_logs)
    # Файл со строкой, где есть отсутствует необходимый атрибут должен
    # быть пропущен
    with patch("builtins.open", mock_incorrect_data):
        print(incorrect_logs)
        result = handler.parse_log_data(handler.path)
        print(result)
        assert len(result) == 1  # Только валидный лог прошёл


def test_show_report(create_handler, capsys):
    handler = create_handler
    table_data = [
        ("", "handler", "total", "avg_response_time"),
        (0, "/api/context/...", 2, 0.21),
        (1, "/api/homeworks/...", 1, 0.22),
        (2, "/api/specializations/...", 2, 0.23)
    ]

    # Проверяем неизвестный тип отчёта
    with pytest.raises(ValueError):
        result = handler.show_report(handler.report_type)
        assert result is None

    # Результат корректного отчета с типом average и его заголовками
    with patch.object(handler, "report_type", "average"):
        # Результат пустого отчёта
        print(handler.show_report(handler.report_type))
        out, err = capsys.readouterr()
        assert err == ""
        assert len(out) != 0
        assert "/api/context/..." not in out
        assert "handler" in out

        mock_report_handlers = Mock()
        mock_report_handlers.return_value = table_data

        # Результат отчёта с данными
        with patch.object(handler, "report_handlers", {
            "average": mock_report_handlers
        }):
            print(handler.show_report(handler.report_type))
            full_out, full_err = capsys.readouterr()
            assert full_err == ""
            assert "handler" in full_out
            assert "/api/context/..." in full_out
            assert "0.23" in full_out


def test_run_average_handling(create_handler, custom_logs):
    handler = create_handler

    """
    Успешно сформирован список с данными для отчёта
    с проверкой одной некорректной строки
    """
    with patch(
            "main.HandlerLogsFile.parse_log_data"
    ) as mock_parse_log_data:
        mock_parse_log_data.return_value = custom_logs + [{"test_incorrect": 1}]

        result = handler.run_average_handling()
        assert len(result) == 4  # Три endpoints и заголовки без невалидной
        assert result[0][3] == "avg_response_time"
        assert result[1][1] == "/api/context/..."
        assert result[2][1] == "/api/homeworks/..."

    # Пустые данные для формирования списка
    with patch(
            "main.HandlerLogsFile.parse_log_data"
    ) as mock_parse_log_data:
        mock_parse_log_data.return_value = []
        result = handler.run_average_handling()
        assert len(result) == 1  # Только заголовки
        assert result[0][2] == "total"
