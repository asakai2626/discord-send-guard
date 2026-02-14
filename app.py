#!/usr/bin/env python3
"""
Discord Send Guard - Menu Bar Application
Main entry point for the macOS GUI app
"""

import sys
import logging
import threading
from pathlib import Path

# Configure logging
log_dir = Path.home() / "Library" / "Logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "com.ideaccept.discord-send-guard.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DiscordSendGuardApp:
    """Main application class"""

    def __init__(self):
        """Initialize the application"""
        logger.info("Initializing Discord Send Guard App v2.0")

        # Import after logging is configured
        from utils.config import get_config
        from discord_send_guard import DiscordSendGuard

        self.config = get_config()
        self.guard = None
        self.guard_thread = None
        self.app = None

        # Set debug level if configured
        if self.config.debug:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.debug("Debug mode enabled")

        # Initialize Discord Send Guard
        self.guard = DiscordSendGuard(debug=self.config.debug)

        # Check for first run
        if self.config.first_run:
            logger.info("First run detected")
            # Mark first run as done (wizard may fail in bundled app)
            self.config.first_run = False
            try:
                from utils.config import save_config
                save_config(self.config)
            except Exception:
                pass
            self._run_setup_wizard()

        # Create menu bar app
        self._create_menu_bar_app()

    def _run_setup_wizard(self):
        """Run the setup wizard for first-time users"""
        try:
            from gui.setup_wizard import run_setup_wizard

            def on_complete():
                logger.info("Setup wizard completed")

            run_setup_wizard(self.config, on_complete=on_complete)

        except Exception as e:
            logger.error(f"Failed to run setup wizard: {e}")
            # Continue anyway - user can configure later

    def _create_menu_bar_app(self):
        """Create the menu bar application"""
        try:
            import rumps

            # Create menu bar app
            self.app = rumps.App(
                "Discord Send Guard",
                icon=self._get_icon_path(),
                quit_button=None  # Custom quit button
            )

            # Add menu items
            self._setup_menu()

            # Start guard if enabled
            if self.config.enabled:
                self._start_guard()

        except Exception as e:
            logger.error(f"Failed to create menu bar app: {e}")
            raise

    def _get_icon_path(self) -> str:
        """
        Get path to menu bar icon

        Returns:
            Path to icon file or None
        """
        # Try to find icon in assets directory
        current_dir = Path(__file__).parent
        icon_path = current_dir / "assets" / "icon.png"

        if icon_path.exists():
            return str(icon_path)

        # Return None to use default icon
        return None

    def _setup_menu(self):
        """Setup menu bar items"""
        import rumps

        # Status item (non-clickable)
        status_text = "✓ Enabled" if self.config.enabled else "✗ Disabled"
        self.status_item = rumps.MenuItem(status_text, callback=None)
        self.app.menu.add(self.status_item)

        # Separator
        self.app.menu.add(rumps.separator)

        # Enable/Disable toggle
        toggle_title = "Disable" if self.config.enabled else "Enable"
        self.app.menu.add(rumps.MenuItem(toggle_title, callback=self._toggle_guard))

        # Settings
        self.app.menu.add(rumps.MenuItem("Settings...", callback=self._show_settings))

        # Permission Guide
        self.app.menu.add(rumps.MenuItem("Permission Guide...", callback=self._show_permission_guide))

        # Separator
        self.app.menu.add(rumps.separator)

        # View Logs
        self.app.menu.add(rumps.MenuItem("View Logs", callback=self._view_logs))

        # About
        self.app.menu.add(rumps.MenuItem("About", callback=self._show_about))

        # Separator
        self.app.menu.add(rumps.separator)

        # Quit
        self.app.menu.add(rumps.MenuItem("Quit", callback=self._quit))

    def _update_status(self):
        """Update status menu item"""
        status_text = "✓ Enabled" if self.config.enabled else "✗ Disabled"
        self.status_item.title = status_text

        # Update toggle button text
        for item in self.app.menu.values():
            if isinstance(item, tuple):
                continue
            if item.title in ["Enable", "Disable"]:
                item.title = "Disable" if self.config.enabled else "Enable"

    def _start_guard(self):
        """Start the Discord Send Guard in a background thread"""
        if self.guard_thread and self.guard_thread.is_alive():
            logger.warning("Guard is already running")
            return

        logger.info("Starting Discord Send Guard...")

        def run_guard():
            try:
                self.guard.start()
            except Exception as e:
                logger.error(f"Guard error: {e}")

        self.guard_thread = threading.Thread(target=run_guard, daemon=True)
        self.guard_thread.start()

        logger.info("Discord Send Guard started")

    def _stop_guard(self):
        """Stop the Discord Send Guard"""
        if not self.guard_thread or not self.guard_thread.is_alive():
            logger.warning("Guard is not running")
            return

        logger.info("Stopping Discord Send Guard...")
        self.guard.stop()

        # Wait for thread to finish (with timeout)
        self.guard_thread.join(timeout=2)

        logger.info("Discord Send Guard stopped")

    def _toggle_guard(self, sender):
        """Toggle guard on/off"""
        try:
            if self.config.enabled:
                # Disable
                self._stop_guard()
                self.config.enabled = False
                logger.info("Guard disabled")
            else:
                # Enable
                self.config.enabled = True
                self._start_guard()
                logger.info("Guard enabled")

            self._update_status()

        except Exception as e:
            logger.error(f"Failed to toggle guard: {e}")
            import rumps
            rumps.alert("Error", f"Failed to toggle guard: {e}")

    def _show_settings(self, sender):
        """Show settings window"""
        try:
            # Need to run in main thread for tkinter
            import threading
            from gui.settings_window import show_settings

            def run_settings():
                show_settings(self.config, self.guard)

            settings_thread = threading.Thread(target=run_settings)
            settings_thread.start()

        except Exception as e:
            logger.error(f"Failed to show settings: {e}")
            import rumps
            rumps.alert("Error", f"Failed to open settings: {e}")

    def _show_permission_guide(self, sender):
        """Show permission guide"""
        try:
            import threading
            from gui.permission_guide import show_permission_guide

            def run_guide():
                show_permission_guide()

            guide_thread = threading.Thread(target=run_guide)
            guide_thread.start()

        except Exception as e:
            logger.error(f"Failed to show permission guide: {e}")
            import rumps
            rumps.alert("Error", f"Failed to open permission guide: {e}")

    def _view_logs(self, sender):
        """Open log file in Console.app"""
        try:
            import subprocess
            subprocess.run(['open', '-a', 'Console', str(log_file)])
            logger.info("Opened log file in Console")
        except Exception as e:
            logger.error(f"Failed to open log file: {e}")
            import rumps
            rumps.alert("Error", f"Failed to open logs: {e}")

    def _show_about(self, sender):
        """Show about dialog"""
        import rumps

        about_text = (
            "Discord Send Guard v2.0\n\n"
            "Prevents accidental message sends in Discord\n\n"
            "• Enter = New line\n"
            "• Cmd+Enter = Send message\n\n"
            "© 2025 Asakai & ideaccept-openclaw"
        )

        rumps.alert("About Discord Send Guard", about_text)

    def _quit(self, sender):
        """Quit the application"""
        logger.info("Quitting Discord Send Guard")

        # Stop guard if running
        if self.config.enabled:
            self._stop_guard()

        # Quit the app
        import rumps
        rumps.quit_application()

    def run(self):
        """Run the application"""
        logger.info("Starting Discord Send Guard menu bar app")
        try:
            self.app.run()
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
            self._quit(None)
        except Exception as e:
            logger.error(f"Application error: {e}")
            raise


def main():
    """Main entry point"""
    try:
        app = DiscordSendGuardApp()
        app.run()
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
