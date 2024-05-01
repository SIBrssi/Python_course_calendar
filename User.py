"""
Пользователь - имеет логин и пароль, а так же календарь.
у пользователя есть итендифекатор начинающийся с @
"""
import hashlib
import unittest
from Calendar import Calendar


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class User:
    def __init__(self, login: object, password: object) -> object:
        self.login = login
        self.password = hash_password(password)
        self.calendar = Calendar(self)  # Создание календаря
        self.identifier = '@' + str(id(self))  # Генерация уникального идентификатора


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User('test_user', 'password123')

    def test_user_attributes(self):
        # Проверяем основные атрибуты
        self.assertEqual(self.user.login, 'test_user')
        self.assertNotEqual(self.user.password, 'password123')  # должен быть хэш
        self.assertIsInstance(self.user.calendar, Calendar)  # Пользователь должен иметь свой календарь
        self.assertTrue(self.user.identifier.startswith('@'))  # Идентификатор должен начинаться с "@"

    def test_password_hashing(self):
        hashed_password = hash_password("password123")
        self.assertNotEqual(hashed_password, 'password123')


if __name__ == "__main__":
    unittest.main()
