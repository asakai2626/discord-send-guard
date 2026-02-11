#!/usr/bin/env python3
"""
Generate icon assets for Discord Send Guard
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def create_shield_icon(size: int, output_path: Path):
    """
    Create a shield icon

    Args:
        size: Icon size (square)
        output_path: Path to save the icon
    """
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    bg_color = (0, 122, 255, 255)  # macOS blue
    border_color = (255, 255, 255, 255)  # White

    # Calculate shield dimensions
    margin = size // 10
    shield_width = size - (margin * 2)
    shield_height = shield_width

    # Draw shield shape (simplified)
    # Top part (rectangle)
    top_height = int(shield_height * 0.6)
    draw.rounded_rectangle(
        [(margin, margin), (size - margin, margin + top_height)],
        radius=size // 10,
        fill=bg_color,
        outline=border_color,
        width=max(2, size // 50)
    )

    # Bottom part (triangle)
    bottom_points = [
        (margin, margin + top_height),
        (size // 2, size - margin),
        (size - margin, margin + top_height)
    ]
    draw.polygon(bottom_points, fill=bg_color, outline=border_color)

    # Add checkmark or symbol
    check_size = size // 3
    check_x = size // 2 - check_size // 4
    check_y = size // 2 - check_size // 4

    # Simple checkmark
    draw.line(
        [(check_x, check_y + check_size // 2),
         (check_x + check_size // 3, check_y + check_size)],
        fill=(255, 255, 255, 255),
        width=max(3, size // 20)
    )
    draw.line(
        [(check_x + check_size // 3, check_y + check_size),
         (check_x + check_size, check_y)],
        fill=(255, 255, 255, 255),
        width=max(3, size // 20)
    )

    # Save icon
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    logger.info(f"Generated icon: {output_path}")


def create_menu_bar_icon(output_path: Path):
    """
    Create menu bar icon (small, template style for macOS)

    Args:
        output_path: Path to save the icon
    """
    # Menu bar icons should be small (22x22 recommended)
    size = 22
    create_shield_icon(size, output_path)


def create_app_icon_png(output_path: Path):
    """
    Create app icon as PNG (will be converted to icns)

    Args:
        output_path: Path to save the icon
    """
    # App icons are typically 512x512 or 1024x1024
    size = 512
    create_shield_icon(size, output_path)


def png_to_icns(png_path: Path, icns_path: Path):
    """
    Convert PNG to ICNS format for macOS app icon

    Args:
        png_path: Path to PNG file
        icns_path: Path to save ICNS file
    """
    try:
        import subprocess

        # Create iconset directory
        iconset_dir = png_path.parent / f"{png_path.stem}.iconset"
        iconset_dir.mkdir(exist_ok=True)

        # Load base image
        img = Image.open(png_path)

        # Required icon sizes for macOS
        sizes = [16, 32, 64, 128, 256, 512, 1024]

        for size in sizes:
            # Normal resolution
            resized = img.resize((size, size), Image.Resampling.LANCZOS)
            resized.save(iconset_dir / f"icon_{size}x{size}.png")

            # Retina resolution (2x)
            if size <= 512:  # Max 1024x1024
                retina_size = size * 2
                resized_2x = img.resize((retina_size, retina_size), Image.Resampling.LANCZOS)
                resized_2x.save(iconset_dir / f"icon_{size}x{size}@2x.png")

        # Convert iconset to icns using iconutil
        subprocess.run([
            'iconutil',
            '-c', 'icns',
            str(iconset_dir),
            '-o', str(icns_path)
        ], check=True)

        logger.info(f"Generated ICNS: {icns_path}")

        # Clean up iconset directory
        import shutil
        shutil.rmtree(iconset_dir)

    except Exception as e:
        logger.error(f"Failed to create ICNS: {e}")
        raise


def generate_all_icons(assets_dir: Path):
    """
    Generate all icon assets

    Args:
        assets_dir: Path to assets directory
    """
    # Menu bar icon
    create_menu_bar_icon(assets_dir / "icon.png")

    # App icon (PNG)
    app_icon_png = assets_dir / "app_icon.png"
    create_app_icon_png(app_icon_png)

    # App icon (ICNS for py2app)
    try:
        png_to_icns(app_icon_png, assets_dir / "app_icon.icns")
    except Exception as e:
        logger.warning(f"Failed to create ICNS (may need iconutil): {e}")

    logger.info("All icons generated successfully")


if __name__ == '__main__':
    # For testing
    logging.basicConfig(level=logging.INFO)
    current_dir = Path(__file__).parent.parent
    assets_dir = current_dir / "assets"
    generate_all_icons(assets_dir)
