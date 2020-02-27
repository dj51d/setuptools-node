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


class RunnerMixin(object):
    """Mixin for setuptools commands to invoke other commands"""
    def run_setuptools_command(self, command, **params):
        cmd = command(self.distribution)
        cmd.initialize_options()
        if params:
            for key, value in params.items():
                setattr(cmd, key, value)
        cmd.finalize_options()
        cmd.run()
