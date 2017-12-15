from threading import Lock


class Chatroom:
    """
    This class has all the attributes and functions related to chat room
    """

    def __init__(self, chat_room_name, chat_room_id):
        """Constructor to initialize the chat room object

            Args:
                chat_room_name: the name of the chat room
                chat_room_id: the id uniquely associated to particular chat room

        """

        self.chat_room_name = chat_room_name
        self.chat_room_id = chat_room_id
        self.chat_room_users = {}
        self.chat_room_lock = Lock()
        
    def add_user_to_chat_room(self, conn, port, host, chat_user_id, chat_user_name):
        """this function adds user to a chat room

            Args:
                conn: the connection parameter acting as a link b/w client and server
                port: the port of the connection
                host: host ip of the connection
                chat_user_id: id associated to a particular user
                chat_user_name: name associated with each user

        """

        # Lock the flow to enable sync between threads
        self.chat_room_lock.acquire()
        try:
            # Adding details of the user w.r.t user id
            self.chat_room_users[chat_user_id] = (chat_user_name, conn)
            print len(self.chat_room_users), self.chat_room_users
        finally:
            # Releasing the lock
            self.chat_room_lock.release()

        #  Returning the response after addition is complete
        return "JOINED_CHATROOM: " + self.chat_room_name + "\nSERVER_IP: " + str(host) + "\nPORT: " + str(
            port) + "\nROOM_REF: " + str(self.chat_room_id) + "\nJOIN_ID: " + str(chat_user_id)
    
    def send_chat_msg(self, source_user, msg):

        #  Array that contains the connection details of all the users in chat room
        user_conns = []
        # Lock the flow to enable sync between threads
        self.chat_room_lock.acquire()
        try:
            user_conns = self.chat_room_users.values()
        finally:
            self.chat_room_lock.release()
        print user_conns
        # Loop through all the user connections and send them the message
        for dest_user, dest_conn in user_conns:
            self.send_msg_to_client("CHAT:" + str(self.chat_room_id) + "\nCLIENT_NAME:" + str(source_user) + "\nMESSAGE:" + msg + "\n",
                dest_conn)
    def remove_user_from_chat_room(self, chat_user_id, chat_user_name, conn):

        # Lock the flow to enable sync between threads
        self.chat_room_lock.acquire()
        try:
            # remove the UserID from the list of users in the chat room if exits
            if chat_user_id in self.chat_room_users:
                if self.chat_room_users[chat_user_id][0] == chat_user_name:
                    del self.chat_room_users[chat_user_id]
                else:
                    #  If user does not exist then broadcast error message
                    self.send_error_msg_to_client("the username " + chat_user_name + " does not exists", 3, conn)
                    return
        finally:
            self.chat_room_lock.release()
            
    def disconnect_user_from_chat_room(self, chat_user_id, chat_user_name):
        # acquire clients mutex to check if user in room
        self.chat_room_lock.acquire()
        try:
            # check if client is member of room
            if chat_user_id not in self.chat_room_users:
                return
        finally:
            self.chat_room_lock.release()
        # send disconnect message to all members in chatroom
        self.send_chat_msg(chat_user_name, chat_user_name + " has left this chatroom.")
        # acquire clients mutex to remove user from room
        self.chat_room_lock.acquire()
        try:
            # delete from clients array
            del self.chat_room_users[chat_user_id]
        finally:
            self.chat_room_lock.release()
    def send_error_msg_to_client(self, err_desc, err_code, conn):
        
        print "SENDING ERROR-> Error Code:", str(err_code), "with description", err_desc
        message = "ERROR_CODE: " + str(err_code) + "\nERROR_DESCRIPTION: " + err_desc
        self.send_msg_to_client(message, conn)
    def send_msg_to_client(self, message, conn):
        
        print "SENDING MESSAGE TO CLIENT->\n", message
        if conn:
            conn.sendall((message + "\n").encode())
