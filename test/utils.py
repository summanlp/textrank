import os.path
import sys


def get_test_file_path(file):
    pre_path = os.path.join(os.path.dirname(__file__), 'test_data')
    return os.path.join(pre_path, file)


def get_text_from_test_data(file):
    file_path = get_test_file_path(file)
    with open(file_path, mode='r', encoding="utf-8") as f:
        return f.read()


def silence_stderr(f):
    def new_f(*args, **kwargs):
        real_stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')
        try:
            return f(*args, **kwargs)
        finally:
            sys.stderr.close()
            sys.stderr = real_stderr

    return new_f