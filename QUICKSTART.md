# Discord Send Guard v2.0 - Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies

```bash
cd discord-send-guard
source .venv/bin/activate  # Virtual environment should already exist
pip install -r requirements.txt
```

### 2. Launch the App

```bash
python app.py
```

### 3. Follow Setup Wizard

On first run, you'll see a setup wizard that guides you through:

1. **Welcome** - Learn what the app does
2. **Permissions** - Set up accessibility permissions (required)
3. **Auto-Start** - Choose if you want auto-start on login
4. **Complete** - You're ready to go!

---

## 📋 What Happens Next

After completing the setup:

1. **Menu Bar Icon** - Look for the 🛡️ icon in your menu bar
2. **The app is running** - It's now protecting you from accidental sends
3. **Test it** - Open Discord and try pressing Enter (it should create a new line!)

---

## 🎯 How to Use

### In Discord

- **Press Enter** → Creates a new line (doesn't send)
- **Press Cmd+Enter** → Sends your message

### Menu Bar Controls

Click the 🛡️ icon in the menu bar:

- **Enable/Disable** - Turn protection on/off
- **Settings...** - Open settings window
- **Permission Guide...** - View permission setup guide again
- **View Logs** - Open logs in Console.app
- **Quit** - Exit the app

---

## ⚙️ Configuration

### Settings Window

Access via menu bar icon → Settings:

- ✅ Enable/Disable Discord Send Guard
- ✅ Start automatically on login
- ✅ Enable debug logging
- ✅ Check permissions

### Config File

Located at: `~/.discord-send-guard/config.json`

```json
{
  "enabled": true,
  "autostart": false,
  "debug": false,
  "first_run": false
}
```

---

## 🔧 Accessibility Permissions (macOS)

The app needs accessibility permissions to intercept keyboard input.

### Quick Setup

1. Click **Permission Guide...** from menu bar icon
2. Follow the 4-step visual guide
3. Click **Check Permission** to verify

### Manual Setup

1. Open **System Settings**
2. Go to **Privacy & Security** → **Accessibility**
3. Click 🔒 and authenticate
4. Click **+** and add your Python or the app
5. Enable the checkbox
6. **Restart the app**

---

## 🏗️ Build Standalone App (Optional)

Want a double-click .app?

```bash
# Build
python setup.py py2app

# The app will be in dist/
open dist/Discord\ Send\ Guard.app
```

The built .app:
- ✅ Runs without Python installed
- ✅ No terminal window
- ✅ Can be moved to Applications folder
- ✅ Starts from menu bar only (no dock icon)

---

## 🐛 Troubleshooting

### "Operation not permitted" error

→ Accessibility permissions not granted. Follow the permission guide.

### Enter key doesn't work

1. Check menu bar icon shows "✓ Enabled"
2. Make sure Discord is the active window
3. Enable debug logging in Settings
4. Check logs: **View Logs** from menu bar

### Setup wizard doesn't appear

The wizard only shows once. To see it again:

```bash
# Delete config
rm ~/.discord-send-guard/config.json

# Restart app
python app.py
```

### Menu bar icon doesn't appear

1. Check for errors in terminal
2. Make sure rumps is installed: `pip install rumps`
3. Check Python version: `python --version` (needs 3.7+)

---

## 📚 More Documentation

- **README.md** - Full documentation
- **BUILD.md** - Build and distribution guide
- **UPGRADE_COMPLETE.md** - Complete upgrade details
- **CHANGELOG.md** - Version history

---

## ✨ Features Overview

### What It Does
- Prevents accidental Discord message sends
- Swaps Enter and Cmd+Enter behavior in Discord
- Only affects Discord (other apps work normally)

### What's New in v2.0
- 🎯 Menu bar app (always running)
- 🎨 GUI setup wizard
- ⚙️ Settings window
- 📖 Permission guide with images
- 🚀 Auto-start on login
- 📦 Standalone .app bundle

### Security & Privacy
- ✅ No keylogging
- ✅ No network activity
- ✅ Only monitors Discord windows
- ✅ All processing happens locally
- ✅ Open source (check the code!)

---

## 🆘 Need Help?

- Check **README.md** for detailed docs
- View **logs**: Menu bar → View Logs
- Enable **debug mode**: Settings → Enable debug logging
- Report issues: [GitHub Issues](https://github.com/asakai2626/discord-send-guard/issues)

---

## 🎉 You're All Set!

Discord Send Guard v2.0 is now protecting you from accidental sends.

**Enjoy safer Discord messaging!** 🛡️
