"""
Сущность, отвечающая за храние и предоставление данных
Оно хранит пользователей, календари и события.
Хранение в том числе означает сохранение между сессиями в csv файлах
(пароли пользователей хранятся как hash)

Должен быть статическим или Синглтоном

*) Нужно хранить для каждого пользователя все события которые с нима произошли но ещё не были обработаны.
"""
import csv
import hashlib
import json
import tempfile
import unittest


class DataStorage:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataStorage, cls).__new__(cls)
            cls._instance.users = {}
            cls._instance.calendars = {}
            cls._instance.events = {}
        return cls._instance

    def add_user(self, user_id, user_data):
        # добавление нового пользователя
        if "password" in user_data:
            user_data["password"] = self.hash_password(user_data["password"])
        user_data["unprocessed_events"] = []
        self.users[user_id] = user_data

    def get_user(self, user_id):
        # Получение информации о пользователе
        return self.users.get(user_id)

    def add_calendar(self, calendar_id, calendar_data):
        # Добавление календаря
        self.calendars[calendar_id] = calendar_data

    def get_calendar(self, calendar_id):
        # Получение информации о календаре
        return self.calendars.get(calendar_id)

    def add_event(self, event_id, event_data):
        # Добавление события
        self.events[event_id] = event_data

    def get_event(self, event_id):
        # Получение информации о событии
        return self.events.get(event_id)

    def save_data_to_csv(self, filename="storage.csv"):
        # Сохранение данных в  файл
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["user_id", "user_data"])
            for user_id, user_data in self.users.items():
                writer.writerow([user_id, json.dumps(user_data)])

    def load_data_from_csv(self, filename="storage.csv"):
        # Загрузка данных из файла
        try:
            with open(filename, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    user_id = row["user_id"]
                    user_data = json.loads(row["user_data"])

                    if "password_hashed" in user_data:
                        user_data["password"] = user_data["password_hashed"]
                        del user_data["password_hashed"]

                    self.users[user_id] = user_data
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")

    @staticmethod
    def hash_password(password):
        # Хэширование пароля
        if len(password) == 64:
            return password
        else:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            return hashed_password

    def add_event_for_user(self, user_id, event_id):
        # Добавление события для пользователя
        if user_id in self.users:
            self.users[user_id]["unprocessed_events"].append(event_id)

    def get_unprocessed_events_for_user(self, user_id):
        # Получение непрошедших событий для пользователя
        return self.users.get(user_id, {}).get("unprocessed_events", [])


class TestDataStorage(unittest.TestCase):
    def setUp(self):
        self.data_storage = DataStorage()

    def tearDown(self):
        self.data_storage.users = {}
        self.data_storage.calendars = {}
        self.data_storage.events = {}

    def test_save_and_load_data_to_csv(self):
        user_data = {"name": "Bob", "password": "strong_password", "unprocessed_events": []}
        self.data_storage.add_user("Bob", user_data)

        filename = tempfile.mktemp()
        self.data_storage.save_data_to_csv(filename)

        # Сброс данных перед загрузкой
        self.data_storage.users = {}
        self.data_storage.calendars = {}
        self.data_storage.events = {}

        self.data_storage.load_data_from_csv(filename)

        loaded_user_data = self.data_storage.get_user("Bob")

        expected_hashed_password = hashlib.sha256("strong_password".encode()).hexdigest()

        expected_loaded_user_data = {"name": "Bob", "password": expected_hashed_password, "unprocessed_events": []}

        self.assertEqual(loaded_user_data, expected_loaded_user_data)


if __name__ == '__main__':
    unittest.main()
