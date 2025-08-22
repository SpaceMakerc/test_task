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
<img width="1105" height="190" alt="image" src="https://github.com/user-attachments/assets/9f74d933-5b25-4bf4-9670-77f03f29a841" />

2 - Один файл без указания даты
<img width="927" height="180" alt="image" src="https://github.com/user-attachments/assets/d1220fec-1243-40b8-b7e0-a1babbcaae7d" />

3 - Один файл с указанием даты
<img width="1057" height="186" alt="image" src="https://github.com/user-attachments/assets/f4449b89-7454-4a57-b41a-607b19a377e1" />

4 - Два файла с указанием даты
<img width="1124" height="189" alt="image" src="https://github.com/user-attachments/assets/022adb35-aae2-47a7-bc5b-2cbb6fc6d5d1" />

Покрытие тестами:

1 - Общий процент покрытия
<img width="1094" height="189" alt="image" src="https://github.com/user-attachments/assets/208c8cce-f0c8-4423-92b6-320d89f30146" />

2 - Все тесты
<img width="1210" height="200" alt="image" src="https://github.com/user-attachments/assets/32126eb9-1b8e-43ad-82c2-36a594a20d30" />

3 - Пример с запуском несуществующих файлов
<img width="854" height="127" alt="image" src="https://github.com/user-attachments/assets/58f6d640-dac8-402e-8bd9-b2619a4e1ef5" />

