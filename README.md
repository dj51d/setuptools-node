# setuptools extensions for working with Node.js

The setuptools_node package contains a number of useful setuptools extensions
for working with Node.js, many useful web development tools can be found in the
npm ecosystem.

## General Use

In general custom setuptools command are used by registering the custom command
in the `cmdclass` argument to the `setup()` function

```python
setup(cmdclass={ 'my_command': MyCommand })
```

### General options

By default all paths are relative to the directory containing `setup.py`.  Node
will be in the `node` directory and node modules in `node_modules`

* `--node-dir` Specify an alternate directory where node may be found
* `--node-modules-dir` Specify an alternate directory for node modules

## InstallNode

The `InstallNode` command is used to fetch a copy of node.js and install it
in the project directory.  The download will be cached in the `cache` directory
to facilitate a quick reinstall.

### InstallNode Options

* `--node-dist-url` Specify the URL from which to fetch node
* `--node-version` Specify the version of node to fetch
* `--cache-dir` Specify the directory in which to store the node download

setup.py:

```python
from setuptools_node import InstallNode


setup(cmdclass={ 'install_node': InstallNode })
```

Use:

```sh
user@host $ python setup.py install_node
```

## NpmInstall

The `NpmInstall` command is used to install modules from npm.  By default
`npm install` is used, `npm ci` may be specified with `--use-ci`

### NpmInstall Options

* `--use-ci` Use `npm ci` to install modules instead of `npm install`

setup.py:

```python
from setuptools_node import NpmInstall


setup(cmdclass={ 'npm_install': NpmInstall })
```

Use:

```sh
user@host $ python setup.py npm_install  # or
user@host $ python setup.py npm_install --use-ci
```

## Gulp

The `Gulp` command runs the gulp build tool

### Gulp Options

* `--task` Specify the task to run insteaed of the default

setup.py:

```python
from setuptools_node import Gulp


setup(cmdclass={ 'gulp': Gulp })
```

Use:

```sh
user@host $ python setup.py gulp  # run default task
user@host $ python setup.py gulp --task foo  # run the 'foo' task
```

## GulpBuild

The `GulpBuild` command provides a version of `build_py` that executes gulp
before proceeding with the normal `build_py` process, this allows you to
build/transform static files for a web application before they are included
in the package built by `build_py`.

Node will be installed if it is not found, and modules will be
installed/updated.

setup.py:

```python
from setuptools_node import GulpBuild


setup(cmdclass={ 'build_py': GulpBuild })
```

Use:

```sh
user@host $ python setup.py bdist_wheel
```
