from setuptools import setup, find_packages

setup(
    name='sqltree',
    version='0.1',
    url='https://github.com/ignamv/sqltree',

    # Author details
    author='Ignacio Martinez Vazquez',
    author_email='ignamv@gmail.com',

    # Choose your license
    license='GPLv3',
    packages=find_packages(exclude=("tests",)),
)

