# tests/test_utils.py
import importlib
import student_code
importlib.reload(student_code)

def run_case(input_str, state=None):
    if state is None:
        state = {}
    out = student_code.student_handle(input_str, state)
    return out