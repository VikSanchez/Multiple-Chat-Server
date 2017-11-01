#!/bin/sh
echo Please provide your port number :

read var

echo Your server is running on Port Number : $var

python Py-server.py "$var"