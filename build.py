
import PyInstaller.__main__
import sys
import os

PyInstaller.__main__.run([
    'src/main.py',
    '--onefile',
    '--windowed',
    '--name=Pastero',
    '--add-data=README.md:.',
    '--icon=docs/icon.ico',
])
