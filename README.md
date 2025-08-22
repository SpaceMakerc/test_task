Скрипт обработки лог файлов разных типов.
Скрипт читает файлы и на основании полученной информации формирует отчёты, которые содеражт следующие колонки:
- Индекс URL
- Обработчик
- Количество обращений на обработчик
- Среднее время ответа обработчика

Скрипт поддерживает следующий функционал:
- Принимает путь к файлу, файлов может быть несколько
- Принимает название отчета
- Вывод отчёта в виде таблицы в консоль

Запуск скрипта python main.py --file files_to_handle --report types_of_report --date optional_fiel_for_filtering_data
  
Примеры запуска скрипта:

1 - Два файла, без указания даты
![two_files](https://github.com/user-attachments/assets/a940e246-2627-4b05-8232-c3427326bb4c)

2 - Один файл без указания даты
![one_file](https://github.com/user-attachments/assets/6044d18c-63ea-460f-9329-c594b49cbc14)

3 - Один файл с указанием даты
![one_file_with_date](https://github.com/user-attachments/assets/76fe86d2-84a1-4ba6-9094-001fffd8a3dd)

4 - Два файла с указанием даты
![two_files_with_date](https://github.com/user-attachments/assets/09b06173-1040-46da-ae81-098e490bd27a)

Покрытие тестами:

1 - Общий процент покрытия
<img width="1094" height="189" alt="image" src="https://github.com/user-attachments/assets/208c8cce-f0c8-4423-92b6-320d89f30146" />

2 - Все тесты
<img width="1210" height="200" alt="image" src="https://github.com/user-attachments/assets/32126eb9-1b8e-43ad-82c2-36a594a20d30" />



