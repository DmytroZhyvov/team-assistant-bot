from prompt_toolkit.completion import Completer, Completion

COMMANDS = [
    "hello",
    "add",
    "remove-contact",
    "delete-contact",
    "change",
    "remove-phone",
    "phone",
    "all",
    "add-birthday",
    "show-birthday",
    "birthdays",
    "add-email",
    "change-email",
    "close",
    "exit",
]

class CommandCompleter(Completer):
    """
    Autocomplete only for the *command* part
    """

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