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