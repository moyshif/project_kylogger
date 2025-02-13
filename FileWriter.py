class Logger(ABC):
    @abstractmethod
    def Writes_to_file(self, data: dict):
        pass

    @abstractmethod
    def Upload_to_server(self, file_path: str):
        pass


class FileWriter(Logger):
    def __init__(self, filename="log.json"):
        self.filename = filename

    def Writes_to_file(self, data: dict):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = {}
        else:
            existing_data = {}

        existing_data.update(data)

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

    def Upload_to_server(self, file_path: str):
        pass
