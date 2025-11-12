from collections import UserDict
from datetime import datetime, timedelta
from functools import wraps
import pickle


class Field:
    """Базовий клас для всіх полів."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту."""

    def __init__(self, value):
        if not value:
            raise ValueError("Invalid name.")
        super().__init__(value)


class Phone(Field):
    """Клас для зберігання номера телефону з валідацією (10 цифр)."""

    def __init__(self, value):
        if not self._validate(value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

    @staticmethod
    def _validate(value: str) -> bool:
        return value.isdigit() and len(value) == 10

    @property
    def phone_number(self) -> str:
        return self.value

    def update_number(self, new_number: str) -> None:
        """Оновлює номер телефону з валідацією."""
        if not self._validate(new_number):
            raise ValueError("Phone number must contain exactly 10 digits.")
        self.value = new_number


class Birthday(Field):
    """Клас для зберігання дати народження (формат DD.MM.YYYY)."""

    def __init__(self, value: str):
        try:
            # Перетворити рядок на datetime та зберегти у value
            dt = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(dt.date())
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    @property
    def date_str(self) -> str:
        """Повертає дату у вихідному форматі."""
        return self.value.strftime("%d.%m.%Y")


class Record:
    """Клас для зберігання інформації про контакт."""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    def add_phone(self, phone_number: str) -> None:
        """Додає номер телефону до запису."""
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        """Видаляє номер телефону з запису."""
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)

    def edit_phone(self, old_number: str, new_number: str) -> bool:
        """Редагує номер телефону в записі."""
        phone = self.find_phone(old_number)
        if phone:
            phone.update_number(new_number)
            return True
        return False

    def find_phone(self, phone_number: str) -> Phone | None:
        """Знаходить номер телефону в записі."""
        for ph in self.phones:
            if ph.phone_number == phone_number:
                return ph
        return None

    def add_birthday(self, birthday_str: str) -> None:
        """Додає день народження до контакту."""
        if self.birthday is not None:
            raise ValueError("Birthday already set.")
        self.birthday = Birthday(birthday_str)
    def add_email(self, email_str: str) -> None:
        """Додає email до контакту після перевірки."""
        if self.email is not None:
            raise ValueError("Email already set. Use edit_email() to change it.")
        try:
            self.email = Email(email_str)
        except ValueError as e:
            print(f"⚠️ {e}")

    def edit_email(self, new_email: str) -> None:
        """Редагує існуючий email."""
        if self.email is None:
            print("⚠️ Email not set yet. Use add_email() to add one.")
            return
        try:
            self.email.update_email(new_email)
        except ValueError as e:
            print(f"⚠️ {e}")

    def __str__(self) -> str:
        phones_str = "; ".join(p.phone_number for p in self.phones) or "No phones"
        bday = self.birthday.date_str if self.birthday else "N/A"
        email_str = self.email.value if self.email else "N/A" #нове поле для email
        return (
            f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {bday}"
        )

import re
class Email:
    """Клас для зберігання та валідації email."""
    def __init__(self, email: str):
        if not self.validate_email(email):
            raise ValueError(f"Invalid email format: {email}")
        self.value = email

    @staticmethod
    def validate_email(email: str) -> bool:
        """Перевіряє формат email за допомогою регулярного виразу."""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        return re.match(pattern, email) is not None

    def update_email(self, new_email: str) -> None:
        """Оновлює email після перевірки."""
        if not self.validate_email(new_email):
            raise ValueError(f"Invalid email format: {new_email}")
        self.value = new_email


class AddressBook(UserDict):
    """Клас для зберігання та управління колекцією записів."""

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        """Знаходить запис за ім'ям."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Видаляє запис за ім'ям."""
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self) -> list[str]:
        """Повертає список вітальних повідомлень на наступний тиждень."""
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        greetings = []
        for rec in self.data.values():
            if rec.birthday:
                # оновити рік на поточний
                bday_this_year = rec.birthday.value.replace(year=today.year)
                # якщо вже пройшов у цьому році – брати наступний рік
                if bday_this_year < today:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)
                if today <= bday_this_year <= next_week:
                    # якщо день народження припадає на вихідні – переносимо на наступний понеділок
                    congr_date = bday_this_year
                    if congr_date.weekday() >= 5:  # 5 = субота, 6 = неділя
                        congr_date = congr_date + timedelta(
                            days=(7 - congr_date.weekday())
                        )
                    greetings.append(
                        f"{congr_date.strftime('%Y-%m-%d')}: {rec.name.value}"
                    )
        return greetings
