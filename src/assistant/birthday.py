from datetime import datetime, timedelta
from assistant.models import AddressBook, Record
from assistant.storage import save_data, load_data

def create_birthdays(book: AddressBook):
    """Створює початкові дні народження"""
    birthdays = [
        ("Ivan Serduk", "01.10.1985"),
        ("Eva Black", "07.11.1999"),
        ("Lilia Vovk", "24.07.2002")
    ]
    for name, bday_str in birthdays:
        record = book.find(name)
        if not record:
            record = Record(name)
            book.add_record(record)
        # додаємо або оновлюємо день народження
        record.birthday = bday_str
    return book

def add_or_update_birthday(book: AddressBook, name: str, birthday: str):
    """Додає або оновлює день народження для користувача"""
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.birthday = birthday
    save_data(book)
    print(f"Birthday set for {name}: {birthday}")

def find_same_birthdays(book: AddressBook):
    """Шукає користувачів з однаковими днями народження"""
    result = {}
    for record in book.data.values():
        if record.birthday:
            # Використовуємо str(record.name), якщо name не рядок
            result.setdefault(str(record.birthday), []).append(str(record.name))
    # Показуємо дні, коли є більше одного користувача
    for bday, names in result.items():
        if len(names) > 1:
            print(f"{bday}: {', '.join(names)}")

def show_upcoming_birthdays(book: AddressBook, days_ahead: int = 30):
    """Показує користувачів, у яких день народження протягом найближчих days_ahead днів"""
    today = datetime.today()
    upcoming = []
    for record in book.data.values():
        if record.birthday:
            # Якщо об'єкт Birthday, беремо його як рядок у форматі ISO (YYYY-MM-DD)
            bday_str = str(record.birthday)
            # Парсимо у datetime
            try:
                bday_date = datetime.strptime(bday_str, "%Y-%m-%d")
            except ValueError:
                # Якщо все ще DD.MM.YYYY
                bday_date = datetime.strptime(bday_str, "%d.%m.%Y")
            
            # Наступне святкування (цей рік)
            next_bday = bday_date.replace(year=today.year)
            if next_bday < today:
                next_bday = next_bday.replace(year=today.year + 1)
            if 0 <= (next_bday - today).days <= days_ahead:
                upcoming.append((record.name, next_bday.strftime("%d.%m.%Y")))
    
    if upcoming:
        print(f"\nUpcoming birthdays in the next {days_ahead} days:")
        for name, bday in sorted(upcoming, key=lambda x: datetime.strptime(x[1], "%d.%m.%Y")):
            print(f"{name}: {bday}")
    else:
        print(f"\nNo upcoming birthdays in the next {days_ahead} days.")

if __name__ == "__main__":
    # Завантажуємо адресну книгу
    book = load_data()
    
    # Створюємо початкові дні народження
    book = create_birthdays(book)

    # Приклади використання
    add_or_update_birthday(book, "John Doe", "01.10.1985")
    add_or_update_birthday(book, "Emma Brown", "12.12.1986")

    print("\nUsers with the same birthdays:")
    find_same_birthdays(book)

    # Показуємо найближчі дні народження
    show_upcoming_birthdays(book, days_ahead=60)

    # Зберігаємо зміни
    save_data(book)
    print("\nAll birthdays updated successfully!")