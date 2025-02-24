class Encryption:
    def __init__(self, key):
        self.key = key

    def xor_encrypt_decrypt(self, text):
        """ מבצע XOR על מחרוזת ומחזיר מחרוזת של תווים """
        return ''.join(chr(ord(char) ^ self.key) for char in text)

    def xor_encrypt_decrypt_dict_list(self, data):
        print(type(data))
        processed_dict = {}

        # עבור כל מפתח במילון
        for timestamp_key, dictionary_list in data.items():
            processed_list = []
            for dictionary in dictionary_list:  # עבור כל רשימה (מילון) עבור המפתח
                processed_dict_entry = {}
                for k, v in dictionary.items():  # עבור כל זוג מפתח-ערך במילון
                    if isinstance(v, str):  # אם הערך הוא מחרוזת, נבצע עליו XOR
                        encrypted_key = self.xor_encrypt_decrypt(k)  # הצפנה/פענוח של המפתח
                        encrypted_value = self.xor_encrypt_decrypt(v)  # הצפנה/פענוח של הערך
                        processed_dict_entry[encrypted_key] = encrypted_value
                    else:
                        processed_dict_entry[k] = v  # אם לא מחרוזת, פשוט מעתיקים את הערך
                processed_list.append(processed_dict_entry)  # מוסיפים את המילון המעובד לרשימה

            processed_dict[timestamp_key] = processed_list  # מוסיפים את המפתח עם הרשימה המעובדת

        return processed_dict

c = {

    "24/02/2025 12:57": [
        {
            "פלל׭%בעהףלט": "כב%ץ׬כ"
        },
        {
            "‮זאו׭%ץמץפ%-441,%(%h501=107130Ebhdli+fjh%(%Bhdli%(%Bjjbi`%Fmwjh`": "במאי%הפז׭"
        }
    ],
    "24/02/2025 12:58": [
        {
            " Bjjbi`%DL%Vqpalj%(%U|qmjk%DUL%Lkq`wdfqljkv%y%Bjjbi`%DL%Vqpalj": "אכב%קם^GDFNVUDF@Xאז"
        },
        {
            "פלל׭%בעהףלט": "םאה"
        }
    ]
}

if __name__ == "__main__":
    a = Encryption(5)
    print(a.xor_encrypt_decrypt_dict_list(c))
