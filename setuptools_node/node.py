'''Setuptools commands for working with node/npm'''

from distutils.core import Command
from distutils.errors import DistutilsError
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tarfile
import urllib.request
import zipfile

from .util import chdir, RunnerMixin


class NodeCommand(Command):
    '''Base for node related commands.

    Commands may subclass NodeCommand to get the basic paths and options
    setup for them.

    '''
    base_options = [
        ('node-dir=', None, 'Directory for Node install'),
        ('node-modules-dir=', None, 'Directory for node_modules')
    ]

    def resolve_path(self, path):
        if isinstance(path, str):
            return Path(path).resolve()
        return path

    def resolve_binary(self):
        exe = self.node_dir / 'node.exe'
        binary = self.node_dir / 'bin' / 'node'
        if exe.is_file():
            return exe
        elif binary.is_file():
            return binary

    def resolve_lib(self):
        lib = self.node_dir / 'lib' / 'node_modules'
        if not lib.is_dir():
            lib = self.node_dir / 'node_modules'
        return lib

    def initialize_options(self):
        self.base_dir = Path('.').resolve()
        self.node_dir = self.base_dir / 'node'
        self.node = self.resolve_binary()
        self.node_lib = self.resolve_lib()
        self.node_modules = self.base_dir / 'node_modules'

    def finalize_options(self):
        self.node_dir = self.resolve_path(self.node_dir)
        self.node = self.resolve_binary()
        self.node_lib = self.resolve_lib()
        self.node_modules = self.resolve_path(self.node_modules)

    def node_exists(self):
        return self.node is not None


class NpmInstall(NodeCommand, RunnerMixin):
    '''Command for installing packages with npm

    By default packages will be installed with ``npm install``, if the
    ``--use-ci`` argument is given, ``npm ci`` will be used instead.  In
    addition the common options from `:py:class:NodeCommand` are supported.

    Usage in setup.py::

        from setuptools_node import NpmInstall

        setup(cmdclass={ 'npm_install': NpmInstall })

    '''
    description = 'Run npm install'
    user_options = NodeCommand.base_options + [
        ('use-ci', None, 'Use npm ci instead of npm install')
    ]

    def initialize_options(self):
        super().initialize_options()
        self.use_ci = None

    def finalize_options(self):
        super().finalize_options()

    def run(self):
        npm = self.node_lib / 'npm' / 'bin' / 'npm-cli.js'
        if not self.node:
            self.run_setuptools_command(InstallNode)
            self.finalize_options()
        args = [
            str(self.node.resolve()),
            str(npm.resolve()),
            'ci' if self.use_ci else 'install',
            '--scripts-prepend-node-path'
        ]
        res = subprocess.run(args)
        if res.returncode != 0:
            raise DistutilsError('Failed to run npm install')


class InstallNode(NodeCommand):
    '''Command to install a local copy of node.js

    Usage in setup.py::

        from setuptools_node import InstallNode

        setup(cmdclass={ 'install_node': InstallNode })

    '''
    description = 'Install a local copy of node.js'
    user_options = NodeCommand.base_options + [
        ('node-dist-url=', None, 'Base URL to fetch Node from'),
        ('node-version=', None, 'Version of Node to fetch'),
        ('cache-dir=', None, 'Directory to cache Node distribution files')
    ]

    def node_archive(self):
        bits, _ = platform.architecture()
        arch = 'x64' if bits == '64bit' else 'x86'
        if sys.platform in ('win32', 'cygwin'):
            node_os = 'win'
            archive = 'zip'
        elif sys.platform in ('linux', 'linux2') and arch == 'x64':
            node_os = 'linux'
            archive = 'tar.xz'
        else:
            raise Exception('{} {} is not supported'.format(
                bits, sys.platform))
        filename = 'node-{}-{}-{}.{}'.format(
            self.node_version, node_os, arch, archive)
        dist_url = '{}{}/{}'.format(
            self.node_dist_url, self.node_version, filename)
        return filename, dist_url

    def initialize_options(self):
        super().initialize_options()
        self.node_dist_url = 'https://nodejs.org/dist/'
        self.node_version = 'v12.14.1'
        self.cache_dir = self.base_dir / 'cache'

    def finalize_options(self):
        super().finalize_options()
        self.cache_dir = self.resolve_path(self.cache_dir)

    def node_archive_exists(self, filename):
        archive = self.cache_dir / filename
        return archive.is_file()

    def download_node(self, url, filename):
        print('Downloading from {}'.format(url))
        if not self.cache_dir.is_dir():
            self.cache_dir.mkdir()
        archive = self.cache_dir / filename
        with urllib.request.urlopen(url) as response:
            with archive.open('wb') as f:
                shutil.copyfileobj(response, f)

    def install_node(self, filename):
        archive = self.cache_dir / filename
        opener = zipfile.ZipFile if filename.endswith('.zip') else tarfile.open
        with opener(archive) as f:
            names = f.namelist() if hasattr(f, 'namelist') else f.getnames()
            install_dir, _ = next(x for x in names if '/' in x).split('/', 1)
            bad_members = [
                x for x in names if x.startswith('/') or x.startswith('..')]
            if bad_members:
                raise Exception(
                    '{} appears to be malicious, bad filenames: {}'.format(
                        filename, bad_members))
            f.extractall(self.base_dir)
            with chdir(self.base_dir):
                os.rename(install_dir, self.node_dir.stem)

    def run(self):
        if self.node_exists():
            print('Using existing Node installation')
        else:
            print('Installing Node {}'.format(self.node_version))
            archive, url = self.node_archive()
            if not self.node_archive_exists(archive):
                self.download_node(url, archive)
            self.install_node(archive)
