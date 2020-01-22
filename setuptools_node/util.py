'''Common utility functions'''

import contextlib
import os


@contextlib.contextmanager
def chdir(new_dir):
    '''Context Manager for changing the working directory'''
    cur_dir = os.getcwd()
    try:
        yield
    finally:
        os.chdir(cur_dir)
