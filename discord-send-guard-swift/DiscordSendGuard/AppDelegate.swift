import AppKit

final class AppDelegate: NSObject, NSApplicationDelegate {
    private var statusItem: NSStatusItem!
    private let keyInterceptor = KeyInterceptor()

    func applicationDidFinishLaunching(_ notification: Notification) {
        setupStatusItem()
        checkPermissionAndStart()
    }

    func applicationWillTerminate(_ notification: Notification) {
        keyInterceptor.stop()
    }

    // MARK: - Status Bar

    private func setupStatusItem() {
        statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)

        if let button = statusItem.button {
            button.image = NSImage(
                systemSymbolName: "shield.checkered",
                accessibilityDescription: "Discord Send Guard"
            )
        }

        updateMenu()
    }

    private func updateMenu() {
        let menu = NSMenu()

        // Status
        let statusText = SettingsManager.shared.guardEnabled ? "✓ ガード有効" : "✗ ガード無効"
        let statusItem = NSMenuItem(title: statusText, action: nil, keyEquivalent: "")
        statusItem.isEnabled = false
        menu.addItem(statusItem)

        menu.addItem(NSMenuItem.separator())

        // Toggle
        let toggleTitle = SettingsManager.shared.guardEnabled ? "ガードを無効にする" : "ガードを有効にする"
        let toggleItem = NSMenuItem(title: toggleTitle, action: #selector(toggleGuard), keyEquivalent: "")
        toggleItem.target = self
        menu.addItem(toggleItem)

        menu.addItem(NSMenuItem.separator())

        // Auto start
        let autoStartItem = NSMenuItem(
            title: "ログイン時に起動",
            action: #selector(toggleAutoStart),
            keyEquivalent: ""
        )
        autoStartItem.target = self
        autoStartItem.state = AutoStartManager.isEnabled ? .on : .off
        menu.addItem(autoStartItem)

        menu.addItem(NSMenuItem.separator())

        // Permission check
        let permItem = NSMenuItem(
            title: "権限を確認...",
            action: #selector(checkPermission),
            keyEquivalent: ""
        )
        permItem.target = self
        menu.addItem(permItem)

        menu.addItem(NSMenuItem.separator())

        // Quit
        let quitItem = NSMenuItem(title: "終了", action: #selector(quit), keyEquivalent: "q")
        quitItem.target = self
        menu.addItem(quitItem)

        self.statusItem.menu = menu
    }

    // MARK: - Actions

    @objc private func toggleGuard() {
        let settings = SettingsManager.shared
        settings.guardEnabled = !settings.guardEnabled

        if settings.guardEnabled {
            keyInterceptor.start()
        } else {
            keyInterceptor.stop()
        }

        updateMenu()
    }

    @objc private func toggleAutoStart() {
        let newValue = !AutoStartManager.isEnabled
        AutoStartManager.setEnabled(newValue)
        updateMenu()
    }

    @objc private func checkPermission() {
        if PermissionManager.isTrusted() {
            let alert = NSAlert()
            alert.messageText = "権限OK"
            alert.informativeText = "Accessibility権限は付与されています。"
            alert.alertStyle = .informational
            alert.runModal()
        } else {
            PermissionManager.showPermissionGuide()
        }
    }

    @objc private func quit() {
        NSApplication.shared.terminate(nil)
    }

    // MARK: - Startup

    private func checkPermissionAndStart() {
        if !PermissionManager.isTrusted() {
            PermissionManager.requestPermission()
        }

        if SettingsManager.shared.guardEnabled {
            keyInterceptor.start()
        }
    }
}
