#!/usr/bin/env python3
"""
Generate guide images programmatically using Pillow
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Image dimensions
IMG_WIDTH = 800
IMG_HEIGHT = 600
BG_COLOR = (240, 240, 245)  # Light gray
TEXT_COLOR = (40, 40, 50)   # Dark gray
ACCENT_COLOR = (0, 122, 255)  # macOS blue
BORDER_COLOR = (200, 200, 210)


def create_guide_image(title: str, steps: list, output_path: Path):
    """
    Create a guide image with title and steps

    Args:
        title: Title text
        steps: List of step strings
        output_path: Path to save the image
    """
    # Create image
    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Try to use a nice font, fall back to default
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
        step_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 32)
        text_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    except Exception:
        title_font = ImageFont.load_default()
        step_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # Draw border
    draw.rectangle(
        [(20, 20), (IMG_WIDTH - 20, IMG_HEIGHT - 20)],
        outline=BORDER_COLOR,
        width=3
    )

    # Draw title
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (IMG_WIDTH - title_width) // 2
    draw.text((title_x, 60), title, fill=ACCENT_COLOR, font=title_font)

    # Draw steps
    y_offset = 150
    for i, step in enumerate(steps, 1):
        # Step number circle
        circle_x = 80
        circle_y = y_offset
        circle_radius = 25
        draw.ellipse(
            [(circle_x - circle_radius, circle_y - circle_radius),
             (circle_x + circle_radius, circle_y + circle_radius)],
            fill=ACCENT_COLOR,
            outline=ACCENT_COLOR
        )

        # Step number text
        step_num = str(i)
        num_bbox = draw.textbbox((0, 0), step_num, font=step_font)
        num_width = num_bbox[2] - num_bbox[0]
        num_height = num_bbox[3] - num_bbox[1]
        draw.text(
            (circle_x - num_width // 2, circle_y - num_height // 2 - 5),
            step_num,
            fill=(255, 255, 255),
            font=step_font
        )

        # Step text (with wrapping)
        lines = wrap_text(step, 50)
        text_y = circle_y - (len(lines) * 15)
        for line in lines:
            draw.text((140, text_y), line, fill=TEXT_COLOR, font=text_font)
            text_y += 30

        y_offset += 120

    # Save image
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    logger.info(f"Generated guide image: {output_path}")


def wrap_text(text: str, max_chars: int) -> list:
    """
    Wrap text to fit within max_chars per line

    Args:
        text: Text to wrap
        max_chars: Maximum characters per line

    Returns:
        List of text lines
    """
    words = text.split()
    lines = []
    current_line = []
    current_length = 0

    for word in words:
        word_length = len(word) + 1  # +1 for space
        if current_length + word_length <= max_chars:
            current_line.append(word)
            current_length += word_length
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = word_length

    if current_line:
        lines.append(' '.join(current_line))

    return lines


def generate_all_guide_images(assets_dir: Path):
    """
    Generate all guide images

    Args:
        assets_dir: Path to assets directory
    """
    guide_dir = assets_dir / "guide"

    # Step 1: Open System Settings
    create_guide_image(
        "Step 1: Open System Settings",
        [
            "Click the Apple menu in the top-left corner",
            "Select 'System Settings' from the menu"
        ],
        guide_dir / "step1_system_settings.png"
    )

    # Step 2: Navigate to Privacy & Security
    create_guide_image(
        "Step 2: Privacy & Security",
        [
            "Click 'Privacy & Security' in the sidebar",
            "Scroll down if needed"
        ],
        guide_dir / "step2_privacy.png"
    )

    # Step 3: Open Accessibility
    create_guide_image(
        "Step 3: Accessibility",
        [
            "Find and click 'Accessibility' in the list",
            "You may need to scroll down"
        ],
        guide_dir / "step3_accessibility.png"
    )

    # Step 4: Add Discord Send Guard
    create_guide_image(
        "Step 4: Add App",
        [
            "Click the lock icon and authenticate",
            "Click the '+' button to add an app",
            "Select Discord Send Guard"
        ],
        guide_dir / "step4_add_app.png"
    )

    logger.info("All guide images generated successfully")


if __name__ == '__main__':
    # For testing
    logging.basicConfig(level=logging.INFO)
    current_dir = Path(__file__).parent.parent
    assets_dir = current_dir / "assets"
    generate_all_guide_images(assets_dir)
