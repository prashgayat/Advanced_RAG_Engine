# memory_utils.py

class MemoryManager:
    """
    Memory manager to store and retrieve chat history.
    """

    def __init__(self):
        self.history = []

    def add_user_message(self, message):
        """
        Add a message from the user to history.
        """
        self.history.append(("user", message))

    def add_assistant_message(self, message):
        """
        Add a message from the assistant to history.
        """
        self.history.append(("assistant", message))

    def get_history(self):
        """
        Retrieve the full conversation history.
        """
        return self.history

    def clear(self):
        """
        Clear the entire conversation history.
        """
        self.history = []
