from .storage import load_data, save_data, load_notes, save_notes
from .handlers import (
    parse_input,
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
    remove_contact,
    remove_phone,
    add_email,
    edit_email,
    add_note,
    edit_note,
    delete_note,
    find_note,
    add_note_tag,
    remove_note_tag,
    find_note_tag,
    sort_tags,
)
from prompt_toolkit import PromptSession
from .autocomplete import COMMANDS, CommandCompleter


def main():
    # Завантажуємо AddressBook та NoteBook з файлу
    book = load_data()
    notes = load_notes()
    print("Welcome to the assistant bot!")

    # Ініціалізуємо інтерактивну сесію введення команд:
    # - працює автодоповнення лише для назви команди
    # - підказки з’являються під час набору тексту (без автоматичної вставки)
    session = PromptSession(
        completer=CommandCompleter(COMMANDS),
        complete_while_typing=True,
    )

    while True:
        user_input = session.prompt("Enter a command: ")
        command, args = parse_input(user_input)
        if command in ("close", "exit"):
            # Перед виходом зберігаємо AddressBook та NoteBook у файл
            save_data(book)
            save_notes(notes)
            print("Data saved. Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add-contact":
            print(add_contact(args, book))
        elif command == "remove-contact":
            print(remove_contact(args, book))
        elif command == "change-contact":
            print(change_contact(args, book))
        elif command == "remove-phone":
            print(remove_phone(args, book))
        elif command == "show-phone":
            print(show_phone(args, book))
        elif command == "show-all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        elif command == "add-email":
            print(add_email(args, book))
        elif command == "change-email":
            print(edit_email(args, book))
        # --- Нотатки ---
        elif command == "add-note":
            print(add_note(args, notes))
        elif command == "show-notes":
            print(notes.show_all())
        elif command == "find-note":
            print(find_note(args, notes))
        elif command == "edit-note":
            print(edit_note(args, notes))
        elif command == "delete-note":
            print(delete_note(args, notes))
        # --- Теги ---
        elif command == "add-tag":
            print(add_note_tag(args, notes))
        elif command == "remove-tag":
            print(remove_note_tag(args, notes))
        elif command == "find-tag":
            print(find_note_tag(args, notes))
        elif command == "sort-tags":
            print(sort_tags(notes))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
