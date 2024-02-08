"""
Позволяет зайти по логину-паролю или создать нового пользователя (а так же выйти из аккаунта)
Позволяет выбрать календарь, узнать ближайшие события, события из промежутка времени а так же
Создать событие или удалить событие
После создания события можно добавить туда пользователей
Если нас добавили в событие или удалили мы получаем уведомление.

в main можно использовать ТОЛЬКО interface
"""
import unittest
from datetime import datetime, timedelta
from Event import Event  # Импортируем класс Event из модуля Event
from User import User, hash_password  # Импортируем класс User из модуля User
from Calendar import Calendar  # Импортируем класс Calendar из модуля Calendargitadd In


# noinspection PyArgumentList
class Interface:
    def __init__(self):
        self.users = {}
        self.current_user = None
        self.logged_in = False

    # Метод для создания нового пользователя
    def create_user(self, login):
        if login not in self.users:
            new_user = User()
            self.users[login] = new_user
            print(f"Пользователь '{login}' создан.")
        else:
            print('Пользователь с таким логином уже существует')

    # Метод для входа пользователя в систему
    def login(self, login):
        if login in self.users and self.users[login].password == hash_password():
            self.current_user = self.users[login]
            self.logged_in = True
            print(f"Выполнен вход {login}.")
        else:
            print("Неверный логин или пароль.")

    def logout(self):
        if self.logged_in:
            print(f"Выполнен выход из учетной записи {self.current_user.login}.")
            self.current_user = None
            self.logged_in = False
        else:
            print('пользователи отсутвуют ')

    def choose_calendar(self):
        if self.logged_in:
            print(f"Выбран календарь для пользователя {self.current_user.login}.")
        else:
            print(f'осуществите вход ')

    def view_upcoming_events(self):
        if self.logged_in:
            print('события:')
        else:
            print(f'выполните вход')

    def view_interval_events(self):
        if self.logged_in:
            print('События в интервале:')
        else:
            print(f'Пожалуйста, выполните вход')

    # Метод для создания нового события
    def create_event(self, name, description, start_time, is_recurring=False):
        if self.logged_in:
            new_event = Event(name, description, self.current_user, start_time, is_recurring)
            self.current_user.calendar.add_event(new_event)
            print(f'Событие {new_event.name} создано')
        else:
            print(f' выполните вход')

    def delete_event(self, event):
        if self.logged_in:
            self.current_user.calendar.remove_event(event)
            print(f'Событие {event.name} удалено ')
        else:
            print(f'выполните вход')

    def add_participant(self, event, participant):
        if self.logged_in:
            event.add_participant(participant)
            print(f"Пользователь '{participant}' добавлен к событию '{event.name}'")
        else:
            print(f'Пожалуйста, выполните вход')

    # Метод для удаления участника из события
    def delete_participant(self, event, participant):
        if self.logged_in:
            event.remove_participant(participant)
            print(f"Пользователь '{participant}' удален из события '{event.name}'")
        else:
            print(f'Пожалуйста, выполните вход')


# noinspection PyArgumentList
class TestInterface(unittest.TestCase):
    def setUp(self):
        self.interface = Interface()
        self.user1 = User()
        self.user2 = User()
        self.calendar = Calendar("TestCalendar")
        self.event = Event("TestEvent", "EventDescription", self.user1, [self.user2], datetime.now())
        self.interface.users = {"user1": self.user1, "user2": self.user2}
        self.interface.current_user = self.user1
        self.interface.logged_in = True
        self.user1.calendar = self.calendar
        self.user1.calendar.add_event(self.event)

    def test_create_user(self):
        self.interface.create_user("newuser")
        self.assertIn("newuser", self.interface.users)

    def test_login(self):
        self.interface.login("user1")
        self.assertTrue(self.interface.logged_in)
        self.assertEqual(self.interface.current_user, self.user1)

    def test_logout(self):
        self.interface.logout()
        self.assertFalse(self.interface.logged_in)
        self.assertIsNone(self.interface.current_user)

    def test_choose_calendar(self):
        self.interface.choose_calendar()

    def test_view_upcoming_events(self):
        self.interface.view_upcoming_events()

    def test_view_interval_events(self):
        start_time = datetime.now()
        start_time + timedelta(days=7)
        self.interface.view_interval_events()

    def test_create_event(self):
        self.interface.create_event("NewEvent", "NewEventDescription", datetime.now())

    def test_delete_event(self):
        self.interface.delete_event(self.event)

    def test_add_participant(self):
        event = Event("AnotherEvent", "EventDescription", self.user1, [], datetime.now())
        self.interface.add_participant(event, "user3")

    def test_delete_participant(self):
        self.interface.delete_participant(self.event, "user2")


if __name__ == "__main__":
    unittest.main()
