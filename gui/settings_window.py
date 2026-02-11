#!/usr/bin/env python3
"""
Settings window for Discord Send Guard
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import logging

logger = logging.getLogger(__name__)


class SettingsWindow:
    """Settings window"""

    def __init__(self, config, guard=None, parent=None):
        """
        Initialize settings window

        Args:
            config: Config instance
            guard: DiscordSendGuard instance (optional)
            parent: Parent window (optional)
        """
        self.config = config
        self.guard = guard
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Discord Send Guard - Settings")
        self.window.geometry("600x500")
        self.window.resizable(False, False)

        self._create_widgets()
        self._load_settings()

    def _create_widgets(self):
        """Create window widgets"""
        # Main container
        main_frame = ttk.Frame(self.window, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title = ttk.Label(
            main_frame,
            text="Settings",
            font=('Helvetica', 24, 'bold')
        )
        title.pack(pady=(0, 30))

        # Settings sections
        self._create_general_section(main_frame)
        self._create_autostart_section(main_frame)
        self._create_debug_section(main_frame)
        self._create_permission_section(main_frame)

        # Button container
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, pady=(20, 0))

        # Save button
        save_btn = ttk.Button(
            button_frame,
            text="Save",
            command=self._save_settings
        )
        save_btn.pack(side=tk.LEFT, padx=5)

        # Cancel button
        cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            command=self._cancel
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def _create_general_section(self, parent):
        """Create general settings section"""
        frame = ttk.LabelFrame(parent, text="General", padding="15")
        frame.pack(fill=tk.X, pady=10)

        # Enabled checkbox
        self.enabled_var = tk.BooleanVar()
        enabled_check = ttk.Checkbutton(
            frame,
            text="Enable Discord Send Guard",
            variable=self.enabled_var
        )
        enabled_check.pack(anchor=tk.W, pady=5)

        # Description
        desc = ttk.Label(
            frame,
            text="When enabled, Enter key will create a new line instead of sending messages in Discord.",
            wraplength=500,
            font=('Helvetica', 10)
        )
        desc.pack(anchor=tk.W, pady=(0, 5))

    def _create_autostart_section(self, parent):
        """Create auto-start settings section"""
        frame = ttk.LabelFrame(parent, text="Auto-Start", padding="15")
        frame.pack(fill=tk.X, pady=10)

        # Autostart checkbox
        self.autostart_var = tk.BooleanVar()
        autostart_check = ttk.Checkbutton(
            frame,
            text="Start automatically on login",
            variable=self.autostart_var
        )
        autostart_check.pack(anchor=tk.W, pady=5)

        # Description
        desc = ttk.Label(
            frame,
            text="Discord Send Guard will start automatically when you log in to macOS.",
            wraplength=500,
            font=('Helvetica', 10)
        )
        desc.pack(anchor=tk.W, pady=(0, 5))

    def _create_debug_section(self, parent):
        """Create debug settings section"""
        frame = ttk.LabelFrame(parent, text="Debug", padding="15")
        frame.pack(fill=tk.X, pady=10)

        # Debug checkbox
        self.debug_var = tk.BooleanVar()
        debug_check = ttk.Checkbutton(
            frame,
            text="Enable debug logging",
            variable=self.debug_var
        )
        debug_check.pack(anchor=tk.W, pady=5)

        # Description
        desc = ttk.Label(
            frame,
            text="Show detailed logs for troubleshooting. Check ~/Library/Logs/com.ideaccept.discord-send-guard.log",
            wraplength=500,
            font=('Helvetica', 10)
        )
        desc.pack(anchor=tk.W, pady=(0, 5))

    def _create_permission_section(self, parent):
        """Create permission check section"""
        frame = ttk.LabelFrame(parent, text="Permissions", padding="15")
        frame.pack(fill=tk.X, pady=10)

        # Permission status
        self.permission_label = ttk.Label(
            frame,
            text="Checking...",
            font=('Helvetica', 10)
        )
        self.permission_label.pack(anchor=tk.W, pady=5)

        # Action buttons
        button_container = ttk.Frame(frame)
        button_container.pack(anchor=tk.W, pady=(10, 0))

        check_btn = ttk.Button(
            button_container,
            text="Check Permission",
            command=self._check_permission
        )
        check_btn.pack(side=tk.LEFT, padx=(0, 5))

        guide_btn = ttk.Button(
            button_container,
            text="Show Guide",
            command=self._show_permission_guide
        )
        guide_btn.pack(side=tk.LEFT)

        # Initial permission check
        self._check_permission()

    def _load_settings(self):
        """Load current settings"""
        self.enabled_var.set(self.config.enabled)
        self.autostart_var.set(self.config.autostart)
        self.debug_var.set(self.config.debug)

    def _check_permission(self):
        """Check accessibility permission"""
        try:
            from utils.permissions import check_accessibility_permission

            granted = check_accessibility_permission()

            if granted:
                self.permission_label.config(
                    text="✓ Accessibility permission granted",
                    foreground="green"
                )
            else:
                self.permission_label.config(
                    text="✗ Accessibility permission required",
                    foreground="orange"
                )

        except Exception as e:
            logger.error(f"Failed to check permission: {e}")
            self.permission_label.config(
                text="⚠ Unable to check permission",
                foreground="red"
            )

    def _show_permission_guide(self):
        """Show permission guide"""
        try:
            from gui.permission_guide import show_permission_guide
            show_permission_guide(parent=self.window, on_complete=self._check_permission)
        except Exception as e:
            logger.error(f"Failed to show permission guide: {e}")
            messagebox.showerror("Error", f"Failed to open guide: {e}")

    def _save_settings(self):
        """Save settings"""
        try:
            # Update config
            self.config.enabled = self.enabled_var.get()
            self.config.debug = self.debug_var.get()

            # Handle autostart
            new_autostart = self.autostart_var.get()
            if new_autostart != self.config.autostart:
                from utils.autostart import toggle_autostart
                if toggle_autostart(new_autostart):
                    self.config.autostart = new_autostart
                else:
                    messagebox.showwarning(
                        "Warning",
                        "Failed to update auto-start setting"
                    )

            # Update guard debug level if available
            if self.guard:
                if self.config.debug:
                    logging.getLogger().setLevel(logging.DEBUG)
                else:
                    logging.getLogger().setLevel(logging.INFO)

            messagebox.showinfo("Success", "Settings saved successfully")
            self.window.destroy()

        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
            messagebox.showerror("Error", f"Failed to save settings: {e}")

    def _cancel(self):
        """Cancel and close window"""
        self.window.destroy()

    def show(self):
        """Show the window"""
        self.window.mainloop()


def show_settings(config, guard=None, parent=None):
    """
    Show settings window

    Args:
        config: Config instance
        guard: DiscordSendGuard instance (optional)
        parent: Parent window (optional)
    """
    settings = SettingsWindow(config, guard, parent)
    if parent:
        # Modal if parent provided
        settings.window.transient(parent)
        settings.window.grab_set()
        parent.wait_window(settings.window)
    else:
        settings.show()


if __name__ == '__main__':
    # For testing
    logging.basicConfig(level=logging.INFO)
    from utils.config import get_config
    config = get_config()
    show_settings(config)
