# TelegramBotTestT

## Зависимости
- [requests](https://pypi.org/project/requests/)
- Python 3

## Установка

Можно запустить скрипт prepare.sh, который скачает и установит все необходимые файлы (тестировал на Debian).
В противном случае необходимо поставить все пакеты, указанные в зависимостях.

## Запуск
1. Скопировать токен бота в переменную TOKEN
2. Установить время проверки в переменную check_time. Формат: check_time = (\<hour\>, \<minute\>, \<second\>, 0)
3. Запустить скрипт
4. Отправить боту команду /start (после сообщения скрипта)