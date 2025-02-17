import json
import os
from abc import ABC, abstractmethod

class Logger(ABC):
    @abstractmethod
    def Writes_to_file(self, data: dict):
        pass


class FileWriter(Logger):
    def __init__(self, filename="log.json", encryption_key=123):
        self.filename = filename
        self.encryption_key = encryption_key

    # פונקציית XOR להצפנה
    def xor_encrypt_decrypt(self, data: str, key: int):
        return ''.join(chr(ord(char) ^ key) for char in data)

    def Writes_to_file(self, data: dict):
        # המרת הנתונים ל-JSON
        json_data = json.dumps(data, ensure_ascii=False, indent=4)

        # הצפנה של הנתונים ב-JSON
        encrypted_data = self.xor_encrypt_decrypt(json_data, self.encryption_key)

        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    existing_data = file.read()
                    if not existing_data:
                        existing_data = ''
            except (FileNotFoundError):
                existing_data = ''
        else:
            existing_data = ''

        # כתיבת הנתונים המוצפנים לקובץ
        with open(self.filename, "w", encoding="utf-8") as file:
            file.write(encrypted_data)

        return self.filename

    def Writes_to_network(self, data: dict):
        pass
