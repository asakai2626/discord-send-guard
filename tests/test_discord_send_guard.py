#!/usr/bin/env python3
"""
Discord Send Guardのユニットテスト
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from discord_send_guard import DiscordSendGuard
from pynput.keyboard import Key


class TestDiscordSendGuard(unittest.TestCase):
    """DiscordSendGuardのテストケース"""

    def setUp(self):
        """各テストの前に実行"""
        self.guard = DiscordSendGuard(debug=True)

    def tearDown(self):
        """各テストの後に実行"""
        if self.guard.running:
            self.guard.stop()

    def test_initialization(self):
        """初期化のテスト"""
        self.assertFalse(self.guard.running)
        self.assertFalse(self.guard.modifier_pressed)
        self.assertIsNotNone(self.guard.keyboard_controller)

    def test_modifier_key_detection_mac(self):
        """Mac用修飾キー検出のテスト"""
        with patch('discord_send_guard.IS_MAC', True):
            with patch('discord_send_guard.IS_WINDOWS', False):
                guard = DiscordSendGuard()
                result = guard.on_press(Key.cmd)
                self.assertTrue(result)
                self.assertTrue(guard.modifier_pressed)
                result = guard.on_release(Key.cmd)
                self.assertTrue(result)
                self.assertFalse(guard.modifier_pressed)

    def test_modifier_key_detection_windows(self):
        """Windows用修飾キー検出のテスト"""
        with patch('discord_send_guard.IS_MAC', False):
            with patch('discord_send_guard.IS_WINDOWS', True):
                guard = DiscordSendGuard()
                result = guard.on_press(Key.ctrl_l)
                self.assertTrue(result)
                self.assertTrue(guard.modifier_pressed)
                result = guard.on_release(Key.ctrl_l)
                self.assertTrue(result)
                self.assertFalse(guard.modifier_pressed)

    @patch.object(DiscordSendGuard, 'is_discord_active')
    def test_enter_key_in_non_discord(self, mock_discord_active):
        """Discord以外でのEnterキーのテスト"""
        mock_discord_active.return_value = False
        result = self.guard.on_press(Key.enter)
        self.assertTrue(result)

    @patch.object(DiscordSendGuard, 'is_discord_active')
    def test_enter_key_with_modifier_in_discord(self, mock_discord_active):
        """DiscordでのCmd+Enter/Ctrl+Enterのテスト"""
        mock_discord_active.return_value = True
        self.guard.modifier_pressed = True
        result = self.guard.on_press(Key.enter)
        self.assertTrue(result)

    @patch.object(DiscordSendGuard, 'is_discord_active')
    def test_enter_key_without_modifier_in_discord(self, mock_discord_active):
        """DiscordでのEnter単体のテスト"""
        mock_discord_active.return_value = True
        self.guard.modifier_pressed = False
        # MagicMockはコンテキストマネージャをサポート
        self.guard.keyboard_controller = MagicMock()
        result = self.guard.on_press(Key.enter)
        self.assertFalse(result)
        self.guard.keyboard_controller.pressed.assert_called_once_with(Key.shift)

    def test_is_discord_active_mac_true(self):
        """macOSでDiscordがアクティブな場合のテスト"""
        mock_workspace = Mock()
        mock_app = Mock()
        mock_app.get.return_value = 'Discord'
        mock_workspace.sharedWorkspace.return_value.activeApplication.return_value = mock_app

        with patch('discord_send_guard.IS_MAC', True), \
             patch.dict('sys.modules', {'AppKit': Mock(NSWorkspace=mock_workspace)}):
            result = self.guard._is_discord_active_mac()
        self.assertTrue(result)

    def test_is_discord_active_mac_false(self):
        """macOSでDiscordがアクティブでない場合のテスト"""
        mock_workspace = Mock()
        mock_app = Mock()
        mock_app.get.return_value = 'Safari'
        mock_workspace.sharedWorkspace.return_value.activeApplication.return_value = mock_app

        with patch('discord_send_guard.IS_MAC', True), \
             patch.dict('sys.modules', {'AppKit': Mock(NSWorkspace=mock_workspace)}):
            result = self.guard._is_discord_active_mac()
        self.assertFalse(result)

    def test_is_discord_active_windows_true(self):
        """WindowsでDiscordがアクティブな場合のテスト"""
        mock_win32gui = Mock()
        mock_win32gui.GetForegroundWindow.return_value = 12345
        mock_win32gui.GetWindowText.return_value = 'Discord - Channel Name'

        with patch('discord_send_guard.IS_WINDOWS', True), \
             patch.dict('sys.modules', {'win32gui': mock_win32gui}):
            result = self.guard._is_discord_active_windows()
        self.assertTrue(result)

    def test_is_discord_active_windows_false(self):
        """WindowsでDiscordがアクティブでない場合のテスト"""
        mock_win32gui = Mock()
        mock_win32gui.GetForegroundWindow.return_value = 12345
        mock_win32gui.GetWindowText.return_value = 'Google Chrome'

        with patch('discord_send_guard.IS_WINDOWS', True), \
             patch.dict('sys.modules', {'win32gui': mock_win32gui}):
            result = self.guard._is_discord_active_windows()
        self.assertFalse(result)

    def test_multiple_modifier_press_release(self):
        """修飾キーの複数回押下・解放のテスト"""
        with patch('discord_send_guard.IS_MAC', True):
            guard = DiscordSendGuard()
            guard.on_press(Key.cmd)
            self.assertTrue(guard.modifier_pressed)
            guard.on_release(Key.cmd)
            self.assertFalse(guard.modifier_pressed)
            guard.on_press(Key.cmd)
            self.assertTrue(guard.modifier_pressed)
            guard.on_release(Key.cmd)
            self.assertFalse(guard.modifier_pressed)

    @patch.object(DiscordSendGuard, 'is_discord_active')
    def test_error_handling_in_key_press(self, mock_discord_active):
        """キー押下時のエラーハンドリングのテスト"""
        mock_discord_active.side_effect = Exception("Test error")
        result = self.guard.on_press(Key.enter)
        self.assertTrue(result)

    def test_stop_when_not_running(self):
        """実行中でないときのstop()のテスト"""
        self.assertFalse(self.guard.running)
        self.guard.stop()
        self.assertFalse(self.guard.running)


class TestIntegration(unittest.TestCase):
    """統合テスト"""

    def test_full_workflow_mac(self):
        """macOS上での全体ワークフローのテスト"""
        mock_workspace = Mock()
        mock_app = Mock()
        mock_app.get.return_value = 'Discord'
        mock_workspace.sharedWorkspace.return_value.activeApplication.return_value = mock_app

        with patch('discord_send_guard.IS_MAC', True), \
             patch.dict('sys.modules', {'AppKit': Mock(NSWorkspace=mock_workspace)}):

            guard = DiscordSendGuard(debug=True)
            guard.keyboard_controller = MagicMock()

            guard.on_press(Key.cmd)
            self.assertTrue(guard.modifier_pressed)

            result = guard.on_press(Key.enter)
            self.assertTrue(result)

            guard.on_release(Key.cmd)
            self.assertFalse(guard.modifier_pressed)

            result = guard.on_press(Key.enter)
            self.assertFalse(result)
            guard.keyboard_controller.pressed.assert_called_with(Key.shift)


def run_tests():
    """テストを実行"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    run_tests()
