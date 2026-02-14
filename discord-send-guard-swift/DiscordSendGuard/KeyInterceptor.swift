import Foundation
import CoreGraphics

final class KeyInterceptor {
    private var eventTap: CFMachPort?
    private var runLoopSource: CFRunLoopSource?
    private var tapThread: Thread?

    var isRunning: Bool {
        return eventTap != nil
    }

    func start() {
        guard eventTap == nil else { return }

        tapThread = Thread {
            self.setupEventTap()
            CFRunLoopRun()
        }
        tapThread?.name = "KeyInterceptor"
        tapThread?.start()
    }

    func stop() {
        if let tap = eventTap {
            CGEvent.tapEnable(tap: tap, enable: false)
            if let source = runLoopSource {
                CFRunLoopSourceInvalidate(source)
            }
            eventTap = nil
            runLoopSource = nil
        }
    }

    private func setupEventTap() {
        let eventMask: CGEventMask = (1 << CGEventType.keyDown.rawValue)

        guard let tap = CGEvent.tapCreate(
            tap: .cgSessionEventTap,
            place: .headInsertEventTap,
            options: .defaultTap,
            eventsOfInterest: eventMask,
            callback: keyCallback,
            userInfo: nil
        ) else {
            DispatchQueue.main.async {
                PermissionManager.showPermissionGuide()
            }
            return
        }

        eventTap = tap
        runLoopSource = CFMachPortCreateRunLoopSource(kCFAllocatorDefault, tap, 0)
        CFRunLoopAddSource(CFRunLoopGetCurrent(), runLoopSource, .commonModes)
        CGEvent.tapEnable(tap: tap, enable: true)
    }
}

private func keyCallback(
    proxy: CGEventTapProxy,
    type: CGEventType,
    event: CGEvent,
    refcon: UnsafeMutableRawPointer?
) -> Unmanaged<CGEvent>? {
    // If the tap is disabled by the system, re-enable it
    if type == .tapDisabledByTimeout || type == .tapDisabledByUserInput {
        return Unmanaged.passRetained(event)
    }

    // Only process keyDown events
    guard type == .keyDown else {
        return Unmanaged.passRetained(event)
    }

    // Check if guard is enabled
    guard SettingsManager.shared.guardEnabled else {
        return Unmanaged.passRetained(event)
    }

    // Only intercept Enter key (keyCode 36)
    let keyCode = event.getIntegerValueField(.keyboardEventKeycode)
    guard keyCode == 36 else {
        return Unmanaged.passRetained(event)
    }

    // Only intercept when Discord is frontmost
    guard DiscordDetector.isDiscordFrontmost() else {
        return Unmanaged.passRetained(event)
    }

    // If Cmd is held, allow the send (pass through)
    let flags = event.flags
    if flags.contains(.maskCommand) {
        return Unmanaged.passRetained(event)
    }

    // Enter without Cmd in Discord: add Shift flag to convert to newline
    event.flags = flags.union(.maskShift)
    return Unmanaged.passRetained(event)
}
