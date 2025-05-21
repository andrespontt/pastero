
# Pastero

A desktop application built with Python and CustomTkinter to simplify text manipulation and copying.

## Features

- **Text Area with Line Numbers**: Easy-to-use text editor with line number indicators
- **Copy Line Feature**: Click on any line number to copy that specific line
  - Hover tooltip shows copy functionality
  - Visual feedback with hand cursor
  - Status bar shows what was copied
- **Text Operations**:
  - Trim Text: Removes leading and trailing whitespace
  - Clear: Quick way to clear all content
- **Auto-scroll Sync**: Line numbers sync with text area scrolling
- **Dark Mode**: Modern dark theme interface

## Download

You can download the latest executable from the `dist` folder:
- Windows: [Pastero.exe](dist/Pastero.exe)

## Development Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python src/main.py`

## Building from Source

To create an executable:
1. Install PyInstaller: `pip install pyinstaller`
2. Run build script: `python build.py`
3. Find the executable in `dist/Pastero.exe`

## Project Structure
```
pastero/
├── src/              # Source code
│   ├── __init__.py
│   ├── main.py      # Main application
│   └── utils/       # Utility functions
├── tests/           # Test files
├── dist/            # Compiled executables
├── docs/            # Documentation
├── build.py         # Build script
└── README.md
```

## Usage

Just run the application and start pasting your text. Use the buttons at the bottom to trim or clear text as needed.
