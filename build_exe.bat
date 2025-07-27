@echo off
echo Building portable executable for qBittorrentDriveLetterChanger.py...

:: Ensure PyInstaller is installed
pip install pyinstaller requests

:: Run PyInstaller to create a single executable in the root directory
pyinstaller --onefile --name qBittorrentDriveLetterChanger --distpath . qBittorrentDriveLetterChanger.py

echo.
echo Build complete! The executable is located in the root directory as 'qBittorrentDriveLetterChanger.exe'.
pause