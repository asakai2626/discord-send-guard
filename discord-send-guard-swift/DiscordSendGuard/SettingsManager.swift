import Foundation

final class SettingsManager {
    static let shared = SettingsManager()

    private let defaults = UserDefaults.standard

    private enum Keys {
        static let guardEnabled = "guardEnabled"
        static let autoStartEnabled = "autoStartEnabled"
    }

    var guardEnabled: Bool {
        get { defaults.object(forKey: Keys.guardEnabled) as? Bool ?? true }
        set { defaults.set(newValue, forKey: Keys.guardEnabled) }
    }

    var autoStartEnabled: Bool {
        get { defaults.bool(forKey: Keys.autoStartEnabled) }
        set { defaults.set(newValue, forKey: Keys.autoStartEnabled) }
    }

    private init() {}
}
