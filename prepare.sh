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

echo "System ready"