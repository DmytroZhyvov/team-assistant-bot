# Team Assistant Bot

CLI-based **Personal Assistant Bot** built with Python.  
Manages contacts and birthdays — supports adding, editing, searching, and storing data with validation and persistence.

---

## Features

✅ Add, edit and delete contact  
✅ Store and show birthdays  
✅ Validate phone numbers  
✅ Show upcoming birthdays  
✅ Persistent data (saved automatically between sessions)

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