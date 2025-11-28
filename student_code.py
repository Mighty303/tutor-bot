# student_code.py
# Students edit this file only. Keep the function signature exactly as below.

def student_handle(input_str: str, state: dict) -> dict:
    """Simple example logic for beginners.


    Commands supported in the starter:
    - show : show current messages
    - add <text> : append text to messages
    - clear : clear messages
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