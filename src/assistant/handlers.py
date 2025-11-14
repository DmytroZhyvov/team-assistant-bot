from functools import wraps
from assistant.models import AddressBook, Record
from assistant.notes import NotesBook

DEFAULT_BIRTHDAY_DAYS = 7


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
def remove_phone(args: list[str], book: AddressBook) -> str:
    """Видаляє конкретний номер телефону з контакту."""

    name, phone, *_ = args
    record = book.find(name)
    if not record:
        raise KeyError
    if not record.phones:
        return "No phones."
    if not record.find_phone(phone):
        return "Phone not found."
    record.remove_phone(phone)
    return f"Phone {phone} has been removed."


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


@input_error
def birthdays(args: list[str], book: AddressBook) -> str:
    """Показує дні народження, які відбудуться протягом наступного тижня."""
    days = int(args[0]) if args else DEFAULT_BIRTHDAY_DAYS
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return f"No birthdays in the next {days} {"days" if days != 1 else "day"}."
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


@input_error
def add_email(args: list[str], book: AddressBook) -> str:
    name, email, *_ = args
    record = book.find(name)
    if not record:
        raise KeyError
    record.add_email(email)
    return "Email added."


@input_error
def edit_email(args: list[str], book: AddressBook) -> str:
    name, new_email, *_ = args
    record = book.find(name)
    if not record:
        raise KeyError
    record.edit_email(new_email)
    return "Email updated."


@input_error
def add_note(args: list[str], notes: NotesBook) -> str:
    """Додає нову нотатку."""
    text = " ".join(args)
    return notes.add_note(text)


@input_error
def find_note(args: list[str], notes: NotesBook) -> str:
    """Пошук нотаток за тегом або словом."""
    keyword = " ".join(args)
    return notes.find_notes(keyword)


@input_error
def edit_note(args: list[str], notes: NotesBook) -> str:
    """Редагує текст нотатки."""
    note_id = int(args[0])
    new_text = " ".join(args[1:])
    return notes.edit_note(note_id, new_text)


@input_error
def delete_note(args: list[str], notes: NotesBook) -> str:
    """Видаляє нотатку за ID."""
    note_id = int(args[0])
    return notes.delete_note(note_id)


@input_error
def add_note_tag(args, notes: NotesBook):
    """add-tag <id> <#tag>"""
    if len(args) < 2:
        raise ValueError("Usage: add-tag <id> <#tag>")
    note_id = int(args[0])
    tag = args[1]
    note = notes.get_note(note_id)
    if not note:
        return "Note not found."
    note.add_tag(tag)
    return "Tag added."


@input_error
def remove_note_tag(args, notes: NotesBook):
    """remove-tag <id> <#tag>"""
    if len(args) < 2:
        raise ValueError("Usage: remove-tag <id> <#tag>")
    note_id = int(args[0])
    tag = args[1]
    note = notes.get_note(note_id)
    if not note:
        return "Note not found."
    note.remove_tag(tag)
    return "Tag removed."


@input_error
def find_note_tag(args, notes: NotesBook):
    """find-tag <#tag>"""
    if not args:
        raise ValueError("Please provide tag.")
    tag = args[0]
    return notes.get_notes_by_tag(tag)


def sort_tags(notes: NotesBook):
    return notes.sort_by_tags()
