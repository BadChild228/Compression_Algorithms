import random
import string

class DataLoader:
    """Класс для загрузки тестовых данных"""
    def load_file(self, file_path, file_type="text"):
        """Загружает данные из файла"""
        if file_type == "text":
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif file_type == "binary":
            with open(file_path, 'rb') as f:
                return f.read()
        else:
            raise ValueError(f"Неподдерживаемый тип файла: {file_type}")

