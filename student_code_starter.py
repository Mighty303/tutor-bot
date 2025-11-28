def is_command(text: str) -> bool:
    # TODO: return True if text starts with '!'
    pass

def handle_ping(text: str) -> str:
    # TODO: if text == 'ping', return 'pong'
    # otherwise return something else
    pass

def student_handle(input_str: str, state: dict) -> dict:
    # DO NOT EDIT THIS FUNCTION except where marked.
    
    # 1. command detection
    if is_command(input_str):
        return {"output": "That's a command!", "state": state}
    
    # 2. ping check
    if input_str == "ping":
        return {"output": handle_ping(input_str), "state": state}

    # default
    return {"output": "I don't understand.", "state": state}
