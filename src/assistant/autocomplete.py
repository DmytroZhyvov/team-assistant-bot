from prompt_toolkit.completion import Completer, Completion

COMMANDS = [
    "hello",
    "add-contact",
    "remove-contact",
    "change-contact",
    "remove-phone",
    "show-phone",
    "find-contact",
    "show-all-contacts",
    "add-birthday",
    "show-birthday",
    "birthdays-in",
    "add-email",
    "change-email",
    "add-address",
    "change-address",
    "add-note",
    "show-notes",
    "find-note",
    "edit-note",
    "delete-note",
    "add-tag",
    "remove-tag",
    "find-tag",
    "sort-tags",
    "close",
    "exit",
]


class CommandCompleter(Completer):
    """Клас автокомпліта для команд"""

    def __init__(self, commands: list[str]):
        self.commands = commands

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor

        if not text.strip() or " " in text:
            return

        word = text.strip()
        for cmd in self.commands:
            if cmd.startswith(word):
                yield Completion(cmd, start_position=-len(word))
