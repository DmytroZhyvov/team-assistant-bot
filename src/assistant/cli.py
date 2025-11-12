from .models import AddressBook, Record
from .storage import load_data, save_data
from .handlers import (
    parse_input,
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
    add_email,
    show_email,
    remove_contact,
)


def main():
    # Завантажуэмо AddressBook з файлу
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        if command in ("close", "exit"):
            # Перед виходом зберігаємо AddressBook у файл
            save_data(book)
            print("Data saved. Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command in ("remove-contact", "delete-contact"):
            print(remove_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        elif command == "add-email":
            print(add_birthday(args, book))
        elif command == "show-email":
            print(show_birthday(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
