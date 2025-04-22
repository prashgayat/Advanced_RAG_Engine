# memory_utils.py

class MemoryManager:
    """
    Simple memory manager to store and retrieve chat history per session.
    """

    def __init__(self):
        self.sessions = {}

    def get_memory(self, session_id):
        """
        Get chat history for a given session.
        """
        return self.sessions.get(session_id, [])

    def save_turn(self, session_id, user_input, assistant_response):
        """
        Save a new turn (question + answer) into session history.
        """
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        self.sessions[session_id].append((user_input, assistant_response))
