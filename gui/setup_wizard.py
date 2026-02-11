#!/usr/bin/env python3
"""
Setup wizard for first-run experience
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class SetupWizard:
    """First-run setup wizard"""

    def __init__(self, config, on_complete=None):
        """
        Initialize setup wizard

        Args:
            config: Config instance
            on_complete: Callback when setup is complete
        """
        self.config = config
        self.on_complete = on_complete
        self.window = tk.Tk()
        self.window.title("Discord Send Guard - Setup Wizard")
        self.window.geometry("700x600")
        self.window.resizable(False, False)

        self.current_page = 0
        self.pages = []

        self._create_pages()
        self._show_page(0)

    def _create_pages(self):
        """Create wizard pages"""
        # Page 1: Welcome
        self.pages.append(self._create_welcome_page)
        # Page 2: Accessibility Permission
        self.pages.append(self._create_permission_page)
        # Page 3: Auto-start
        self.pages.append(self._create_autostart_page)
        # Page 4: Complete
        self.pages.append(self._create_complete_page)

    def _clear_window(self):
        """Clear all widgets from window"""
        for widget in self.window.winfo_children():
            widget.destroy()

    def _create_welcome_page(self):
        """Create welcome page"""
        self._clear_window()

        frame = ttk.Frame(self.window, padding="40")
        frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title = ttk.Label(
            frame,
            text="Welcome to Discord Send Guard!",
            font=('Helvetica', 28, 'bold')
        )
        title.pack(pady=(40, 20))

        # Icon (text-based)
        icon = ttk.Label(
            frame,
            text="🛡️",
            font=('Helvetica', 72)
        )
        icon.pack(pady=20)

        # Description
        desc = ttk.Label(
            frame,
            text="Discord Send Guard prevents accidental message sends in Discord.\n\n"
                 "• Enter key = New line (no send)\n"
                 "• Cmd+Enter = Send message\n\n"
                 "Let's get you set up in just a few steps!",
            font=('Helvetica', 14),
            justify=tk.CENTER,
            wraplength=600
        )
        desc.pack(pady=30)

        # Navigation buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(side=tk.BOTTOM, pady=20)

        next_btn = ttk.Button(
            button_frame,
            text="Get Started →",
            command=self._next_page
        )
        next_btn.pack()

    def _create_permission_page(self):
        """Create permission setup page"""
        self._clear_window()

        frame = ttk.Frame(self.window, padding="40")
        frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title = ttk.Label(
            frame,
            text="Accessibility Permission Required",
            font=('Helvetica', 24, 'bold')
        )
        title.pack(pady=(20, 20))

        # Description
        desc = ttk.Label(
            frame,
            text="Discord Send Guard needs accessibility permission to intercept keyboard input.\n\n"
                 "This permission allows the app to detect when you press Enter in Discord.\n\n"
                 "Your privacy is protected - we only monitor Discord windows.",
            font=('Helvetica', 12),
            justify=tk.CENTER,
            wraplength=600
        )
        desc.pack(pady=20)

        # Permission status
        self.permission_status_label = ttk.Label(
            frame,
            text="",
            font=('Helvetica', 12, 'bold')
        )
        self.permission_status_label.pack(pady=10)

        # Action buttons
        action_frame = ttk.Frame(frame)
        action_frame.pack(pady=20)

        open_guide_btn = ttk.Button(
            action_frame,
            text="📖 Show Step-by-Step Guide",
            command=self._show_permission_guide
        )
        open_guide_btn.pack(pady=5)

        check_btn = ttk.Button(
            action_frame,
            text="🔄 Check Permission",
            command=self._check_permission
        )
        check_btn.pack(pady=5)

        # Initial permission check
        self._check_permission()

        # Navigation buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(side=tk.BOTTOM, pady=20)

        back_btn = ttk.Button(
            button_frame,
            text="← Back",
            command=self._prev_page
        )
        back_btn.pack(side=tk.LEFT, padx=5)

        self.permission_next_btn = ttk.Button(
            button_frame,
            text="Next →",
            command=self._next_page
        )
        self.permission_next_btn.pack(side=tk.LEFT, padx=5)

    def _create_autostart_page(self):
        """Create auto-start configuration page"""
        self._clear_window()

        frame = ttk.Frame(self.window, padding="40")
        frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title = ttk.Label(
            frame,
            text="Auto-Start on Login",
            font=('Helvetica', 24, 'bold')
        )
        title.pack(pady=(40, 20))

        # Icon
        icon = ttk.Label(
            frame,
            text="🚀",
            font=('Helvetica', 72)
        )
        icon.pack(pady=20)

        # Description
        desc = ttk.Label(
            frame,
            text="Would you like Discord Send Guard to start automatically when you log in?\n\n"
                 "This ensures your Discord is always protected from accidental sends.",
            font=('Helvetica', 12),
            justify=tk.CENTER,
            wraplength=600
        )
        desc.pack(pady=30)

        # Checkbox
        self.autostart_var = tk.BooleanVar(value=True)
        autostart_check = ttk.Checkbutton(
            frame,
            text="Start Discord Send Guard automatically on login",
            variable=self.autostart_var,
            style='Large.TCheckbutton'
        )
        autostart_check.pack(pady=20)

        # Navigation buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(side=tk.BOTTOM, pady=20)

        back_btn = ttk.Button(
            button_frame,
            text="← Back",
            command=self._prev_page
        )
        back_btn.pack(side=tk.LEFT, padx=5)

        next_btn = ttk.Button(
            button_frame,
            text="Next →",
            command=self._next_page
        )
        next_btn.pack(side=tk.LEFT, padx=5)

    def _create_complete_page(self):
        """Create completion page"""
        self._clear_window()

        frame = ttk.Frame(self.window, padding="40")
        frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title = ttk.Label(
            frame,
            text="Setup Complete!",
            font=('Helvetica', 28, 'bold')
        )
        title.pack(pady=(40, 20))

        # Icon
        icon = ttk.Label(
            frame,
            text="✅",
            font=('Helvetica', 72)
        )
        icon.pack(pady=20)

        # Description
        desc = ttk.Label(
            frame,
            text="Discord Send Guard is ready to protect you from accidental sends!\n\n"
                 "The app will run in your menu bar.\n\n"
                 "Remember:\n"
                 "• Enter = New line\n"
                 "• Cmd+Enter = Send message",
            font=('Helvetica', 14),
            justify=tk.CENTER,
            wraplength=600
        )
        desc.pack(pady=30)

        # Navigation buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(side=tk.BOTTOM, pady=20)

        finish_btn = ttk.Button(
            button_frame,
            text="Finish & Start",
            command=self._finish_setup
        )
        finish_btn.pack()

    def _show_page(self, page_index: int):
        """
        Show a specific page

        Args:
            page_index: Page index
        """
        self.current_page = page_index
        if 0 <= page_index < len(self.pages):
            self.pages[page_index]()

    def _next_page(self):
        """Go to next page"""
        # If on autostart page, save autostart preference
        if self.current_page == 2:
            self._save_autostart_preference()

        if self.current_page < len(self.pages) - 1:
            self._show_page(self.current_page + 1)

    def _prev_page(self):
        """Go to previous page"""
        if self.current_page > 0:
            self._show_page(self.current_page - 1)

    def _show_permission_guide(self):
        """Show permission guide window"""
        try:
            from gui.permission_guide import show_permission_guide
            show_permission_guide(
                parent=self.window,
                on_complete=self._check_permission
            )
        except Exception as e:
            logger.error(f"Failed to show permission guide: {e}")
            messagebox.showerror("Error", f"Failed to open guide: {e}")

    def _check_permission(self):
        """Check accessibility permission"""
        try:
            from utils.permissions import check_accessibility_permission

            granted = check_accessibility_permission()

            if granted:
                self.permission_status_label.config(
                    text="✓ Permission granted!",
                    foreground="green"
                )
                self.permission_next_btn.config(state=tk.NORMAL)
            else:
                self.permission_status_label.config(
                    text="✗ Permission not yet granted",
                    foreground="orange"
                )
                # Still allow next, but warn
                self.permission_next_btn.config(state=tk.NORMAL)

        except Exception as e:
            logger.error(f"Failed to check permission: {e}")
            self.permission_status_label.config(
                text="⚠ Unable to check permission",
                foreground="red"
            )

    def _save_autostart_preference(self):
        """Save autostart preference"""
        try:
            from utils.autostart import toggle_autostart

            enabled = self.autostart_var.get()
            self.config.autostart = enabled

            # Configure system autostart
            toggle_autostart(enabled)

            logger.info(f"Autostart {'enabled' if enabled else 'disabled'}")

        except Exception as e:
            logger.error(f"Failed to configure autostart: {e}")
            messagebox.showwarning(
                "Warning",
                f"Failed to configure auto-start: {e}\n\nYou can change this later in Settings."
            )

    def _finish_setup(self):
        """Finish setup and close wizard"""
        # Mark first run as complete
        self.config.first_run = False

        if self.on_complete:
            self.on_complete()

        self.window.destroy()

    def run(self):
        """Run the setup wizard"""
        self.window.mainloop()


def run_setup_wizard(config, on_complete=None):
    """
    Run the setup wizard

    Args:
        config: Config instance
        on_complete: Callback when setup is complete
    """
    wizard = SetupWizard(config, on_complete)
    wizard.run()


if __name__ == '__main__':
    # For testing
    logging.basicConfig(level=logging.INFO)
    from utils.config import get_config
    config = get_config()
    run_setup_wizard(config)
