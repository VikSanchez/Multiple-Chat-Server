#!/bin/sh
echo Please provide your port number :

read var

python ChatServer.py "$var"

echo Your server is running on Port Number : $var

