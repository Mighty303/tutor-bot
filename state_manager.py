# state_manager.py
import json
import threading


class StateManager:
    def __init__(self, path='state.json'):
        self.path = path
        self.lock = threading.Lock()
        try:
            with open(self.path, 'r') as f:
                self.data = json.load(f)
        except Exception:
            self.data = {}


    def save(self):
        with self.lock:
            with open(self.path, 'w') as f:
                json.dump(self.data, f, indent=2)


    def get_state(self, user_id):
        return self.data.get(user_id, {})


    def set_state(self, user_id, state):
        self.data[user_id] = state
        self.save()