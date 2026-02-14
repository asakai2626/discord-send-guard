import Foundation
import ServiceManagement

struct AutoStartManager {
    static var isEnabled: Bool {
        if #available(macOS 13.0, *) {
            return SMAppService.mainApp.status == .enabled
        } else {
            return SettingsManager.shared.autoStartEnabled
        }
    }

    static func setEnabled(_ enabled: Bool) {
        if #available(macOS 13.0, *) {
            do {
                if enabled {
                    try SMAppService.mainApp.register()
                } else {
                    try SMAppService.mainApp.unregister()
                }
            } catch {
                NSLog("AutoStart error: \(error)")
            }
        } else {
            setEnabledLegacy(enabled)
        }
        SettingsManager.shared.autoStartEnabled = enabled
    }

    // Fallback for macOS 12 and earlier using LaunchAgent plist
    private static func setEnabledLegacy(_ enabled: Bool) {
        let launchAgentsDir = FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent("Library/LaunchAgents")
        let plistPath = launchAgentsDir
            .appendingPathComponent("com.discordsendguard.app.plist")

        if enabled {
            guard let appPath = Bundle.main.executablePath else { return }
            let plist: [String: Any] = [
                "Label": "com.discordsendguard.app",
                "ProgramArguments": [appPath],
                "RunAtLoad": true,
            ]
            try? FileManager.default.createDirectory(
                at: launchAgentsDir, withIntermediateDirectories: true)
            (plist as NSDictionary).write(to: plistPath, atomically: true)
        } else {
            try? FileManager.default.removeItem(at: plistPath)
        }
    }
}
