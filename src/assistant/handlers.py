from functools import wraps
from assistant.models import AddressBook, Record


def input_error(func):
    """Декоратор для обробки помилок вводу користувача."""

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Enter the command followed by necessary arguments."

    return inner


def parse_input(user_input: str) -> tuple[str, list[str]]:
    """Парсить вхідний рядок на команду та аргументи."""
    parts = user_input.strip().split()
    if not parts:
        return "", []
    cmd = parts[0].lower()
    return cmd, parts[1:]


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    """Додає або оновлює контакт у адресній книзі."""
    name, phone, *_ = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
    """Змінює номер телефону для вказаного контакту."""
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if not record:
        raise KeyError
    if record.edit_phone(old_phone, new_phone):
        return "Phone updated."
    return "Old phone not found."


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    """Показує телефонні номери для вказаного контакту."""
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError
    phones = "; ".join(p.phone_number for p in record.phones) or "No phones."
    return phones


@input_error
def add_email(args: list[str], book: AddressBook) -> str:
    """Додає email до існуючого контакту."""
    name, email_str, *_ = args
    record = book.find(name)
    if not record:
        raise KeyError
    record.add_email(email_str)
    return f"Email added for contact '{name}'."

@input_error
def show_email(args: list[str], book: AddressBook) -> str:
    """Показує email для вказаного контакту."""
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError
    if record.email:
        return record.email.value
    return "Email not set."


def show_all(book: AddressBook) -> str:
    """Показує всі контакти в адресній книзі."""
    if not book.data:
        return "No contacts."
    return "\n".join(str(rec) for rec in book.data.values())


@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    """Додає дату народження для вказаного контакту."""
    name, bday_str, *_ = args
    record = book.find(name)
    if not record:
        raise KeyError
    record.add_birthday(bday_str)
    return "Birthday added."


@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    """Показує дату народження для вказаного контакту."""
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError
    if record.birthday:
        return record.birthday.date_str
    return "Birthday not set."


def birthdays(book: AddressBook) -> str:
    """Показує дні народження, які відбудуться протягом наступного тижня."""
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next 7 days."
    return "\n".join(upcoming)


@input_error
def remove_contact(args: list[str], book: AddressBook) -> str:
    """Видаляє контакт з адресної книги за їм'ям."""
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError
    book.delete(name)
    return f"Contact '{name}' has been removed."
