# Discord Teach Bot

This repository is a minimal, **ready-to-run** teaching environment that hides Discord complexity from students and lets them focus on Python basics: loops, conditionals, lists, inputs, functions.

> **How it works (short):**
>
> * You run the bot (your machine). The bot receives Discord messages.
> * It calls `student_code.student_handle(input_str, state)` and sends the returned `output` back to Discord.
> * Student edits only `student_code.py` (pure synchronous Python). They never import `discord` or touch async.
> * A state manager persist per-user state between messages.
> * An automated tester runs student code against level specs.

---

## Folder structure

```
discord-teach-bot/
├─ bot.py                 # The Discord bot (yours only)
├─ state_manager.py       # simple JSON-backed per-user state manager
├─ student_code.py        # STUDENTS EDIT THIS - single entry point
├─ levels/                # Lesson level specs and tests
│  ├─ 01_conditionals.json
│  ├─ 02_loops.json
│  ├─ 03_lists.json
│  └─ 04_functions.json
├─ tests/
│  ├─ runner.py           # automated tester CLI
│  └─ test_utils.py       # helpers for tests
├─ requirements.txt
└─ README.md
```

---

## Important design constraints

* **Student API (stable):**

```python
# signature in student_code.py
def student_handle(input_str: str, state: dict) -> dict:
    """Return {'output': str, 'state': dict}

    * Only allowed to use plain Python (no discord imports).
    * `state` is any JSON-serializable dict persisted between calls.
    """
```

* The bot reloads `student_code` every time it needs to run their code, so changes are reflected immediately.
* The tester also imports the same file and calls `student_handle` for test vectors.

---

## Files (full code)

> **Open the files below in your editor**. Students only ever edit `student_code.py`.

### `requirements.txt`

```
discord.py==2.3.2
python-dotenv
```

(Adjust versions as you like.)

---

### `bot.py`

```python
# bot.py  (run this locally)
import discord
import importlib
import json
import os
from state_manager import StateManager

# load token from env for safety
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
if not TOKEN:
    print('ERROR: set DISCORD_BOT_TOKEN in your environment')

sm = StateManager('state.json')

class TutorBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (id: {self.user.id})')

    async def on_message(self, message):
        # ignore ourselves
        if message.author.id == self.user.id:
            return

        # simple command prefix to trigger students: !run <text>
        content = message.content.strip()
        if not content.startswith('!run'):
            return

        payload = content[len('!run'):].strip()
        # load student code fresh each message
        try:
            import student_code
            importlib.reload(student_code)
        except Exception as e:
            await message.channel.send(f'Bot error loading student code: {e}')
            return

        user_state = sm.get_state(str(message.author.id))
        try:
            result = student_code.student_handle(payload, user_state)
        except Exception as e:
            await message.channel.send(f'Error in student code: {e}')
            return

        # Expect result to be dict with output and state
        if not isinstance(result, dict) or 'output' not in result:
            await message.channel.send('student_handle must return a dict with key "output"')
            return

        sm.set_state(str(message.author.id), result.get('state', user_state))
        await message.channel.send(result['output'])


intents = discord.Intents.default()
intents.message_content = True

client = TutorBot(intents=intents)
client.run(TOKEN)
```

---

### `state_manager.py`

```python
# state_manager.py
import json
import threading

class StateManager:
    def __init__(self, path='state.json'):
        self.path = path
        self.lock = threading.Lock()
        try:
            with open(self.path, 'r') as f:
                self.data = json.load(f)
        except Exception:
            self.data = {}

    def save(self):
        with self.lock:
            with open(self.path, 'w') as f:
                json.dump(self.data, f, indent=2)

    def get_state(self, user_id):
        return self.data.get(user_id, {})

    def set_state(self, user_id, state):
        self.data[user_id] = state
        self.save()
```

---

### `student_code.py` (INITIAL TEMPLATE - students edit this file only)

```python
# student_code.py

# Students edit this file only. Keep the function signature exactly as below.

def student_handle(input_str: str, state: dict) -> dict:
    """Simple example logic for beginners.

    Commands supported in the starter:
    - show        : show current messages
    - add <text>  : append text to messages
    - clear       : clear messages
    """
    if state is None:
        state = {}

    messages = state.get('messages', [])

    parts = input_str.split()
    if not parts:
        return {'output': "(no input)", 'state': state}

    cmd = parts[0].lower()
    if cmd == 'show':
        return {'output': '\n'.join(messages) or '(no messages)', 'state': state}

    if cmd == 'add':
        rest = input_str[len('add'):].strip()
        messages.append(rest)
        state['messages'] = messages
        return {'output': f'Added: {rest}', 'state': state}

    if cmd == 'clear':
        state['messages'] = []
        return {'output': 'Cleared', 'state': state}

    return {'output': "I don't understand that command.", 'state': state}
```

Make the tasks progressively harder by editing `levels/*.json`.

---

### `levels/01_conditionals.json` (example level spec)

```json
{
  "title": "Conditionals: ping/pong and command detection",
  "description": "Detect ping and commands starting with !",
  "tests": [
    {"input": "ping", "expected_output_contains": "pong"},
    {"input": "!help", "expected_output_contains": "command"}
  ]
}
```

### `levels/02_loops.json`

```json
{
  "title": "Loops: iterate fake members",
  "description": "Given a fake members list in state, print numbered names.",
  "setup_state": {"members": ["Alice", "Bob", "Charlie"]},
  "tests": [
    {"input": "list_members", "expected_output_contains": "1. Alice"}
  ]
}
```

### `levels/03_lists.json`

```json
{
  "title": "Lists: add/remove users",
  "description": "Add or remove from a list in state",
  "tests": [
    {"input": "add_user Zoe", "expected_output_contains": "Zoe"},
    {"input": "remove_user Zoe", "expected_output_contains": "removed"}
  ]
}
```

### `levels/04_functions.json`

```json
{
  "title": "Functions: break logic into helpers",
  "description": "Refactor repetitive tasks into helper functions.",
  "tests": [
    {"input": "greet Alice", "expected_output_contains": "Hello Alice"}
  ]
}
```

---

### `tests/test_utils.py`

```python
# tests/test_utils.py
import importlib
import student_code
importlib.reload(student_code)

def run_case(input_str, state=None):
    if state is None:
        state = {}
    out = student_code.student_handle(input_str, state)
    return out
```

---

### `tests/runner.py` (automated tester CLI)

```python
# tests/runner.py
import json
import importlib
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import student_code

LEVELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'levels')


def run_level(file_name):
    path = os.path.join(LEVELS_DIR, file_name)
    spec = json.load(open(path))
    tests = spec.get('tests', [])
    setup_state = spec.get('setup_state', {})

    print('\n==', spec.get('title', file_name), '==')
    all_ok = True
    for t in tests:
        inp = t['input']
        expected = t['expected_output_contains']
        importlib.reload(student_code)
        res = student_code.student_handle(inp, dict(setup_state))
        out = res.get('output','')
        ok = expected in out
        print(f"INPUT: {inp}\nOUTPUT: {out}\nEXPECTS: '{expected}' -> {'OK' if ok else 'FAIL'}\n")
        all_ok = all_ok and ok

    if all_ok:
        print('LEVEL PASSED')
    else:
        print('LEVEL FAILED')


if __name__ == '__main__':
    # If provided a filename, run that level. Otherwise run all.
    args = sys.argv[1:]
    if args:
        for fn in args:
            run_level(fn)
    else:
        for fn in os.listdir(LEVELS_DIR):
            if fn.endswith('.json'):
                run_level(fn)
```

---

## How to run (developer)

1. Create a virtualenv and install requirements:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Set your bot token in environment (do not commit to git):

```bash
export DISCORD_BOT_TOKEN="YOUR_TOKEN"
python bot.py
```

3. In Discord, send messages like:

```
!run add hello world
!run show
!run clear
```

Students only ever edit `student_code.py`.

---

## How to run the automated tester

From repo root:

```bash
python tests/runner.py
# or run a specific level
python tests/runner.py 01_conditionals.json
```

The runner will import `student_code` fresh for every test and call `student_handle`.

---

## Lesson plans / Levels (brief)

* **01_conditionals** — identifying commands, if/else, startswith
* **02_loops** — `for` loops over lists, `enumerate`, counting
* **03_lists** — append/pop/filter, slicing
* **04_functions** — write helper functions, return values, pure functions

For each level provide 3-5 micro-exercises, start with a worked example and progress to open-ended challenges.

---

## Safety and tips

* Keep the student env sandboxed — run locally, never give students the bot token.
* Use fake data in state (members, messages) to simulate Discord.
* Encourage students to write small functions and test them using the `tests/runner.py` CLI.

---

## Next steps / optional upgrades

1. Add a `grader` mode that returns structured feedback (pass/fail + hints).
2. Make a web UI for students to edit code (optional, more complex).
3. Add timeouts / safety wrappers around student code to avoid infinite loops (can be done by running student code in a subprocess).

---
