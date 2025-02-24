from abc import ABC, abstractmethod
import platform
import subprocess
import ctypes
from ctypes import wintypes


class ActiveWindowDetectorBase(ABC):

    @abstractmethod
    def get_active_window_name(self) -> str:
        pass


class WindowsActiveWindowDetector(ActiveWindowDetectorBase):
    """
    מחלקה לזיהוי החלון הפעיל במערכת Windows.
    """

    def __init__(self):
        self.user32 = ctypes.WinDLL('user32', use_last_error=True)
        self._define_windows_api_functions()

    def _define_windows_api_functions(self):
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

    def get_active_window_name(self) -> str:
        """קבלת שם החלון הפעיל ב-Windows"""
        hwnd = self.user32.GetForegroundWindow()
        length = 256
        buffer = ctypes.create_unicode_buffer(length)
        self.user32.GetWindowTextW(hwnd, buffer, length)
        return buffer.value


class LinuxActiveWindowDetector(ActiveWindowDetectorBase):
    """
    מחלקה לזיהוי החלון הפעיל במערכת Linux.
    """

    def get_active_window_name(self) -> str:
        """קבלת שם החלון הפעיל ב-Linux באמצעות הפקודה xdotool"""
        try:
            output = subprocess.check_output(["xdotool", "getwindowfocus", "getwindowname"])
            return output.decode().strip()
        except Exception:
            return "Unknown Window"


class MacOSActiveWindowDetector(ActiveWindowDetectorBase):
    """
    מחלקה לזיהוי החלון הפעיל במערכת macOS.
    """

    # from AppKit import NSWorkspace  # רק עבור macOS
    def get_active_window_name(self) -> str:
        """פונקציה שמחזירה את שם החלון הפעיל ב-macOS באמצעות NSWorkspace"""
        return NSWorkspace.sharedWorkspace().frontmostApplication().localizedName()


class ActiveWindowDetector:
    """
    מחלקה פקטורי שמחזירה את גלאי החלון הפעיל המתאים למערכת ההפעלה הנוכחית.
    """

    def __new__(cls):
        system = platform.system()
        if system == "Windows":
            return WindowsActiveWindowDetector()
        elif system == "Linux":
            return LinuxActiveWindowDetector()
        elif system == "Darwin":
            return MacOSActiveWindowDetector()
        else:
            return UnknownActiveWindowDetector()


class UnknownActiveWindowDetector(ActiveWindowDetectorBase):
    """
    מחלקה לטיפול במערכות הפעלה לא נתמכות.
    """

    def get_active_window_name(self) -> str:
        return "Unsupported OS"
