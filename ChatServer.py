#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 16:45:17 2017

@author: vikas
"""

# chat_server.py
 
import sys, socket, select

def check_msg(msg):
	print('Checking for your connection')
	if (msg.find('JOIN_CHATROOM'.encode('utf-8'))+1):
		return(1)	
	elif (msg.find('LEAVE_CHATROOM'.encode('utf-8'))+1):
		return(2)
	elif (msg.find('DISCONNECT'.encode('utf-8'))+1):
		return(3)
	elif (msg.find('CHAT:'.encode('utf-8'))+1):
		return(4)	
	else:
		return(5)
