APP_NAME = DiscordSendGuard
BUILD_DIR = build
APP_BUNDLE = $(BUILD_DIR)/$(APP_NAME).app
CONTENTS = $(APP_BUNDLE)/Contents
MACOS = $(CONTENTS)/MacOS
RESOURCES = $(CONTENTS)/Resources

SOURCES = $(wildcard DiscordSendGuard/*.swift)
PLIST = DiscordSendGuard/Info.plist

SWIFT_FLAGS = -O -target arm64-apple-macos12

.PHONY: build clean run

build: $(MACOS)/$(APP_NAME)

$(MACOS)/$(APP_NAME): $(SOURCES) $(PLIST)
	@mkdir -p $(MACOS) $(RESOURCES)
	swiftc $(SWIFT_FLAGS) $(SOURCES) -o $(MACOS)/$(APP_NAME)
	@cp $(PLIST) $(CONTENTS)/Info.plist
	@echo "Build complete: $(APP_BUNDLE)"

run: build
	@open $(APP_BUNDLE)

clean:
	rm -rf $(BUILD_DIR)
