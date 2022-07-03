from config import POST_PATH
from json import load as json_load, dump as json_dump, JSONDecodeError
from sys import getsizeof as gs
from re import findall
from flask import abort


class DataBase:
    def __init__(self, path: str = POST_PATH):
        self.path = path
        self.data = []

    def _json_loader(self):
        """Загрузка json БазаДанных"""
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json_load(f)
        except FileNotFoundError:
            return abort(400)
        except JSONDecodeError:
            return abort(400)

    def class_database_loader(self):
        """Заполнение данными экземпляра класса"""
        for line in self._json_loader():
            self.data.append(line)

    def json_write(self, data_to_write):
        """Запись в json базу данных"""
        database = self._json_loader()
        database.append(data_to_write)
        with open(self.path, "w", encoding="utf-8") as f:
            json_dump(database, f, ensure_ascii=False, indent=2)

    def search_in_database(self, query: str) -> list:
        """Метод класса - поиск в базе данных по вхождению строки в комментарии"""
        output_data = []
        for line in self.data:
            if query.lower().strip() in findall(r"\w+", line["content"].lower()):
                output_data.append(line)
        return output_data

