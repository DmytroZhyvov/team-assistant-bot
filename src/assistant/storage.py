import pickle
from .models import AddressBook

DEFAULT_DB = "addressbook.pkl"


def save_data(book: AddressBook, filename: str = "addressbook.pkl") -> None:
    """Серіалізація адресної книги у файл за допомогою pickle."""
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename: str = "addressbook.pkl") -> AddressBook:
    """Десеріалізація адресної книги з файлу, або створення нової, якщо файл відсутній."""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
