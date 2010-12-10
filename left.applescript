#!/usr/bin/osascript
tell application "System Events"
    tell process "Finder"
        key code 123 using option down --switches to space 2
    end tell
end tell