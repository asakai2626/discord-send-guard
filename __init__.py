"""
Discord Send Guard - Discordでの誤送信を防止するツール

使用方法:
    from discord_send_guard import DiscordSendGuard

    guard = DiscordSendGuard()
    guard.start()
"""

__version__ = '1.0.0'
__author__ = 'Claude Code'
__license__ = 'MIT'

try:
    from .discord_send_guard import DiscordSendGuard, main
    __all__ = ['DiscordSendGuard', 'main']
except ImportError:
    pass
