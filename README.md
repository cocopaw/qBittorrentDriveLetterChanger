# qBittorrent Drive Letter Changer

## Overview
The **qBittorrent Drive Letter Changer** (Version 1.0.1) is a Python script (also available as a standalone `.exe`) designed to update the drive letter for multiple torrents with differing save paths in qBittorrent. It addresses a limitation of the qBittorrent GUI’s "Set Location" function, which only supports updating multiple torrents with the same save path.

## Features
- Updates drive letters for torrent save paths in qBittorrent via its WebUI API.
- Option to filter torrent selection by a specific tracker domain.
- Interactive preview of changes before processing.
- Option to processes torrents one at a time or all at once.
- Detailed logging to track actions and errors.
- Ensures qBittorrent is properly configured before proceeding.

## Requirements
- **For Python version**:
  - Python 3.6 or higher
  - `requests` library (`pip install requests`)
- **For executable version**:
  - No Python installation required; use the provided `.exe` file
- qBittorrent with WebUI enabled
- qBittorrent installed on a Windows operating system

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
   - Note the IP address (default '*') and port (default '8080').
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
   - Enter WebUI URL, username, and password (defaults: `http://localhost:8080`, `admin`).
   - Specify the old and new drive letters (e.g., `D:` to `E:`).
   - Choose to filter by a tracker (optional).
   - Select to process a single torrent or all torrents or quit.

4. Tracker Filtering:
- The script allows filtering torrents by tracker domain, matching the behavior of the qBittorrent GUI's "Trackers" section.
- When prompted to filter by tracker:
  - Enter `y` to enable filtering, then input a tracker domain exactly as it appears in the qBittorrent GUI's "Trackers" section.
  - Enter `n` or press Enter to process all torrents, equivalent to the GUI's "All" tracker setting.

5. The program will preview changes and update torrent paths. Logs are saved in the `Logs` directory.

## Behavior
The script's behavior mirrors the "Set Location" function in qBittorrent GUI, equivalent to selecting "Set Location" and changing the drive letter in the address bar for each torrent. Specifically:
- It updates the save path for each torrent and handles the associated torrent data as follows:
  - If the torrent data is already present at the destination location (new drive), the script updates the save path and verifies the data at the new location, leaving the source data in place.
  - If the torrent data is not at the destination location but is present at the source location (old drive), the script moves the data on disk from the source to the destination and deletes the source data.

## Use Cases
The script addresses limitations in the qBittorrent GUI's "Set Location" function and is particularly useful in the following scenarios:
- **Bulk updating torrents with different save paths**: The GUI's "Set Location" function cannot update multiple torrents with different save paths in a single action, requiring users to manually update each torrent individually, which is impractical for large numbers of torrents.
- **Efficient drive migration**: The script allows users to update the drive letter for multiple torrents with varying save paths in a single operation, preserving their original save path structure (e.g., migrating all torrents from `D:` to `E:` regardless of their individual paths). In contrast, the GUI's "Set Location" function only supports moving multiple torrents simultaneously if they share the same save path.
- **Other scenarios**: The script may be used for any situation that calls for updating the drive letter on multiple torrents with varying save paths.

## Example
To change all torrents from drive `D:` to `E:`:
1. Enter WebUI URL: `http://localhost:8080`
2. Enter username: `admin`
3. Enter password: `your_password`
4. Enter old drive: `D:`
5. Enter new drive: `E:`
6. Filter by tracker? (y/n): `n`

## Logs
- Logs are saved in the `Logs` directory with filenames like `qbittorrent_drive_change_YYYY-MM-DD_HH-MM-SS.log`.
- Logs include timestamps, torrent details, and error messages.
- Only critical messages (e.g., errors, successful updates) are printed to the console, while detailed debug and operational logs are recorded in the log file.

## Changelog
See the [`CHANGELOG.md`](./CHANGELOG.md) file for a detailed version history and release notes.

## Important Notes
- **Backup is mandatory**: Always back up qBittorrent data before running the program to prevent data loss.
- **WebUI must be enabled**: Ensure qBittorrent's WebUI is active and accessible.
- **HTTPS Support**: The script supports HTTPS if enabled in qBittorrent (e.g., `https://localhost:8080`) with a valid certificate/key.
- **No warranty**: This program is provided as-is. Use at your own risk. The author is not responsible for any issues or data loss.

## Troubleshooting
- **Authentication Failure**: Verify WebUI URL, username, and password. Ensure qBittorrent is running.
- **No Torrents Found**: Check if torrents match the specified drive letter or tracker.
- **API Errors**: Ensure the WebUI is accessible and not blocked by a firewall.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Disclaimer
This program is not affiliated with qBittorrent. Use it responsibly and ensure you have backups before making changes.