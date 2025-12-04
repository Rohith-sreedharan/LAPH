import os
import datetime

class Logger:
    def __init__(self, path="logs/laph.log"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.path = path

    def log(self, message: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.path, "a") as f:
            f.write(f"[{timestamp}] {message}\n")

    def clear(self):
        with open(self.path, "w") as f:
            f.write("")
