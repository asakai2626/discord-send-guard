#!/usr/bin/env python3
"""
LaunchAgent management for macOS auto-start
"""

import os
import platform
import subprocess
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

IS_MAC = platform.system() == 'Darwin'

# LaunchAgent configuration
LAUNCHAGENT_LABEL = "com.ideaccept.discord-send-guard"
LAUNCHAGENT_DIR = Path.home() / "Library" / "LaunchAgents"
LAUNCHAGENT_PLIST = LAUNCHAGENT_DIR / f"{LAUNCHAGENT_LABEL}.plist"


def get_app_path() -> str:
    """
    Get the path to the application

    Returns:
        Path to the app or Python script
    """
    # Check if we're running from a .app bundle
    if getattr(sys, 'frozen', False):
        # Running from py2app bundle
        return os.path.dirname(sys.executable)
    else:
        # Running from source - point to app.py
        current_dir = Path(__file__).parent.parent
        return str(current_dir / "app.py")


def create_launchagent_plist(app_path: str = None) -> str:
    """
    Create LaunchAgent plist content

    Args:
        app_path: Path to the application (auto-detected if None)

    Returns:
        plist XML content as string
    """
    import sys

    if app_path is None:
        app_path = get_app_path()

    # Get Python executable path
    python_path = sys.executable

    # Determine if we're running from source or .app
    if app_path.endswith('.app') or '/Contents/' in app_path:
        # .app bundle
        program_args = [app_path]
    else:
        # Source - use python to run app.py
        program_args = [python_path, app_path]

    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{LAUNCHAGENT_LABEL}</string>

    <key>ProgramArguments</key>
    <array>
        {''.join(f'<string>{arg}</string>\n        ' for arg in program_args)}
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <false/>

    <key>StandardOutPath</key>
    <string>{Path.home()}/Library/Logs/{LAUNCHAGENT_LABEL}.log</string>

    <key>StandardErrorPath</key>
    <string>{Path.home()}/Library/Logs/{LAUNCHAGENT_LABEL}.error.log</string>

    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
"""
    return plist_content


def is_autostart_enabled() -> bool:
    """
    Check if autostart is enabled

    Returns:
        True if LaunchAgent plist exists, False otherwise
    """
    if not IS_MAC:
        logger.warning("Autostart only supported on macOS")
        return False

    return LAUNCHAGENT_PLIST.exists()


def enable_autostart(app_path: str = None) -> bool:
    """
    Enable autostart by creating LaunchAgent plist

    Args:
        app_path: Path to the application (auto-detected if None)

    Returns:
        True if successful, False otherwise
    """
    if not IS_MAC:
        logger.warning("Autostart only supported on macOS")
        return False

    try:
        # Ensure LaunchAgents directory exists
        LAUNCHAGENT_DIR.mkdir(parents=True, exist_ok=True)

        # Create plist content
        plist_content = create_launchagent_plist(app_path)

        # Write plist file
        with open(LAUNCHAGENT_PLIST, 'w', encoding='utf-8') as f:
            f.write(plist_content)

        logger.info(f"Created LaunchAgent plist: {LAUNCHAGENT_PLIST}")

        # Load the LaunchAgent
        subprocess.run([
            'launchctl', 'load', str(LAUNCHAGENT_PLIST)
        ], check=True)

        logger.info("LaunchAgent loaded successfully")
        return True

    except Exception as e:
        logger.error(f"Failed to enable autostart: {e}")
        return False


def disable_autostart() -> bool:
    """
    Disable autostart by removing LaunchAgent plist

    Returns:
        True if successful, False otherwise
    """
    if not IS_MAC:
        logger.warning("Autostart only supported on macOS")
        return False

    try:
        if not LAUNCHAGENT_PLIST.exists():
            logger.info("LaunchAgent plist does not exist")
            return True

        # Unload the LaunchAgent
        try:
            subprocess.run([
                'launchctl', 'unload', str(LAUNCHAGENT_PLIST)
            ], check=True)
            logger.info("LaunchAgent unloaded successfully")
        except subprocess.CalledProcessError:
            # May fail if not loaded - that's okay
            logger.warning("LaunchAgent was not loaded")

        # Remove plist file
        LAUNCHAGENT_PLIST.unlink()
        logger.info(f"Removed LaunchAgent plist: {LAUNCHAGENT_PLIST}")
        return True

    except Exception as e:
        logger.error(f"Failed to disable autostart: {e}")
        return False


def toggle_autostart(enable: bool, app_path: str = None) -> bool:
    """
    Enable or disable autostart

    Args:
        enable: True to enable, False to disable
        app_path: Path to the application (auto-detected if None)

    Returns:
        True if successful, False otherwise
    """
    if enable:
        return enable_autostart(app_path)
    else:
        return disable_autostart()


import sys
