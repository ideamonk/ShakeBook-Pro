#!/usr/bin/osascript
tell application "System Events"
    tell process "Finder"
        key code 124 using option down --switches to space 2
    end tell
end tell
