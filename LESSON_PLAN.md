# Python Discord Bot - Lesson Plan

Welcome! In this course, you'll learn Python basics by building a Discord bot that responds to messages. You'll work **only** in `student_code.py` using plain Python—no Discord libraries needed!

---

## How to Test Your Code

After making changes to `student_code.py`, you can test in two ways:

1. **In Discord**: Send messages like `!run ping` or `!run add hello`
2. **Automated Tests**: Run `python tests/runner.py` from the terminal

---

## Level 1: Conditionals & String Basics

**Goal**: Learn `if/else`, string methods like `.startswith()`, and equality checks.

### Exercise 1.1: Detect Commands

**Task**: Complete the `is_command()` function to return `True` if the text starts with `!`.

```python
def is_command(text: str) -> bool:
    # TODO: return True if text starts with '!'
    pass
```

**Expected Behavior**:
```
Input:  "!help"
Output: "That's a command!"

Input:  "hello"
Output: "I don't understand."
```

**Hint**: Use the `.startswith()` method!

---

### Exercise 1.2: Ping-Pong

**Task**: Complete the `handle_ping()` function to return `"pong"` when input is `"ping"`.

```python
def handle_ping(text: str) -> str:
    # TODO: if text == 'ping', return 'pong'
    # otherwise return something else
    pass
```

**Expected Behavior**:
```
Input:  "ping"
Output: "pong"

Input:  "hello"
Output: "I don't understand."
```

---

### Exercise 1.3: Multiple Commands

**Task**: Add support for multiple commands: `!help`, `!about`, `!hello`.

**Expected Behavior**:
```
Input:  "!help"
Output: "Available commands: !help, !about, !hello"

Input:  "!about"
Output: "This is a learning bot made by [Your Name]!"

Input:  "!hello"
Output: "Hello there! 👋"
```

**Hint**: Use `if/elif/else` statements to check which command was sent.

---

### Exercise 1.4: Case Insensitive Commands

**Task**: Make commands work regardless of capitalization (e.g., `PING`, `Ping`, `ping` all work).

**Expected Behavior**:
```
Input:  "PING"
Output: "pong"

Input:  "PiNg"
Output: "pong"
```

**Hint**: Use `.lower()` method to convert strings to lowercase.

---

## Level 2: Loops & Lists

**Goal**: Learn `for` loops, iterating over lists, and using `enumerate()`.

### Exercise 2.1: List Members

**Task**: When the user sends `"list_members"`, loop through a list of fake members in state and print them numbered.

```python
def student_handle(input_str: str, state: dict) -> dict:
    if state is None:
        state = {}
    
    # Set up fake members if not present
    if 'members' not in state:
        state['members'] = ['Nina', 'Megan', 'Martin']
    
    if input_str == 'list_members':
        # TODO: loop through state['members'] and build a numbered list
        pass
```

**Expected Behavior**:
```
Input:  "list_members"
Output: "1. Nina
2. Megan
3. Martin"
```

**Hint**: Use a `for` loop with `enumerate(state['members'], start=1)`.

---

### Exercise 2.2: Count Items

**Task**: Add a command `"count_members"` that returns how many members are in the list.

**Expected Behavior**:
```
Input:  "count_members"
Output: "There are 3 members."
```

**Hint**: Use `len(state['members'])`.

---

### Exercise 2.3: Filter by Letter

**Task**: Add command `"members_with A"` to show only members whose names start with 'A'.

**Expected Behavior**:
```
Input:  "members_with A"
Output: "Members starting with A: Nina"

Input:  "members_with B"
Output: "Members starting with B: Megan"
```

**Hint**: Use a `for` loop and an `if` statement inside it to filter.

---

### Exercise 2.4: Repeat Message

**Task**: If user sends `"repeat Hello 3"`, output `"Hello"` three times.

**Expected Behavior**:
```
Input:  "repeat Hello 3"
Output: "Hello
Hello
Hello"

Input:  "repeat Python 5"
Output: "Python
Python
Python
Python
Python"
```

**Hint**: Use `input_str.split()` to parse the command, then use a `for` loop with `range()`.

---

## Level 3: Working with Lists (Add/Remove/Modify)

**Goal**: Learn to manipulate lists using `.append()`, `.remove()`, list comprehensions, and slicing.

### Exercise 3.1: Add User to List

**Task**: Implement `"add_user <name>"` to add a new member to the state.

**Expected Behavior**:
```
Input:  "add_user Zoe"
Output: "Added Zoe to the list!"

Input:  "list_members"
Output: "1. Nina
2. Megan
3. Martin
4. Zoe"
```

---

### Exercise 3.2: Remove User from List

**Task**: Implement `"remove_user <name>"` to remove a member.

**Expected Behavior**:
```
Input:  "remove_user Megan"
Output: "Removed Megan from the list."

Input:  "list_members"
Output: "1. Nina
2. Martin"
```

**Hint**: Use `.remove()` method or rebuild the list without that member.

---

### Exercise 3.3: Todo List

**Task**: Build a simple todo list with commands: `"add_todo"`, `"show_todos"`, `"complete_todo <number>"`.

**Expected Behavior**:
```
Input:  "add_todo Buy groceries"
Output: "Added: Buy groceries"

Input:  "add_todo Finish homework"
Output: "Added: Finish homework"

Input:  "show_todos"
Output: "1. Buy groceries
2. Finish homework"

Input:  "complete_todo 1"
Output: "Completed: Buy groceries"

Input:  "show_todos"
Output: "1. Finish homework"
```

---

### Exercise 3.4: Clear All

**Task**: Add a `"clear_all"` command that removes everything from the list.

**Expected Behavior**:
```
Input:  "clear_all"
Output: "List cleared!"

Input:  "list_members"
Output: "(no members)"
```

---

## Level 4: Functions & Code Organization

**Goal**: Learn to break code into reusable helper functions with parameters and return values.

### Exercise 4.1: Greet Function

**Task**: Create a helper function `greet(name: str) -> str` that returns a personalized greeting.

```python
def greet(name: str) -> str:
    # TODO: return a greeting like "Hello, [name]!"
    pass

def student_handle(input_str: str, state: dict) -> dict:
    if input_str.startswith('greet '):
        name = input_str[6:].strip()
        return {'output': greet(name), 'state': state}
    # ... rest of code
```

**Expected Behavior**:
```
Input:  "greet Nina"
Output: "Hello, Nina!"

Input:  "greet Megan"
Output: "Hello, Megan!"
```

---

### Exercise 4.2: Calculate Age

**Task**: Create a function `calculate_age(birth_year: int) -> int` and command `"age <year>"`.

**Expected Behavior**:
```
Input:  "age 2010"
Output: "You are 14 years old!"

Input:  "age 2005"
Output: "You are 19 years old!"
```

**Hint**: Use `2024 - birth_year` (or get current year with `import datetime`).

---

### Exercise 4.3: Math Helper Functions

**Task**: Create helper functions for `add`, `subtract`, `multiply`, and `divide`.

```python
def add(a: int, b: int) -> int:
    return a + b

def subtract(a: int, b: int) -> int:
    # TODO
    pass

# ... more functions
```

**Expected Behavior**:
```
Input:  "math add 5 3"
Output: "5 + 3 = 8"

Input:  "math multiply 4 7"
Output: "4 × 7 = 28"

Input:  "math divide 10 2"
Output: "10 ÷ 2 = 5"
```

---

### Exercise 4.4: Parse Command Function

**Task**: Create a `parse_command(input_str: str) -> tuple` function that splits input into command and arguments.

```python
def parse_command(input_str: str) -> tuple:
    """Returns (command, arguments_list)"""
    # TODO: split input and return first word as command, rest as list
    pass
```

**Expected Behavior**:
```python
parse_command("add_user Nina") 
# Returns: ("add_user", ["Nina"])

parse_command("greet Megan Martin")
# Returns: ("greet", ["Megan", "Martin"])
```

---

## Level 5: Advanced State Management

**Goal**: Work with nested dictionaries, track user-specific data, and implement more complex features.

### Exercise 5.1: User Points System

**Task**: Track points for different users. Commands: `"points"`, `"give_points <name> <amount>"`.

**Expected Behavior**:
```
Input:  "points"
Output: "Your points: 0"

Input:  "give_points Nina 10"
Output: "Gave 10 points to Nina!"

Input:  "leaderboard"
Output: "1. Nina: 10 points"
```

---

### Exercise 5.2: Message History

**Task**: Store the last 5 messages a user sent.

**Expected Behavior**:
```
Input:  "history"
Output: "Your last messages:
1. hello
2. ping
3. list_members"
```

**Hint**: Keep a list in state and use slicing to keep only the last 5 items: `messages[-5:]`.

---

### Exercise 5.3: Mini Game - Guess the Number

**Task**: Implement a guessing game where the bot picks a random number (1-10) and users guess.

**Expected Behavior**:
```
Input:  "start_game"
Output: "I'm thinking of a number between 1 and 10. Guess it!"

Input:  "guess 5"
Output: "Too low! Try again."

Input:  "guess 8"
Output: "Correct! You got it in 2 tries!"
```

**Hint**: Use `import random` and `random.randint(1, 10)` to pick a number. Store it in state.

---

## Challenge Projects

Once you've completed all levels, try these open-ended projects:

### 🎯 Challenge 1: Quote Bot
Store a list of quotes and return a random one when user types `"inspire"`.

### 🎯 Challenge 2: Poll System
Create `"create_poll <question>"` and `"vote <option>"` commands.

### 🎯 Challenge 3: Word Counter
Count how many words a user has sent across all messages.

### 🎯 Challenge 4: Reminder System
Store reminders and show them with `"remind_me <text>"` and `"show_reminders"`.

---

## Tips for Success

1. **Read error messages carefully** - they tell you what went wrong!
2. **Test often** - test after every small change
3. **Use print statements** - add `print(state)` to see what's stored
4. **Ask for help** - if you're stuck for more than 10 minutes
5. **Have fun!** - programming is creative and rewarding

---

## Quick Reference

### Common String Methods
```python
text.startswith('!')    # Check if starts with !
text.endswith('?')      # Check if ends with ?
text.lower()            # Convert to lowercase
text.split()            # Split into list of words
text.strip()            # Remove whitespace from ends
```

### Common List Operations
```python
my_list.append(item)        # Add to end
my_list.remove(item)        # Remove specific item
my_list.pop(index)          # Remove by index
len(my_list)                # Get length
my_list[0]                  # Get first item
my_list[-1]                 # Get last item
```

### State Template
```python
def student_handle(input_str: str, state: dict) -> dict:
    if state is None:
        state = {}
    
    # Your code here
    
    return {'output': 'some text', 'state': state}
```

---

Good luck and happy coding! 🚀🐍
