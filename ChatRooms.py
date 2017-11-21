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
