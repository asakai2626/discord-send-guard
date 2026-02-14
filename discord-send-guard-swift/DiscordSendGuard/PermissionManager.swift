import AppKit
import ApplicationServices

struct PermissionManager {
    static func isTrusted() -> Bool {
        return AXIsProcessTrusted()
    }

    static func requestPermission() {
        let options = [kAXTrustedCheckOptionPrompt.takeUnretainedValue(): true] as CFDictionary
        AXIsProcessTrustedWithOptions(options)
    }

    static func showPermissionGuide() {
        let alert = NSAlert()
        alert.messageText = "Accessibility権限が必要です"
        alert.informativeText = """
        Discord Send Guardがキーボード入力を制御するには、\
        Accessibility権限が必要です。

        「システム設定を開く」をクリックして、\
        Discord Send Guardにチェックを入れてください。
        """
        alert.alertStyle = .warning
        alert.addButton(withTitle: "システム設定を開く")
        alert.addButton(withTitle: "キャンセル")

        let response = alert.runModal()
        if response == .alertFirstButtonReturn {
            openAccessibilitySettings()
        }
    }

    static func openAccessibilitySettings() {
        if let url = URL(string: "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility") {
            NSWorkspace.shared.open(url)
        }
    }
}
