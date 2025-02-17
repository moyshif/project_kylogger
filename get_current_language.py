import win32api

class Get_current_language:

    def get_current_language_id_raw(self):
        language_id = win32api.GetKeyboardLayoutName()
        print(language_id)
        return language_id

a = Get_current_language()
print(a.get_current_language_id_raw())