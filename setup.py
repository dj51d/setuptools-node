import os
from shutil import rmtree
from setuptools import Command, find_packages, setup


with open('README.md', 'r') as f:
    long_description = f.read()


class Clean(Command):
    """Clean up build results

    With PEP 632, distutils is deprecated and setuptools does not appear to
    include a clean command.  Additionall, the old distutils clean command
    failed to remove things like the dist and *.egg-info directories.
    """
    descripion = 'clean up all build results'
    user_options = [
        ('dry-run', 'd', 'dry run')
    ]

    def initialize_options(self) -> None:
        self.egg_info = None
        self.dist_dir = None
        self.eggs = None
        self.dry_run = None

    def finalize_options(self) -> None:
        dist_name = self.distribution.get_name()
        self.egg_info = f'{dist_name}.egg-info'
        self.dist_dir = self.get_finalized_command('sdist').dist_dir
        self.eggs = '.eggs'

    def run(self) -> None:
        dirs = [self.egg_info, self.dist_dir, self.eggs]

        for directory in dirs:
            if os.path.exists(directory):
                self.remove_tree(directory)

    def remove_tree(self, directory: str) -> None:
        if self.dry_run:
            print(f'Remove directory {directory}')
        else:
            rmtree(directory)


setup(
    name='setuptools_node',
    version='0.3.0.dev1',
    description='Setuptools extensions for working with node',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dj51d/setuptools-node',
    author='Dan Johnson',
    author_email='dj51d@warbirdsurvivors.com',
    packages=find_packages(),
    install_requires=[
        'setuptools>=65.5.1'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    cmdclass={
        'clean': Clean
    }
)
