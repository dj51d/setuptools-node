from setuptools import find_packages, setup


setup(
    name='setuptools_node',
    version='0.1.1',
    description='Setuptools extensions for working with node',
    url='https://github.com/dj51d/setuptools-node',
    author='Dan Johnson',
    author_email='dj51d@warbirdsurvivors.com',
    packages=find_packages(),
    install_requires=[
        'setuptools>=40.0.0'
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
    ]
)
