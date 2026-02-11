# Discord Send Guard v2.0 - Build Instructions

## Quick Start (Development)

```bash
# 1. Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the GUI app
python app.py
```

## Building the .app Bundle

### Prerequisites

- macOS 10.13+
- Python 3.7+
- Xcode Command Line Tools (for iconutil)

### Build Steps

```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Build the .app
python setup.py py2app

# 3. The app will be in dist/
ls -la dist/

# 4. Test the app
open dist/Discord\ Send\ Guard.app
```

### Build Output

```
dist/
└── Discord Send Guard.app/
    ├── Contents/
    │   ├── MacOS/
    │   │   └── Discord Send Guard  # Executable
    │   ├── Resources/
    │   │   ├── app_icon.icns       # App icon
    │   │   └── assets/             # Guide images
    │   └── Info.plist              # App metadata
```

## Distribution

### Creating a DMG (Optional)

```bash
# Using hdiutil
hdiutil create -volname "Discord Send Guard" \
  -srcfolder "dist/Discord Send Guard.app" \
  -ov -format UDZO \
  "Discord-Send-Guard-v2.0.dmg"
```

### Code Signing (Optional, for distribution)

```bash
# Sign the app
codesign --deep --force --verify --verbose \
  --sign "Developer ID Application: YOUR_NAME" \
  "dist/Discord Send Guard.app"

# Verify signature
codesign --verify --deep --strict --verbose=2 \
  "dist/Discord Send Guard.app"
```

## Troubleshooting

### "No module named 'rumps'" during build

Make sure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Build fails with "iconutil: command not found"

Install Xcode Command Line Tools:

```bash
xcode-select --install
```

### App doesn't launch after building

Check the Console.app for errors:

```bash
open -a Console
# Look for "Discord Send Guard" entries
```

### Clean build

```bash
# Remove build artifacts
rm -rf build/ dist/

# Rebuild
python setup.py py2app
```

## Development vs. Production

### Development Mode

- Run directly with `python app.py`
- Logs to console and `~/Library/Logs/`
- Easy to debug and modify

### Production Mode (.app)

- Standalone application
- No Python installation required by users
- Logs only to `~/Library/Logs/`
- Menu bar app with LSUIElement (no dock icon)

## File Structure After Build

```
discord-send-guard/
├── build/              # Temporary build files
├── dist/               # Final .app bundle
├── app.py             # Main entry point
├── discord_send_guard.py  # Core logic
├── gui/               # GUI modules
├── utils/             # Utility modules
├── assets/            # Icons and images
├── setup.py           # py2app config
└── requirements.txt   # Dependencies
```

## Testing the Build

1. **Test in development mode first:**
   ```bash
   python app.py
   ```

2. **Build the .app:**
   ```bash
   python setup.py py2app
   ```

3. **Test the .app:**
   ```bash
   open dist/Discord\ Send\ Guard.app
   ```

4. **Verify functionality:**
   - Check menu bar icon appears
   - Test enable/disable toggle
   - Open settings window
   - Check permission guide
   - Verify Discord key interception works

## Known Issues

### py2app and Python 3.14+

If you encounter issues with Python 3.14, try Python 3.11 or 3.12:

```bash
# Using pyenv
pyenv install 3.12
pyenv local 3.12
```

### tkinter Import Errors

Make sure tkinter is included in your Python installation:

```bash
# Check tkinter
python -m tkinter
```

On macOS, tkinter should be included with the official Python.org installer.

## Version History

- **v2.0.0** - GUI menu bar app with setup wizard
- **v1.0.0** - CLI tool

## Support

For issues, see:
- [GitHub Issues](https://github.com/asakai2626/discord-send-guard/issues)
- README.md
- UPGRADE_REQUIREMENTS.md
