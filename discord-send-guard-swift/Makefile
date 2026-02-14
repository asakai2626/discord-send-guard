APP_NAME = DiscordSendGuard
BUILD_DIR = build
APP_BUNDLE = $(BUILD_DIR)/$(APP_NAME).app
CONTENTS = $(APP_BUNDLE)/Contents
MACOS = $(CONTENTS)/MacOS
RESOURCES = $(CONTENTS)/Resources

SOURCES = $(wildcard DiscordSendGuard/*.swift)
PLIST = DiscordSendGuard/Info.plist

ARCH = $(shell uname -m)
SWIFT_FLAGS = -O -target $(ARCH)-apple-macos12
ENTITLEMENTS = DiscordSendGuard/DiscordSendGuard.entitlements

.PHONY: build clean run

build: $(MACOS)/$(APP_NAME)

$(MACOS)/$(APP_NAME): $(SOURCES) $(PLIST)
	@mkdir -p $(MACOS) $(RESOURCES)
	swiftc $(SWIFT_FLAGS) $(SOURCES) -o $(MACOS)/$(APP_NAME)
	@cp $(PLIST) $(CONTENTS)/Info.plist
	@codesign --force --deep --sign - --entitlements $(ENTITLEMENTS) $(APP_BUNDLE)
	@echo "Build complete: $(APP_BUNDLE)"

run: build
	@open $(APP_BUNDLE)

clean:
	rm -rf $(BUILD_DIR)
