#!/usr/bin/env python3
"""
Permission guide window for Discord Send Guard
Shows step-by-step instructions for granting accessibility permissions
"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class PermissionGuideWindow:
    """Permission guide window"""

    def __init__(self, parent=None, on_complete=None):
        """
        Initialize permission guide window

        Args:
            parent: Parent window (optional)
            on_complete: Callback when guide is completed
        """
        self.on_complete = on_complete
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Discord Send Guard - Accessibility Permission Setup")
        self.window.geometry("900x700")
        self.window.resizable(False, False)

        self.current_step = 0
        self.guide_images = []

        # Get assets directory
        current_dir = Path(__file__).parent.parent
        self.assets_dir = current_dir / "assets" / "guide"

        self._create_widgets()
        self._load_images()
        self._show_step(0)

    def _create_widgets(self):
        """Create window widgets"""
        # Main container
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Accessibility Permission Setup",
            font=('Helvetica', 24, 'bold')
        )
        title_label.pack(pady=(0, 20))

        # Description
        desc_label = ttk.Label(
            main_frame,
            text="Discord Send Guard needs accessibility permissions to intercept keyboard input.",
            font=('Helvetica', 12),
            wraplength=800,
            justify=tk.CENTER
        )
        desc_label.pack(pady=(0, 20))

        # Image container
        self.image_label = ttk.Label(main_frame)
        self.image_label.pack(pady=20)

        # Step description
        self.step_label = ttk.Label(
            main_frame,
            text="",
            font=('Helvetica', 14),
            wraplength=800,
            justify=tk.LEFT
        )
        self.step_label.pack(pady=10, fill=tk.X)

        # Button container
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))

        # Navigation buttons
        self.prev_button = ttk.Button(
            button_frame,
            text="← Previous",
            command=self._prev_step
        )
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = ttk.Button(
            button_frame,
            text="Next →",
            command=self._next_step
        )
        self.next_button.pack(side=tk.RIGHT)

        # Open System Settings button
        self.open_settings_button = ttk.Button(
            button_frame,
            text="Open System Settings",
            command=self._open_system_settings
        )
        self.open_settings_button.pack(side=tk.LEFT, padx=(20, 0))

        # Check permission button
        self.check_button = ttk.Button(
            button_frame,
            text="Check Permission",
            command=self._check_permission
        )
        self.check_button.pack(side=tk.RIGHT, padx=(0, 20))

    def _load_images(self):
        """Load guide images"""
        try:
            from PIL import Image, ImageTk

            image_files = [
                "step1_system_settings.png",
                "step2_privacy.png",
                "step3_accessibility.png",
                "step4_add_app.png"
            ]

            for img_file in image_files:
                img_path = self.assets_dir / img_file
                if img_path.exists():
                    img = Image.open(img_path)
                    # Resize to fit window
                    img = img.resize((800, 400), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.guide_images.append(photo)
                else:
                    logger.warning(f"Guide image not found: {img_path}")
                    self.guide_images.append(None)

        except ImportError:
            logger.error("PIL/Pillow not available for loading images")
        except Exception as e:
            logger.error(f"Failed to load images: {e}")

    def _show_step(self, step: int):
        """
        Show a specific step

        Args:
            step: Step index (0-3)
        """
        self.current_step = step

        # Update image
        if step < len(self.guide_images) and self.guide_images[step]:
            self.image_label.config(image=self.guide_images[step])
        else:
            self.image_label.config(image='', text='Image not available')

        # Update step description
        step_descriptions = [
            "Step 1: Click the Apple menu (🍎) in the top-left corner and select 'System Settings'.",
            "Step 2: In System Settings, click 'Privacy & Security' in the sidebar.",
            "Step 3: Scroll down and click 'Accessibility' in the Privacy section.",
            "Step 4: Click the lock icon to make changes, then click '+' to add Discord Send Guard."
        ]

        if step < len(step_descriptions):
            self.step_label.config(text=step_descriptions[step])

        # Update button states
        self.prev_button.config(state=tk.NORMAL if step > 0 else tk.DISABLED)
        self.next_button.config(
            text="Complete" if step >= 3 else "Next →",
            command=self._complete if step >= 3 else self._next_step
        )

    def _prev_step(self):
        """Go to previous step"""
        if self.current_step > 0:
            self._show_step(self.current_step - 1)

    def _next_step(self):
        """Go to next step"""
        if self.current_step < 3:
            self._show_step(self.current_step + 1)

    def _open_system_settings(self):
        """Open macOS System Settings"""
        try:
            from utils.permissions import open_system_settings
            open_system_settings()
        except Exception as e:
            logger.error(f"Failed to open System Settings: {e}")

    def _check_permission(self):
        """Check if permission is granted"""
        try:
            from utils.permissions import check_accessibility_permission
            from tkinter import messagebox

            if check_accessibility_permission():
                messagebox.showinfo(
                    "Permission Granted",
                    "✓ Accessibility permission has been granted!\n\nYou can now use Discord Send Guard."
                )
            else:
                messagebox.showwarning(
                    "Permission Required",
                    "✗ Accessibility permission is not yet granted.\n\nPlease follow the steps and try again."
                )
        except Exception as e:
            logger.error(f"Failed to check permission: {e}")

    def _complete(self):
        """Complete the guide"""
        if self.on_complete:
            self.on_complete()
        self.window.destroy()

    def show(self):
        """Show the window"""
        self.window.mainloop()


def show_permission_guide(parent=None, on_complete=None):
    """
    Show permission guide window

    Args:
        parent: Parent window (optional)
        on_complete: Callback when guide is completed
    """
    guide = PermissionGuideWindow(parent, on_complete)
    if parent:
        # Modal if parent provided
        guide.window.transient(parent)
        guide.window.grab_set()
        parent.wait_window(guide.window)
    else:
        guide.show()


if __name__ == '__main__':
    # For testing
    logging.basicConfig(level=logging.INFO)
    show_permission_guide()
