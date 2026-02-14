import AppKit

struct DiscordDetector {
    private static let discordBundleID = "com.hnc.Discord"

    static func isDiscordFrontmost() -> Bool {
        guard let frontmost = NSWorkspace.shared.frontmostApplication else {
            return false
        }
        return frontmost.bundleIdentifier == discordBundleID
    }
}
