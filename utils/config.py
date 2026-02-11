#!/usr/bin/env python3
"""
Configuration management for Discord Send Guard
Handles reading/writing config.json in ~/.discord-send-guard/
"""

import json
import os
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

# Config directory and file paths
CONFIG_DIR = Path.home() / ".discord-send-guard"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Default configuration
DEFAULT_CONFIG = {
    "enabled": True,
    "autostart": False,
    "debug": False,
    "first_run": True,
}


class Config:
    """Configuration manager"""

    def __init__(self):
        """Initialize configuration"""
        self.config_dir = CONFIG_DIR
        self.config_file = CONFIG_FILE
        self._config: Dict[str, Any] = {}
        self._ensure_config_dir()
        self.load()

    def _ensure_config_dir(self):
        """Ensure config directory exists"""
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created config directory: {self.config_dir}")

    def load(self) -> Dict[str, Any]:
        """
        Load configuration from file

        Returns:
            Configuration dictionary
        """
        if not self.config_file.exists():
            logger.info("Config file not found, creating default config")
            self._config = DEFAULT_CONFIG.copy()
            self.save()
            return self._config

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
            logger.info("Configuration loaded successfully")

            # Merge with defaults to handle new config keys
            for key, value in DEFAULT_CONFIG.items():
                if key not in self._config:
                    self._config[key] = value

            return self._config
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            self._config = DEFAULT_CONFIG.copy()
            return self._config

    def save(self):
        """Save configuration to file"""
        try:
            self._ensure_config_dir()
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            logger.info("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            raise

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any):
        """
        Set configuration value

        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value
        self.save()

    def update(self, updates: Dict[str, Any]):
        """
        Update multiple configuration values

        Args:
            updates: Dictionary of updates
        """
        self._config.update(updates)
        self.save()

    def reset(self):
        """Reset configuration to defaults"""
        self._config = DEFAULT_CONFIG.copy()
        self.save()
        logger.info("Configuration reset to defaults")

    @property
    def enabled(self) -> bool:
        """Get enabled status"""
        return self._config.get("enabled", True)

    @enabled.setter
    def enabled(self, value: bool):
        """Set enabled status"""
        self.set("enabled", value)

    @property
    def autostart(self) -> bool:
        """Get autostart status"""
        return self._config.get("autostart", False)

    @autostart.setter
    def autostart(self, value: bool):
        """Set autostart status"""
        self.set("autostart", value)

    @property
    def debug(self) -> bool:
        """Get debug status"""
        return self._config.get("debug", False)

    @debug.setter
    def debug(self, value: bool):
        """Set debug status"""
        self.set("debug", value)

    @property
    def first_run(self) -> bool:
        """Get first run status"""
        return self._config.get("first_run", True)

    @first_run.setter
    def first_run(self, value: bool):
        """Set first run status"""
        self.set("first_run", value)


# Global config instance
_config_instance = None


def get_config() -> Config:
    """
    Get global configuration instance

    Returns:
        Config instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance
