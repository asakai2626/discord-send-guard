#!/usr/bin/env python3
"""
Setup wizard for first-run experience (rumps-based, no tkinter dependency)
"""

import subprocess
import logging

logger = logging.getLogger(__name__)


def run_setup_wizard(config, on_complete=None):
    """
    Run the setup wizard using native macOS dialogs (via osascript).
    No tkinter required.
    """
    try:
        # Step 1: Welcome
        _show_dialog(
            "Discord Send Guard へようこそ！ 🛡️",
            "このアプリはDiscordでの誤送信を防止します。\n\n"
            "• Enter = 改行（送信しない）\n"
            "• Cmd+Enter = メッセージ送信\n\n"
            "セットアップを始めましょう！"
        )

        # Step 2: Accessibility Permission
        _show_dialog(
            "アクセシビリティ権限が必要です",
            "キー入力を変更するために、アクセシビリティ権限が必要です。\n\n"
            "次の手順で設定してください：\n"
            "1. システム設定を開く\n"
            "2. プライバシーとセキュリティ → アクセシビリティ\n"
            "3. 「Discord Send Guard」を追加してチェック\n"
            "4. アプリを再起動\n\n"
            "※ この権限がないとキーの変更ができません"
        )

        # Ask to open System Settings
        open_settings = _show_yes_no(
            "システム設定を開く",
            "アクセシビリティ設定を今すぐ開きますか？"
        )
        if open_settings:
            subprocess.run([
                'open', 'x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility'
            ])

        # Step 3: Complete
        _show_dialog(
            "セットアップ完了！ ✅",
            "Discord Send Guard の準備ができました！\n\n"
            "メニューバーの🛡️アイコンから操作できます。\n\n"
            "覚えておくこと：\n"
            "• Enter = 改行\n"
            "• Cmd+Enter = 送信\n\n"
            "※ アクセシビリティ権限を設定した後、アプリを再起動してください。"
        )

        # Mark first run as complete
        config.first_run = False
        try:
            config.save()
        except Exception:
            pass

        if on_complete:
            on_complete()

    except Exception as e:
        logger.error(f"Setup wizard error: {e}")


def _show_dialog(title, message):
    """Show a native macOS dialog"""
    try:
        script = f'display dialog "{_escape(message)}" with title "{_escape(title)}" buttons {{"OK"}} default button "OK"'
        subprocess.run(['osascript', '-e', script], capture_output=True)
    except Exception as e:
        logger.error(f"Dialog error: {e}")


def _show_yes_no(title, message):
    """Show a Yes/No dialog, returns True if Yes"""
    try:
        script = f'display dialog "{_escape(message)}" with title "{_escape(title)}" buttons {{"いいえ", "はい"}} default button "はい"'
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        return "はい" in result.stdout
    except Exception:
        return False


def _escape(text):
    """Escape text for AppleScript"""
    return text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
