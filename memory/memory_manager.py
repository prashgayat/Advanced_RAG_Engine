# memory/memory_manager.py

class MemoryManager:
    def __init__(self):
        self.history = []

    def add_user_message(self, message):
        self.history.append(("user", message))

    def add_assistant_message(self, message):
        self.history.append(("assistant", message))

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []
