import requests
import json
import time
import datetime
import sys
import os

# Create Logs directory if it doesn't exist
LOGS_DIR = "Logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Generate timestamp for log filename
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = os.path.join(LOGS_DIR, f"qbittorrent_drive_change_{timestamp}.log")

# Function to log messages to file only (no CLI for debug or filtered torrents)
def log_message(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
    # Only print non-debug, non-filtered torrent, non-user choice, non-authentication, non-update, non-process completed, and non-logout messages to CLI
    if not message.startswith("Debug:") and not message.startswith("Filtered torrent:") and not message.startswith("Torrents API call initiated") and not message.startswith("Torrents data retrieved") and not message.startswith("Found") and not message.startswith("Preview:") and not message.startswith("Script started") and not message.startswith("User chose") and not message.startswith("Attempting to authenticate") and not message.startswith("Authentication") and not message.startswith("Updated:") and not message.startswith("Process completed") and not message.startswith("Logout performed"):
        print(log_entry.strip())

# Function to check appearing tracker in a tracker (single string or list)
def has_target_tracker(tracker, target_tracker):
    if not tracker or not target_tracker:
        return False
    if isinstance(tracker, str):
        log_message(f"Debug: Checking tracker: {tracker}")
        return target_tracker.lower() in tracker.lower()
    return False

# Function to get ordinal suffix for numbers (e.g., 1st, 2nd, 3rd, 4th)
def get_ordinal_suffix(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"

# Function to validate drive letter input (must end with colon)
def validate_drive_letter(prompt):
    while True:
        drive = input(prompt).strip().upper()
        if drive and drive.endswith(':') and len(drive) == 2 and drive[0].isalpha():
            return drive
        print("Invalid drive letter. Please enter a single letter followed by a colon (e.g. 'E:')")

# Function to process a single torrent
def process_torrent(torrent, torrent_list):
    hash = torrent["hash"]
    old_path = torrent["save_path"]
    torrent_name = torrent.get("name", "Unnamed Torrent")
    new_path = NEW_DRIVE + old_path[len(OLD_DRIVE):]
    
    # Ensure session is still valid
    if not authenticate():
        print("Session expired. Unable to continue. Please restart the script.")
        sys.exit(1)

    # Set location with proper form data
    data = {"hashes": hash, "location": new_path}
    try:
        response = session.post(f"{WEBUI_URL}/api/v2/torrents/setLocation", data=data, timeout=10)
        if response.status_code == 200:
            log_message(f"Updated: {old_path} -> {new_path}")
            print(f"Updated torrent \"{torrent_name}\" successfully")
            torrent_list.remove(torrent)  # Remove processed torrent from list
        else:
            log_message(f"Failed to update {torrent_name}: HTTP {response.status_code} - {response.text}")
            print(f"Failed to update {torrent_name}: HTTP {response.status_code}")
    except Exception as e:
        log_message(f"Error updating {torrent_name}: {str(e)}")
        print(f"Error updating {torrent_name}: {str(e)}")

    time.sleep(0.1)  # Small delay to avoid overwhelming the API

# Add blank line before welcome message
print()

# Welcome message
print("""
Welcome to the qBittorrent Drive Letter Changer! (Version 1.0)
This script updates the Windows drive letter on one or more torrents in qBittorrent.  
All torrents are selected by default. Alternately torrents belonging to a single tracker can be specified.
      
Logs will be saved to: {}
""".format(os.path.join(LOGS_DIR, "qbittorrent_drive_change_*.log")).strip())
log_message("Script started")

# Warranty disclaimer and backup warning
print("""
*** IMPORTANT NOTICE ***
This script is provided as-is, without any warranty. Use it at your own risk.
The author bears no responsibility for any issues, data loss, or damage caused by running this script.

*** BACKUP REQUIRED ***
Before proceeding, you must:
1. Shut down qBittorrent completely.
2. Back up the following directories to a safe location.
   This will allow restoration of qBittorrent to its original state if unexpected results occur.

   - C:\\Users\\<username>\\AppData\\Local\\qBittorrent
   - C:\\Users\\<username>\\AppData\\Roaming\\qBittorrent
""")
input("Press Enter when you have shut down qBittorrent and backed up the specified directories...\n")

# Check WebUI
print("""
Please ensure qBittorrent is running and WebUI is enabled:
1. Open qBittorrent
2. Go to Tools > Options > Web UI
3. Check 'Web User Interface (Remote control)'
4. Note the IP address (usually '*' or '127.0.0.1') and port (default 8080)
5. Ensure authentication is enabled and note your username/password
""".strip())
print()  # Add blank line before input prompt
input("Press Enter when you have confirmed WebUI is enabled...\n")

# Initialize session
session = requests.Session()

# Function to re-authenticate if session is invalid
def authenticate():
    log_message("Attempting to authenticate with WebUI")
    response = session.post(f"{WEBUI_URL}/api/v2/auth/login", data={"username": USERNAME, "password": PASSWORD}, timeout=10)
    if response.status_code == 200 and response.text.strip() == "Ok.":
        log_message("Authentication successful")
        return True
    else:
        log_message(f"Authentication failed: {response.text.strip()}")
        return False

# Get login credentials with retry loop
while True:
    WEBUI_URL = input("Enter qBittorrent WebUI URL (default: 'http://127.0.0.1:8080', press Enter for default): ").strip() or "http://127.0.0.1:8080"
    USERNAME = input("Enter WebUI username (default: 'admin', press Enter for default): ").strip() or "admin"
    PASSWORD = input("Enter WebUI password: ").strip()
    
    # Test connection and authenticate
    if authenticate():
        break
    print()
    print("Failed to authenticate with qBittorrent WebUI.")
    print("Please check credentials and try again.")
    print()

# Get drive letters and tracker choice
OLD_DRIVE = validate_drive_letter("Enter the drive letter you want to change from (e.g. 'D:'): ")
NEW_DRIVE = validate_drive_letter("Enter the drive letter you want to change to (e.g. 'E:'): ")
use_tracker = input("Filter by specific tracker? 'y'/'n' (default: 'n', press Enter for default): ").strip().lower() in ['y', 'yes']
TARGET_TRACKER = input("Enter tracker domain name to filter by (e.g. domain.com): ").strip() if use_tracker else ""

try:
    # Get all torrents with tracker info
    params = {"extra": "trackers"}
    response = session.get(f"{WEBUI_URL}/api/v2/torrents/info", params=params, headers={"Host": "127.0.0.1:8080"}, timeout=10)
    log_message("Torrents API call initiated")
    if response.status_code != 200:
        log_message(f"Failed to get torrents list: HTTP {response.status_code}")
        raise Exception(f"Failed to get torrents list: HTTP {response.status_code}")
    torrents = json.loads(response.text)
    log_message("Torrents data retrieved")

    # Filter torrents
    filtered_torrents = [t for t in torrents if (not use_tracker or has_target_tracker(t.get("tracker"), TARGET_TRACKER)) and t["save_path"].startswith(OLD_DRIVE)]
    log_message(f"Found {len(filtered_torrents)} torrents to process")
    for torrent in filtered_torrents:
        log_message(f"Filtered torrent: {torrent.get('name', 'Unnamed Torrent')} - {torrent['save_path']}")

    if not filtered_torrents:
        log_message("No torrents found matching criteria")
        print("No torrents found matching your criteria. Exiting.")
        session.get(f"{WEBUI_URL}/api/v2/auth/logout")
        sys.exit(0)

    # Sort torrents by name
    filtered_torrents.sort(key=lambda x: x.get("name", "").lower())

    # Description before preview with torrent count
    print()
    print(f"{len(filtered_torrents)} torrents were found to process.")
    print(f"Changing drive letter from {OLD_DRIVE} to {NEW_DRIVE}.")
    print(f"You can test by changing the drive letter on a single torrents one at a time or process all the torrents.")
    print()  # Line space after description

    # Initialize processed count
    processed_count = 0

    # Preview first torrent with name and path
    print("Preview of changes to the 1st torrent:")
    print()
    torrent = filtered_torrents[0]
    old_path = torrent["save_path"]
    torrent_name = torrent.get("name", "Unnamed Torrent")
    old_full_path = os.path.join(old_path, torrent_name) if torrent_name != "Unnamed Torrent" else old_path
    new_full_path = os.path.join(NEW_DRIVE + old_path[len(OLD_DRIVE):], torrent_name) if torrent_name != "Unnamed Torrent" else NEW_DRIVE + old_path[len(OLD_DRIVE):]
    print(f"Before: {old_full_path}")
    print(f"After: {new_full_path}")

    # Process torrents iteratively
    while filtered_torrents:
        # Ask for confirmation
        while True:
            action = input("\nChoose action: [1] Process the single torrent listed above, [2] Process all torrents, [q] Quit: ").strip().lower()
            if action in ['1', '2', 'q']:
                break
            print("Invalid input. Please enter '1', '2', or 'q'.")
        if action == 'q':
            log_message("User chose to quit")
            print("Exiting without making changes.")
            break
        elif action == '1':
            log_message("User chose to process only the first torrent")
            if 'process_torrent' in globals():
                print()  # Add newline before processing
                process_torrent(filtered_torrents[0], filtered_torrents)
                processed_count += 1
                if filtered_torrents:  # Check if there are more torrents to preview
                    print()
                    print(f"Preview of changes to the {get_ordinal_suffix(processed_count + 1)} torrent:")
                    print()
                    torrent = filtered_torrents[0]
                    old_path = torrent["save_path"]
                    torrent_name = torrent.get("name", "Unnamed Torrent")
                    old_full_path = os.path.join(old_path, torrent_name) if torrent_name != "Unnamed Torrent" else old_path
                    new_full_path = os.path.join(NEW_DRIVE + old_path[len(OLD_DRIVE):], torrent_name) if torrent_name != "Unnamed Torrent" else NEW_DRIVE + old_path[len(OLD_DRIVE):]
                    print(f"Before: {old_full_path}")
                    print(f"After: {new_full_path}")
            else:
                log_message("Function 'process_torrent' not found in global scope")
                print("Error: Function 'process_torrent' is not defined. Please check script integrity.")
                break
        else:
            log_message("User chose to process all torrents")
            if 'process_torrent' in globals():
                for torrent in filtered_torrents[:]:
                    print()  # Add newline before processing
                    process_torrent(torrent, filtered_torrents)
                    processed_count += 1
                    if filtered_torrents:  # Check if there are more torrents to preview
                        print()
                        print(f"Preview of changes to the {get_ordinal_suffix(processed_count + 1)} torrent:")
                        print()
                        torrent = filtered_torrents[0]
                        old_path = torrent["save_path"]
                        torrent_name = torrent.get("name", "Unnamed Torrent")
                        old_full_path = os.path.join(old_path, torrent_name) if torrent_name != "Unnamed Torrent" else old_path
                        new_full_path = os.path.join(NEW_DRIVE + old_path[len(OLD_DRIVE):], torrent_name) if torrent_name != "Unnamed Torrent" else NEW_DRIVE + old_path[len(OLD_DRIVE):]
                        print(f"Before: {old_full_path}")
                        print(f"After: {new_full_path}")
            else:
                log_message("Function 'process_torrent' not found in global scope")
                print("Error: Function 'process_torrent' is not defined. Please check script integrity.")
                break

    # Only display completion message if user didn't quit
    if action != 'q':
        log_message("Process completed")
        print()
        print("Process completed successfully! All torrents moved will be rechecked automatically. Exiting now.")
except Exception as e:
    log_message(f"Error occurred: {str(e)}")
    print(f"Error: {str(e)}")
finally:
    session.get(f"{WEBUI_URL}/api/v2/auth/logout")
    log_message("Logout performed")