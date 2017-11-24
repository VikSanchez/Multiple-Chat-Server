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
def process_join_msg(conn, message):

    # Matching the JOIN message with the valid join message template otherwise returns error
    msg_components = regex.match(valid_join_msg, message, regex.M)
    if msg_components is not None:
        create_chat_room(conn, msg_components.groups()[0], msg_components.groups()[3])
    else:
        send_error_msg_to_client(error_code_1, 1, conn)
      
def process_hello_msg(conn, message, addr):

    # Matching the HELO message with the valid HELO message template otherwise returns error
    msg_components = regex.match(valid_hello_msg, message, regex.M)
    if msg_components is not None:
        send_msg_to_client("HELO " + msg_components.groups()[0] + "\nIP:" + str(host) + "\nPort:" + str(port) + "\nStudentID:" + "17304678", conn)
    else:
        send_error_msg_to_client(error_code_1, 1, conn)
def process_leave_msg(conn, message):

    # Matching the LEAVE message with the valid leave message template otherwise returns error
    msg_components = regex.match(valid_leave_msg, message, regex.M)
    if msg_components is not None:
        delete_from_chat_room(conn, msg_components.groups()[0], msg_components.groups()[1], msg_components.groups()[2])
    else:
        send_error_msg_to_client(error_code_1, 1, conn)
def process_chat_msg(conn, message):

    # Matching the LEAVE message with the valid leave message template otherwise returns error
    msg_components = regex.match(valid_chat_msg, message, regex.M)
    if msg_components is not None:
        broadcast_msg_chatroom_users(conn, msg_components.groups()[0], msg_components.groups()[1], msg_components.groups()[2], msg_components.groups()[3])
    else:
        send_error_msg_to_client(error_code_1, 1, conn)
def process_disconnect_msg(conn, message):

    # Matching the LEAVE message with the valid leave message template otherwise if false return error
    msg_components = regex.match(valid_disconnect_msg, message, regex.M)
    if msg_components is not None:
        disconnect_user_from_chatroom(conn, msg_components.groups()[2])
    else:
        send_error_msg_to_client(error_code_1, 1, conn)
 def disconnect_user_from_chatroom(conn, chat_user_name):
    chat_user_id = str(int(hashlib.md5(chat_user_name).hexdigest(), 16))
    rooms = []
    print "Receieved: DISCONNECT from " + chat_user_name
    # acquire chatrooms mutex to access global room data
    rooms_lock.acquire()
    try:
        # cache list of all chatroom objects
        rooms = chat_rooms_array.values()
    finally:
        rooms_lock.release()

    rooms = sorted(rooms, key=lambda x: x.chat_room_name)
    print(rooms)
    for r in rooms:
        r.disconnect_user_from_chat_room(chat_user_id, chat_user_name)
      
def create_chat_room(conn, chat_room_name, chat_user_name):

    # Connecting unique hashes to the chat room name and chat user name
    chat_room_id = str(int(hashlib.md5(chat_room_name).hexdigest(), 16))
    chat_user_id = str(int(hashlib.md5(chat_user_name).hexdigest(), 16))

    # Lock this portion such that no other thread can interfere
    rooms_lock.acquire()
    try:
        # Checking if chat room with ID exists otherwise create a new one
        if chat_room_id not in chat_rooms_array:
            chat_rooms_array[chat_room_id] = ChatRoom.Chatroom(chat_room_name, chat_room_id)
        room = chat_rooms_array[chat_room_id]
    finally:
        # Release the lock so that other thread can interact
        rooms_lock.release()

    print "RECEIVED FROM CLIENT-> Join request to join chat room.", chat_room_name, "from the user ", chat_user_name
    #  Send chat room details and response to the client
    send_msg_to_client(room.add_user_to_chat_room(conn, port, host, chat_user_id, chat_user_name), conn)
    #  Send message to all the users of the chat room that a new user joined
    room.send_chat_msg(chat_user_name, chat_user_name + " joined the chat room")

 
 def server_main():
    global port
    port = 8000  # Port for connection
    # Ipv4 Socket Family and TCP Sockets
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))  # Bind with port and host
    s.listen(5)

    # continuous loop to keep accepting client requests
    while True:
        # accepts a connection request
        conn, address = s.accept()

        # Initializing the client thread
        ClientThread(clients)

        # receive data and put request in queue
        clients.put((conn, address))


if __name__ == '__main__':
    server_main()
