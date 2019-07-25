#!bin/bash

# Скрипт для установки необходимых пакетов. Тестировался на дебиане
# Должен работать везде, где есть apt
installed=$(apt list --installed)
if echo $installed | grep -q "python3"; then
	echo "python3 installed"
else
	apt-get update
	apt-get -y upgrade
fi

if echo $installed | grep -q "python3-pip"; then
	echo "python3-pip installed"
else
	apt-get install -y python3-pip
fi

installed=$(pip3 freeze)
if echo $installed | grep -q "pyTelegramBotAPI"; then
	echo "telebot installed"
else
	pip3 install pytelegrambotapi
fi
echo "System ready"