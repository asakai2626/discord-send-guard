#!/usr/bin/env python3
"""
Accessibility permissions checker for macOS
"""

import platform
import subprocess
import logging

logger = logging.getLogger(__name__)

IS_MAC = platform.system() == 'Darwin'


def check_accessibility_permission() -> bool:
    """
    Check if the app has accessibility permissions on macOS

    Returns:
        True if permissions are granted, False otherwise
    """
    if not IS_MAC:
        logger.warning("Accessibility permission check only available on macOS")
        return True  # Assume granted on non-macOS

    try:
        # Try to check accessibility permission using Quartz
        from Quartz import CGPreflightScreenCaptureAccess

        # This is a proxy check - if we can access screen capture,
        # we likely have accessibility permissions
        # A more direct check would use AXIsProcessTrusted()
        return check_ax_trusted()
    except ImportError:
        logger.error("Quartz framework not available")
        return False
    except Exception as e:
        logger.error(f"Failed to check accessibility permission: {e}")
        return False


def check_ax_trusted() -> bool:
    """
    Check if the process is trusted for accessibility using AXIsProcessTrusted

    Returns:
        True if trusted, False otherwise
    """
    if not IS_MAC:
        return True

    try:
        from ApplicationServices import AXIsProcessTrusted
        trusted = AXIsProcessTrusted()
        logger.debug(f"Accessibility trusted: {trusted}")
        return trusted
    except ImportError:
        logger.error("ApplicationServices framework not available")
        # Fall back to trying to detect via pynput
        return fallback_permission_check()
    except Exception as e:
        logger.error(f"Failed to check AX trusted: {e}")
        return fallback_permission_check()


def fallback_permission_check() -> bool:
    """
    Fallback method to check permissions by attempting to use pynput

    Returns:
        True if likely granted, False otherwise
    """
    try:
        from pynput import keyboard

        # Try to create a listener - this will work if we have permissions
        listener = keyboard.Listener(on_press=lambda k: None)
        listener.start()
        listener.stop()

        return True
    except Exception as e:
        logger.warning(f"Fallback permission check failed: {e}")
        return False


def request_accessibility_permission():
    """
    Request accessibility permission (opens System Settings on macOS)

    Note: This doesn't directly grant permission, but guides the user
    to the right settings page
    """
    if not IS_MAC:
        logger.warning("Accessibility permission request only available on macOS")
        return

    try:
        # Open System Settings to Privacy & Security > Accessibility
        # Using x-apple.systempreferences URL scheme
        subprocess.run([
            'open',
            'x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility'
        ], check=True)
        logger.info("Opened System Settings for accessibility permission")
    except Exception as e:
        logger.error(f"Failed to open System Settings: {e}")
        # Fallback: just open System Settings
        try:
            subprocess.run(['open', '-a', 'System Settings'], check=True)
        except Exception as e2:
            logger.error(f"Failed to open System Settings (fallback): {e2}")


def open_system_settings():
    """
    Open macOS System Settings app
    """
    if not IS_MAC:
        return

    try:
        subprocess.run(['open', '-a', 'System Settings'], check=True)
        logger.info("Opened System Settings")
    except Exception as e:
        logger.error(f"Failed to open System Settings: {e}")


def get_permission_status_message() -> str:
    """
    Get a user-friendly message about permission status

    Returns:
        Status message string
    """
    if not IS_MAC:
        return "Permission checks not required on this platform"

    if check_accessibility_permission():
        return "✓ Accessibility permissions granted"
    else:
        return "✗ Accessibility permissions required - please grant in System Settings"
