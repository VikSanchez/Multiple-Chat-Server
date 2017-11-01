#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 16:47:37 2017

@author: vikas
"""

# chat_client.py

import sys, socket, select

def join():
	chatroom = input('Enter Chatroom name to enter')

	conn_msg = "JOIN_CHATROOM:".encode('utf-8') + chatroom.encode('utf-8') + "\n".encode('utf-8')
	conn_msg += "CLIENT IP: \n".encode('utf-8')
	conn_msg += "PORT: \n".encode('utf-8')
	conn_msg += "CLIENT_NAME:".encode('utf-8') + Cname.encode('utf-8') + "\n".encode('utf-8')

	s.send(conn_msg)
