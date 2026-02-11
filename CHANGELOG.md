# Changelog

All notable changes to Discord Send Guard will be documented in this file.

## [2.0.0] - 2025-02-11

### Added - Major GUI Upgrade

#### Menu Bar Application
- Integrated rumps for native macOS menu bar support
- Menu bar icon with shield design
- Always-on background operation
- LSUIElement enabled (no dock icon, menu bar only)
- Menu items:
  - Status display (Enabled/Disabled)
  - Enable/Disable toggle
  - Settings window access
  - Permission guide access
  - View logs in Console.app
  - About information
  - Quit option

#### Setup Wizard
- Complete first-run setup experience using tkinter
- 4-page wizard flow:
  1. Welcome page with app introduction
  2. Accessibility permission setup with guide
  3. Auto-start configuration
  4. Completion confirmation
- Automatic launch on first run
- Never shows again after completion

#### GUI Components
- **Settings Window**: Full GUI for configuration
  - Enable/disable toggle
  - Auto-start configuration
  - Debug logging toggle
  - Permission status check
  - Access to permission guide
- **Permission Guide**: Step-by-step visual instructions
  - 4 detailed guide images
  - Interactive "Open System Settings" button
  - "Check Permission" verification
  - Previous/Next navigation
- **All windows use tkinter** (Python standard library)

#### Auto-Start System
- LaunchAgent plist generation
- Configurable via setup wizard or settings
- Install/uninstall functionality
- Located at `~/Library/LaunchAgents/com.ideaccept.discord-send-guard.plist`
- Automatic management through utils/autostart.py

#### Configuration Management
- JSON-based configuration in `~/.discord-send-guard/config.json`
- Configuration fields:
  - `enabled`: Guard on/off state
  - `autostart`: Auto-start on login
  - `debug`: Debug logging level
  - `first_run`: First-run wizard flag
- Persistent across app restarts
- GUI and programmatic access

#### Assets & Icons
- Shield icon design for menu bar (22x22)
- High-resolution app icon (512x512)
- macOS .icns bundle icon
- Programmatically generated with Pillow
- 4 guide images for permission setup
- All images generated via scripts (no manual screenshots)

#### Build System
- Complete py2app integration
- Setup.py configured for .app bundling
- Includes all dependencies (rumps, pynput, tkinter, Pillow)
- Bundles assets (icons, guide images)
- Creates standalone macOS application
- App metadata in Info.plist

#### Documentation
- Completely rewritten README.md with GUI instructions
- New BUILD.md with build and distribution guide
- UPGRADE_COMPLETE.md with detailed upgrade summary
- CHANGELOG.md (this file)

#### Utilities
- `utils/config.py`: Configuration management class
- `utils/permissions.py`: Accessibility permission checking
- `utils/autostart.py`: LaunchAgent management
- `utils/generate_guide_images.py`: Guide image generation
- `utils/generate_icons.py`: App icon generation

#### Logging
- Enhanced logging to `~/Library/Logs/com.ideaccept.discord-send-guard.log`
- Console output in development mode
- Configurable debug level
- Log viewer integration (opens in Console.app)

#### Dependencies
- Added `rumps>=0.4.0` for menu bar app
- Added `Pillow>=10.0.0` for image generation
- Added `py2app>=0.28.0` for app bundling
- Existing: pynput, pyobjc-framework-Cocoa, pytest

### Changed

- Upgraded from v1.0.0 CLI tool to v2.0.0 GUI app
- Primary interface now menu bar app (run with `python app.py`)
- CLI mode still available via `python run.py` (backward compatible)
- README.md completely rewritten for GUI workflow
- Project structure expanded with gui/ and utils/ directories
- setup.py updated with py2app configuration

### Maintained

- Core `discord_send_guard.py` logic **unchanged**
- Same keyboard interception behavior
- Same Discord window detection
- CLI mode fully functional (backward compatible)
- All existing tests still valid
- Same key mapping:
  - Enter → New line (no send)
  - Cmd+Enter → Send message

### Technical Details

- Python 3.7+ required
- macOS 10.13+ required
- Accessibility permissions required (guided setup)
- No network connectivity needed
- Local-only operation
- No keylogging or data collection

## [1.0.0] - 2025-02-10

### Added

- Initial release
- CLI tool for Discord send prevention
- Keyboard hook using pynput
- Window detection (macOS and Windows)
- Enter key interception in Discord
- Cmd+Enter (Mac) / Ctrl+Enter (Win) for sending
- Debug mode
- Basic README and tests

### Features

- Prevents accidental Discord message sends
- Swaps Enter and Cmd/Ctrl+Enter behavior
- Cross-platform support (macOS, Windows)
- Zero configuration needed
- No GUI - runs in terminal

---

## Version Format

This project follows [Semantic Versioning](https://semver.org/):

- MAJOR version for incompatible API changes
- MINOR version for added functionality (backward compatible)
- PATCH version for backward compatible bug fixes

## Links

- [GitHub Repository](https://github.com/asakai2626/discord-send-guard)
- [Issue Tracker](https://github.com/asakai2626/discord-send-guard/issues)
