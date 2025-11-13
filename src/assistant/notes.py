from collections import UserDict


class Note:
    """
    Клас однієї нотатки.
    Зберігає текст і список тегів (опціонально).
    """

    def __init__(self, text: str, tags=None):
        self.text = text.strip()
        self.tags = []
        if tags:
            for tag in tags:
                self.add_tag(tag)

    def add_tag(self, tag: str):
        """Додає тег до нотатки."""
        tag = tag.strip("#").lower()
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str):
        """Видаляє тег з нотатки."""
        tag = tag.strip("#").lower()
        if tag in self.tags:
            self.tags.remove(tag)

    def match(self, keyword: str) -> bool:
        """Перевіряє, чи відповідає нотатка пошуку по тегу або ключовому слову."""
        keyword = keyword.lower()
        return self.match_text(keyword) or self.match_tag(keyword)

    def match_text(self, keyword: str) -> bool:
        """Перевіряє, чи містить нотатка певне слово в тексті."""
        return keyword.lower() in self.text.lower()

    def match_tag(self, tag: str) -> bool:
        """Перевіряє, чи має нотатка певний тег."""
        tag = tag.strip("#").lower()
        return tag in [t.lower() for t in self.tags]

    def __str__(self):
        tags_str = ", ".join(f"#{t}" for t in self.tags) if self.tags else "—"
        return f"{self.text} | Tags: {tags_str}"


class NotesBook(UserDict):
    """
    Клас для зберігання та управління нотатками.
    """

    def add_note(self, text: str, tags=None):
        """Додає нову нотатку."""
        note_id = len(self.data) + 1
        self.data[note_id] = Note(text, tags)
        return f"Note added (ID: {note_id})."

    def delete_note(self, note_id: int):
        """Видаляє нотатку за ID."""
        if note_id in self.data:
            del self.data[note_id]
            return "Note deleted."
        return "Note not found."

    def get_note(self, note_id: int):
        """Повертає нотатку за ID."""
        return self.data.get(note_id, None)

    def edit_note(self, note_id: int, new_text: str):
        """Редагує текст нотатки."""
        if note_id in self.data:
            self.data[note_id].text = new_text
            return "Note updated."
        return "Note not found."

    def find_notes(self, keyword: str):
        """Пошук нотаток за тегом або словом."""
        results = [
            f"{note_id}: {note}"
            for note_id, note in self.data.items()
            if note.match(keyword)
        ]
        return "\n".join(results) if results else "No matches found."

    def show_all(self):
        """Показує всі нотатки."""
        if not self.data:
            return "No notes found."
        return "\n".join(f"{idx}: {note}" for idx, note in self.data.items())

    def get_notes_by_tag(self, tag: str):
        """Повертає всі нотатки, які містять вказаний тег."""
        tag = tag.strip("#").lower()
        results = [
            f"{note_id}: {note}"
            for note_id, note in self.data.items()
            if tag in note.tags
        ]
        return "\n".join(results) if results else "No notes with this tag."

    def sort_by_tags(self):
        """Повертає всі нотатки, згруповані за тегами."""
        tag_map = {}

        for note_id, note in self.data.items():
            for tag in note.tags:
                tag_map.setdefault(tag, []).append(f"{note_id}: {note}")

        if not tag_map:
            return "No tags found."

        result = []
        for tag in sorted(tag_map.keys()):
            result.append(f"\n#{tag}:")
            result.extend(tag_map[tag])

        return "\n".join(result)
