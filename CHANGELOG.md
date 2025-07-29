# Changelog

All notable changes to the qBittorrent Drive Letter Changer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2025-07-29

### Added
- Notification for successful WebUI connection: "Authentication successful. Connected to qBittorrent WebUI." displayed after successful authentication.
- Enhanced error handling for WebUI URL validation, checking if the URL is contactable before proceeding.
- Looping mechanism to return to drive letter and tracker selection prompts if no torrents match the specified criteria, instead of exiting the script.

### Changed
- Simplified input prompts for better clarity and conciseness:
  - Drive letter prompts updated to "Enter old drive letter: " and "Enter new drive letter: ".
  - WebUI prompts updated to "Enter WebUI URL [http://localhost:8080]: " and "Enter WebUI username [admin]: ".
  - Tracker filter prompt updated to "Filter by tracker? (y/n) [n]: " and "Enter tracker domain from 'Trackers' section in GUI (Enter for 'All'): ".
- Updated WebUI setup instructions to clarify noting the IP address (default '*') and port (default 8080), using 'localhost' for local access.
- Improved authentication failure handling to request re-entry of username and password only, without requiring re-entry of the WebUI URL.
- Enhanced logging to exclude non-critical messages (e.g., debug, filtered torrents, authentication attempts) from console output, improving user experience.
- Added data handling behavior explanation in the script's welcome message, clarifying that data is verified if present at the new drive or moved from the old drive if not.
- Added support for HTTPS in WebUI URL validation.

### Fixed
- Minor formatting improvements in console output, such as consistent blank lines before prompts and previews for better readability.

## [1.0] - 2025-07-27

### Added
- Initial release of qBittorrent Drive Letter Changer.
- Functionality to update drive letters for torrents in qBittorrent via the WebUI API.
- Support for filtering torrents by a specific tracker domain.
- Logging system to record operations and errors in a `Logs` directory.
- Interactive CLI interface with options to process single torrents or all torrents.
- Validation for drive letter inputs (e.g., requires format like `D:`).
- Preview of changes before processing each torrent.
- Automatic re-authentication with qBittorrent WebUI to handle session expiration.
- Backup warning and WebUI setup instructions for user safety.

[Unreleased]: https://github.com/cocopaw/qBittorrentDriveLetterChanger/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/cocopaw/qBittorrentDriveLetterChanger/compare/v1.0...v1.0.1
[1.0]: https://github.com/cocopaw/qBittorrentDriveLetterChanger/releases/tag/v1.0