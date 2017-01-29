from setuptools import setup

APP = ['moneypython/converter.py']
DATA_FILES = []
OPTIONS= {'iconfile': 'icons/moneypython.icns'}

setup(
    name = "moneypython",
    app = APP,
    data_files = DATA_FILES,
    options = {'py2app': OPTIONS},
    setup_requires = ['py2app']
)
