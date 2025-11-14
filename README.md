# Team Assistant Bot

CLI-based **Personal Assistant Bot** built with Python.  
Helps you manage **contacts**, **birthdays**, **emails**, and **notes with tags** via simple text commands in the terminal.

---

## Features

### Contacts
- Add, edit and delete contacts
- Multiple phone numbers per contact
- Email with validation
- View all contacts

### Birthdays
- Store birthdays (`DD.MM.YYYY`)
- Show birthday for a specific contact
- List upcoming birthdays in the next _N_ days (default — 7)

### Notes & Tags
- Add, edit and delete notes
- Search notes by text or tag
- Add/remove tags to notes
- List notes by tag
- View notes grouped by tags

### Persistence
- All data is stored between sessions:
  - Contacts & birthdays
  - Notes & tags

### CLI Experience
- Interactive prompt powered by `prompt_toolkit`
- Autocomplete for commands (start typing a command and see suggestions)


---

## Installation

### 1️⃣ Clone the repository
```bash
  git clone https://github.com/DmytroZhyvov/team-assistant-bot.git
  cd team-assistant-bot
```

### 2️⃣ Create and activate a virtual environment
```bash
  python -m venv .venv
  source .venv/bin/activate        # macOS / Linux
# OR
  .venv\Scripts\activate           # Windows
```

### 3️⃣ Install dependencies
```bash
  pip install -r requirements.txt
```

### 4️⃣ (Optional) Install in editable mode
If you want to run it as a global command (assistant-bot):
```bash
  pip install -e .
```

### ▶️ Usage
After installation, run:
```bash
  assistant-bot
```
Or (if not installed in editable mode):
```bash
  python src/assistant/cli.py
```

### Commands
Below is the full list of available commands with usage examples.

| Command              | Description                                                       | Example                                       |
|----------------------|-------------------------------------------------------------------|-----------------------------------------------|
| `add-contact {name} {phone}` | Add a new contact or append a phone to an existing one      | `add-contact John 1234567890`                 |
| `remove-contact {name}`      | Delete a contact by name                                    | `remove-contact John`                         |
| `change-contact {name} {old_phone} {new_phone}` | Replace an existing phone number                 | `change-contact John 1234567890 0987654321` |
| `remove-phone {name} {phone}` | Remove a specific phone from a contact                      | `remove-phone John 1234567890`              |
| `show-phone {name}`          | Show all phone numbers for a contact                         | `show-phone John`                           |
| `show-all-contacts`          | Display all saved contacts                                   | `show-all-contacts`                           |

---

### Birthday Commands

| Command                       | Description                                                      | Example                               |
|-------------------------------|------------------------------------------------------------------|----------------------------------------|
| `add-birthday {name} {DD.MM.YYYY}` | Add a birthday to a contact                               | `add-birthday John 31.12.1990`       |
| `show-birthday {name}`       | Show the birthday of a contact                                   | `show-birthday John`                 |
| `birthdays-in {days}`        | Show birthdays in the next *N* days (default = 7)                | `birthdays-in 7` or `birthdays-in`     |

---

### Email Commands

| Command                       | Description                               | Example                                 |
|-------------------------------|-------------------------------------------|-----------------------------------------|
| `add-email {name} {email}`    | Add email to a contact                    | `add-email John john@example.com`       |
| `change-email {name} {email}` | Change existing email                     | `change-email John newjohn@example.com` |

---

### Note Commands

| Command                     | Description                               | Example                                      |
|-----------------------------|-------------------------------------------|----------------------------------------------|
| `add-note {text}`           | Add a new note                            | `add-note Buy milk and bread`                |
| `show-notes`                | Show all notes                            | `show-notes`                                  |
| `find-note {keyword}`       | Find notes by text or tag                 | `find-note milk` / `find-note #work`         |
| `edit-note {id} {text}`     | Edit a note by ID                         | `edit-note 1 Updated note text`              |
| `delete-note {id}`          | Delete a note by ID                       | `delete-note 1`                               |

---

### Tag Commands

| Command                           | Description                         | Example               |
|-----------------------------------|-------------------------------------|------------------------|
| `add-tag {id} {#tag}`             | Add tag to a note                   | `add-tag 1 #work`      |
| `remove-tag {id} {#tag}`          | Remove tag from a note              | `remove-tag 1 #work`   |
| `find-tag {#tag}`                 | Show all notes containing a tag     | `find-tag #work`       |
| `sort-tags`                       | Show notes grouped by tags          | `sort-tags`            |

---

### Exit

| Command | Description                         |
|---------|-------------------------------------|
| `close` | Save data and exit the assistant    |
| `exit`  | Same as `close`                     |
