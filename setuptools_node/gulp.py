'''Setuptools commands for running the gulp build tool'''

from distutils.errors import DistutilsError
from setuptools.command.build_py import build_py
import subprocess
from .node import InstallNode, NodeCommand, NpmInstall


class Gulp(NodeCommand):
    '''Setuptools command for running gulp

    Usage in setup.py::

        from setuptools_node import Gulp

        setup(cmdclass={ 'gulp': Gulp })

    '''
    description = 'Run gulp'
    user_options = NodeCommand.base_options + [
        ('task=', None, 'Specify the gulp task to run')
    ]

    def initialize_options(self):
        super().initialize_options()
        self.task = 'default'

    def finalize_options(self):
        super().finalize_options()

    def run(self):
        gulp = self.node_modules / 'gulp' / 'bin' / 'gulp.js'
        tasks = self.task.split(',')
        args = [
            str(self.node.resolve()),
            str(gulp.resolve()),
        ]
        args = args + tasks
        res = subprocess.run(args)
        if res.returncode != 0:
            raise DistutilsError('Failed to run gulp {}'.format(self.task))


class GulpBuild(build_py):
    '''Custom build_py command that runs gulp.

    Replace build_py with this command to have node automatically installed
    (if required), and have gulp run to execute the default task before
    proceeding with the regular build_py tasks.

    Usage in setup.py::

        from setuptools_node import GulpBuild

        setup(cmdclass={ 'build_py': GulpBuild })

    '''
    user_options = build_py.user_options + [
        ('task=', None, 'Specify the gulp task(s) to run')
    ]

    def initialize_options(self):
        self.task = 'default'
        return super().initialize_options()

    def finalize_options(self):
        return super().finalize_options()

    def run_setuptools_command(self, command, **params):
        cmd = command(self.distribution)
        cmd.initialize_options()
        if params:
            for key, value in params.items():
                setattr(cmd, key, value)
        cmd.finalize_options()
        cmd.run()

    def run(self):
        self.run_setuptools_command(InstallNode)
        self.run_setuptools_command(NpmInstall)
        self.run_setuptools_command(Gulp, task=self.task)
