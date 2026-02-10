#!/usr/bin/env python3
"""
Discord Send Guard - メインモジュール

Discordがアクティブウィンドウのときだけ、Enterキー単体を改行に、
Cmd+Enter(Mac)/Ctrl+Enter(Windows)を送信に変更するツール。
"""

import sys
import platform
import logging
from typing import Optional
from pynput import keyboard
from pynput.keyboard import Key, KeyCode, Controller

# プラットフォーム判定
IS_MAC = platform.system() == 'Darwin'
IS_WINDOWS = platform.system() == 'Windows'

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DiscordSendGuard:
    """Discord Send Guardのメインクラス"""

    def __init__(self, debug: bool = False):
        """
        初期化

        Args:
            debug: デバッグモードの有効化
        """
        self.debug = debug
        if debug:
            logger.setLevel(logging.DEBUG)

        self.keyboard_controller = Controller()
        self.modifier_pressed = False  # Cmd(Mac) or Ctrl(Windows)が押されているか
        self.running = False
        self.listener: Optional[keyboard.Listener] = None

        logger.info(f"Discord Send Guard initialized on {platform.system()}")

    def is_discord_active(self) -> bool:
        """
        Discordがアクティブウィンドウかどうかを判定

        Returns:
            Discordがアクティブの場合True
        """
        try:
            if IS_MAC:
                return self._is_discord_active_mac()
            elif IS_WINDOWS:
                return self._is_discord_active_windows()
            else:
                logger.warning(f"Unsupported platform: {platform.system()}")
                return False
        except Exception as e:
            logger.error(f"Error checking active window: {e}")
            return False

    def _is_discord_active_mac(self) -> bool:
        """macOSでDiscordがアクティブかチェック"""
        try:
            from AppKit import NSWorkspace
            active_app = NSWorkspace.sharedWorkspace().activeApplication()
            app_name = active_app.get('NSApplicationName', '').lower()

            if self.debug:
                logger.debug(f"Active app: {app_name}")

            return 'discord' in app_name
        except ImportError:
            logger.error("AppKit not available. Install with: pip install pyobjc-framework-Cocoa")
            return False

    def _is_discord_active_windows(self) -> bool:
        """WindowsでDiscordがアクティブかチェック"""
        try:
            import win32gui

            hwnd = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(hwnd).lower()

            if self.debug:
                logger.debug(f"Active window: {window_title}")

            return 'discord' in window_title
        except ImportError:
            logger.error("win32gui not available. Install with: pip install pywin32")
            return False

    def on_press(self, key) -> bool:
        """
        キー押下時のハンドラ

        Args:
            key: 押されたキー

        Returns:
            False to stop the listener, True to continue
        """
        try:
            # Cmd(Mac) or Ctrl(Windows)の検出
            if IS_MAC and key == Key.cmd:
                self.modifier_pressed = True
                if self.debug:
                    logger.debug("Cmd pressed")
            elif IS_WINDOWS and key == Key.ctrl_l or key == Key.ctrl_r:
                self.modifier_pressed = True
                if self.debug:
                    logger.debug("Ctrl pressed")

            # Enterキーの処理
            if key == Key.enter:
                if not self.is_discord_active():
                    # Discord以外では通常動作
                    return True

                if self.modifier_pressed:
                    # Cmd+Enter / Ctrl+Enter → 送信（Enterを通す）
                    if self.debug:
                        logger.debug("Modifier+Enter detected in Discord - allowing send")
                    return True
                else:
                    # Enter単体 → 改行（Enterをブロックして Shift+Enter を送信）
                    if self.debug:
                        logger.debug("Enter detected in Discord - converting to newline")

                    # 元のEnterをブロック
                    # Shift+Enterを送信（Discordでは改行になる）
                    with self.keyboard_controller.pressed(Key.shift):
                        self.keyboard_controller.press(Key.enter)
                        self.keyboard_controller.release(Key.enter)

                    return False  # 元のEnterイベントをブロック

        except Exception as e:
            logger.error(f"Error in on_press: {e}")

        return True

    def on_release(self, key) -> bool:
        """
        キー解放時のハンドラ

        Args:
            key: 解放されたキー

        Returns:
            False to stop the listener, True to continue
        """
        try:
            # Cmd(Mac) or Ctrl(Windows)の解放
            if IS_MAC and key == Key.cmd:
                self.modifier_pressed = False
                if self.debug:
                    logger.debug("Cmd released")
            elif IS_WINDOWS and (key == Key.ctrl_l or key == Key.ctrl_r):
                self.modifier_pressed = False
                if self.debug:
                    logger.debug("Ctrl released")

            # Ctrl+C で終了
            if key == KeyCode.from_char('c') and self.modifier_pressed:
                logger.info("Ctrl+C detected, stopping...")
                return False

        except Exception as e:
            logger.error(f"Error in on_release: {e}")

        return True

    def start(self):
        """Discord Send Guardを開始"""
        if self.running:
            logger.warning("Already running")
            return

        logger.info("Starting Discord Send Guard...")
        logger.info("Press Ctrl+C to stop")

        # プラットフォーム固有の警告
        if IS_MAC:
            logger.info("NOTE: macOS requires Accessibility permissions")
            logger.info("Go to: System Settings > Privacy & Security > Accessibility")
        elif IS_WINDOWS:
            logger.info("NOTE: Windows may require administrator privileges")

        self.running = True

        # キーボードリスナーを開始
        with keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release,
            suppress=False  # 通常は他のキーを抑制しない
        ) as self.listener:
            self.listener.join()

        self.running = False
        logger.info("Discord Send Guard stopped")

    def stop(self):
        """Discord Send Guardを停止"""
        if not self.running:
            return

        logger.info("Stopping Discord Send Guard...")
        if self.listener:
            self.listener.stop()
        self.running = False


def main():
    """メインエントリーポイント"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Discord Send Guard - Prevent accidental message sends in Discord'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='Discord Send Guard 1.0.0'
    )

    args = parser.parse_args()

    # プラットフォームチェック
    if not (IS_MAC or IS_WINDOWS):
        logger.error(f"Unsupported platform: {platform.system()}")
        logger.error("This tool only supports macOS and Windows")
        sys.exit(1)

    # Discord Send Guardを開始
    guard = DiscordSendGuard(debug=args.debug)

    try:
        guard.start()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        guard.stop()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
