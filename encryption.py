class Encryption:
    def __init__(self, key):
        self.key = key

    def xor_encrypt_decrypt(self, text):
        """ מבצע XOR על מחרוזת """
        return ''.join(chr(ord(char) ^ self.key) for char in text)

    def xor_encrypt_decrypt_dict_list(self, data):

        # שליפת המפתח הראשון (השעה)
        timestamp_key = next(iter(data))

        processed_list = []
        for dictionary in data[timestamp_key]:  # לוקח את הרשימה שבפנים
            processed_dict = {}
            for k, v in dictionary.items():
                if isinstance(v, str):
                    key_dic = self.xor_encrypt_decrypt(k)  # הצפנת / פיענוח מקור ההקשה
                    processed_dict[key_dic] = self.xor_encrypt_decrypt(v)  # הצפנה/פענוח ההקשות
                else:
                    processed_dict[k] = v
            processed_list.append(processed_dict)

        return {timestamp_key: processed_list}

