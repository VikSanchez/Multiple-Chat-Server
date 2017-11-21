#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 16:45:17 2017

@author: vikas
"""

# chat_server.py
 
import sys, socket, select
from Queue import Queue
from threading import Thread
from threading import Lock  
import re as regex  
import ChatRoom 
import hashlib  
import os 

port = 0
host = sys.argv[0]

# All client stored in the queue
clients = Queue()

# This array will contain all the details of chat rooms
chat_rooms_array = {}

# it would create synchronizing Chat room creation and chats
rooms_lock = Lock()

# All the valid input messages to the server from the client
valid_join_msg = r"JOIN_CHATROOM: ?(.*)(?:\s|\\n)CLIENT_IP: ?(.*)(?:\s|\\n)PORT: ?(.*)(?:\s|\\n)CLIENT_NAME: ?(.*)"
valid_hello_msg = r"HELO ?(.*)\s"
valid_leave_msg = r"LEAVE_CHATROOM: ?(.*)(?:\s|\\n)JOIN_ID: ?(.*)(?:\s|\\n)CLIENT_NAME: ?(.*)"
valid_chat_msg = r"CHAT: ?(.*)(?:\s|\\n)JOIN_ID: ?(.*)(?:\s|\\n)CLIENT_NAME: ?(.*)(?:\s|\\n)MESSAGE: ?(.*)"
valid_disconnect_msg = r"DISCONNECT: ?(.*)(?:\s|\\n)PORT: ?(.*)(?:\s|\\n)CLIENT_NAME: ?(.*)"

error_code_1 = "Invalid Message Format... Please write the correct format"
error_code_2 = "No Chat room exists with the Chat Room Ref-"

def process_message(conn, addr):
 while conn:
  message = ""
            # Looping through messages and storing in the string
            while "\n\n" not in message:
                message_content = conn.recv(1024)
                message += message_content.decode()
                if len(message_content) < 1024:
                    break
            # Check if message string have some data or not
            if len(message) > 0:
                print "MESSAGE FROM CLIENT->", message

                #  Check the type of message and process them accordingly
                if message == "KILL_SERVICE\n":
                    os._exit(0)

                if message.startswith("HELO"):
                    process_hello_msg(conn, message, addr)

                if message.startswith("JOIN_CHATROOM"):
                    process_join_msg(conn, message)

                if message.startswith("LEAVE_CHATROOM"):
                    process_leave_msg(conn, message)

                if message.startswith("CHAT"):
                    process_chat_msg(conn, message)

                if message.startswith("DISCONNECT"):
                    process_disconnect_msg(conn, message)
                    conn.shutdown(1)
                    conn.close()

