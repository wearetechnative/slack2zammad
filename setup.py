from setuptools import setup, find_packages
from _version import __version__

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
  name='slack2zammad',
  packages=find_packages(),
  version=__version__,
  author='Caspersonn',
  description='Slack App providing a Message Shortcut to create Zammad ticket from Slack message',
  install_requires=install_requires,
  scripts=['_version.py'],
  py_modules=['app'],
  entry_points={
    'console_scripts': ['slack2zammad = app:main']
  },
)

