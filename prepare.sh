#!/bin/bash

# Скрипт для установки необходимых пакетов. Тестировался на дебиане
# Должен работать везде, где есть apt
installed=$(apt list --installed)
if echo $installed | grep -q "python3"; then
	echo "python3 check done"
else
	apt-get update
	apt-get -y upgrade
fi

if echo $installed | grep -q "python3-pip"; then
	echo "python3-pip check done"
else
	apt-get install -y python3-pip
fi

installed=$(pip3 freeze)
if echo $installed | grep -q "requests"; then
	echo "requests check done"
else
	pip3 install requests
	echo "requests installed"
fi

echo "Done"
