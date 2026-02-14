import Foundation
import CoreGraphics

final class KeyInterceptor {
    fileprivate var eventTap: CFMachPort?
    private var runLoopSource: CFRunLoopSource?
    private var tapThread: Thread?
    private var tapRunLoop: CFRunLoop?

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
            if let runLoop = tapRunLoop {
                CFRunLoopStop(runLoop)
            }
            eventTap = nil
            runLoopSource = nil
            tapRunLoop = nil
        }
    }

    private func setupEventTap() {
        let eventMask: CGEventMask = (1 << CGEventType.keyDown.rawValue)
        let selfPtr = Unmanaged.passUnretained(self).toOpaque()

        guard let tap = CGEvent.tapCreate(
            tap: .cgSessionEventTap,
            place: .headInsertEventTap,
            options: .defaultTap,
            eventsOfInterest: eventMask,
            callback: keyCallback,
            userInfo: selfPtr
        ) else {
            DispatchQueue.main.async {
                PermissionManager.showPermissionGuide()
            }
            return
        }

        eventTap = tap
        tapRunLoop = CFRunLoopGetCurrent()
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
    // タップがタイムアウトで無効化された場合、再有効化する
    if type == .tapDisabledByTimeout || type == .tapDisabledByUserInput {
        if let refcon = refcon {
            let interceptor = Unmanaged<KeyInterceptor>.fromOpaque(refcon).takeUnretainedValue()
            if let tap = interceptor.eventTap {
                CGEvent.tapEnable(tap: tap, enable: true)
            }
        }
        return Unmanaged.passRetained(event)
    }

    guard type == .keyDown else {
        return Unmanaged.passRetained(event)
    }

    guard SettingsManager.shared.guardEnabled else {
        return Unmanaged.passRetained(event)
    }

    let keyCode = event.getIntegerValueField(.keyboardEventKeycode)
    guard keyCode == 36 else {
        return Unmanaged.passRetained(event)
    }

    guard DiscordDetector.isDiscordFront else {
        return Unmanaged.passRetained(event)
    }

    let flags = event.flags
    if flags.contains(.maskCommand) {
        return Unmanaged.passRetained(event)
    }

    // Enter without Cmd in Discord: Shift+Enter に変換して改行にする
    event.flags = flags.union(.maskShift)
    return Unmanaged.passRetained(event)
}
