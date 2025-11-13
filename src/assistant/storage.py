import pickle
from .models import AddressBook
from .notes import NotesBook

DEFAULT_DB = "addressbook.pkl"
DEFAULT_DB_NOTES = "notesbook.pkl"


def save_data(book: AddressBook, filename: str = DEFAULT_DB) -> None:
    """Серіалізація адресної книги у файл за допомогою pickle."""
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename: str = DEFAULT_DB) -> AddressBook:
    """Десеріалізація адресної книги з файлу, або створення нової, якщо файл відсутній."""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def save_notes(notes: NotesBook, filename: str = DEFAULT_DB_NOTES) -> None:
    """Серіалізація нотаток у файл за допомогою pickle."""
    with open(filename, "wb") as f:
        pickle.dump(notes, f)


def load_notes(filename: str = DEFAULT_DB_NOTES) -> NotesBook:
    """Десеріалізація нотаток з файлу, або створення нової, якщо файл відсутній."""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return NotesBook()


def save_all(
    book: AddressBook,
    notes: NotesBook,
    book_filename: str = DEFAULT_DB,
    notes_filename: str = DEFAULT_DB_NOTES,
) -> None:
    """Зберігає AddressBook та NotesBook у відповідні файли."""
    save_data(book, book_filename)
    save_notes(notes, notes_filename)


def load_all(
    book_filename: str = DEFAULT_DB, notes_filename: str = DEFAULT_DB_NOTES
) -> tuple[AddressBook, NotesBook]:
    """Завантажує AddressBook та NotesBook з файлів."""
    address_book = load_data(book_filename)
    notes_book = load_notes(notes_filename)
    return address_book, notes_book
