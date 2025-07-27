# qBittorrent Drive Letter Changer

## Overview
The **qBittorrent Drive Letter Changer** is a Python script (also available as a standalone `.exe`) designed to update the drive letter for torrent save paths in qBittorrent. It allows users to change the drive letter for all torrents or filter by a specific tracker domain, making it useful for scenarios like migrating torrents to a new drive.

## Features
- Updates drive letters for torrent save paths in qBittorrent via its WebUI API.
- Option to process all torrents or filter by a specific tracker domain.
- Interactive preview of changes before processing.
- Processes torrents one at a time or all at once.
- Detailed logging to track actions and errors.
- Validates user inputs for drive letters and WebUI credentials.
- Ensures qBittorrent is properly configured before proceeding.

## Requirements
- **For Python version**:
  - Python 3.6 or higher
  - `requests` library (`pip install requests`)
- **For executable version**:
  - No Python installation required; use the provided `.exe` file
- qBittorrent with WebUI enabled
- Windows operating system (due to drive letter functionality)

## Installation
1. **Option 1: Using Python**
   - Clone or download this repository.
   - Install the required Python library:
     ```bash
     pip install requests
     ```
2. **Option 2: Using Executable**
   - Download the `qBittorrentDriveLetterChanger.exe` from the releases section.
   - No additional installation is required.
3. Ensure qBittorrent is installed and running with WebUI enabled:
   - Go to **Tools > Options > Web UI** in qBittorrent.
   - Check **Web User Interface (Remote control)**.
   - Note the IP address (usually '*' or '127.0.0.1') and port (default `8080`).
   - Ensure authentication is enabled and note your username/password.

## Usage
1. **Backup qBittorrent Data**:
   - Shut down qBittorrent.
   - Back up the following directories:
     - `C:\Users\<username>\AppData\Local\qBittorrent`
     - `C:\Users\<username>\AppData\Roaming\qBittorrent`
2. Run the program:
   - **Python version**:
     ```bash
     python qBittorrentDriveLetterChanger.py
     ```
   - **Executable version**:
     - Double-click `qBittorrentDriveLetterChanger.exe` or run it from the command prompt.
3. Follow the prompts:
   - Confirm qBittorrent has been backed up.
   - Verify WebUI settings.
   - Enter WebUI URL, username, and password (defaults: `http://127.0.0.1:8080`, `admin`).
   - Specify the old and new drive letters (e.g., `D:` to `E:`).
   - Choose to filter by a tracker (optional).
   - Select to process a single torrent or all torrents, or quit.
4. The program will preview changes and update torrent paths. Logs are saved in the `Logs` directory.

## Example
To change all torrents from drive `D:` to `E:`:
1. Enter WebUI URL: `http://127.0.0.1:8080`
2. Enter username: `admin`
3. Enter password: `your_password`
4. Enter old drive: `D:`
5. Enter new drive: `E:`
6. Choose to process all torrents.

## Logs
- Logs are saved in the `Logs` directory with filenames like `qbittorrent_drive_change_YYYY-MM-DD_HH-MM-SS.log`.
- Logs include timestamps, torrent details, and error messages.
- Only critical messages (e.g., errors, updates) are printed to the console.

## Important Notes
- **Backup is mandatory**: Always back up qBittorrent data before running the program to prevent data loss.
- **WebUI must be enabled**: Ensure qBittorrent's WebUI is active and accessible.
- **No warranty**: This program is provided as-is. Use at your own risk. The author is not responsible for any issues or data loss.

## Troubleshooting
- **Authentication Failure**: Verify WebUI URL, username, and password. Ensure qBittorrent is running.
- **No Torrents Found**: Check if torrents match the specified drive letter or tracker.
- **API Errors**: Ensure the WebUI is accessible and not blocked by a firewall.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Disclaimer
This program is not affiliated with qBittorrent. Use it responsibly and ensure you have backups before making changes.