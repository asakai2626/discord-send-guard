import AppKit

final class DiscordDetector {
    private static let discordBundleID = "com.hnc.Discord"
    private static var _isDiscordFront = false

    static var isDiscordFront: Bool { _isDiscordFront }

    static func startMonitoring() {
        // 現在の状態を初期化
        _isDiscordFront = NSWorkspace.shared.frontmostApplication?.bundleIdentifier == discordBundleID

        // アプリ切り替えを監視（メインスレッドで実行）
        NSWorkspace.shared.notificationCenter.addObserver(
            forName: NSWorkspace.didActivateApplicationNotification,
            object: nil,
            queue: .main
        ) { notification in
            if let app = notification.userInfo?[NSWorkspace.applicationUserInfoKey] as? NSRunningApplication {
                _isDiscordFront = (app.bundleIdentifier == discordBundleID)
            }
        }
    }
}
