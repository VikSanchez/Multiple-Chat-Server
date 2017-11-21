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
