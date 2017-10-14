#!/usr/bin/env sh
gsettings set org.freedesktop.ibus.general.hotkey next-engine "['Alt+Shift_L']"
gsettings set org.freedesktop.ibus.general.hotkey disable-unconditional "['']"
gsettings set org.freedesktop.ibus.general.hotkey enable-unconditional "['']"
gsettings set org.freedesktop.ibus.general.hotkey trigger "['Control+space', 'Zenkaku_Hankaku', 'Alt+Kanji', 'Alt+grave', 'Hangul', 'Alt+Release+Alt_R']"
gsettings set org.freedesktop.ibus.general.hotkey previous-engine "['']"
gsettings set org.freedesktop.ibus.general.hotkey prev-engine "['']"
gsettings set org.freedesktop.ibus.general.hotkey next-engine-in-menu "['Alt+Shift_L']"
gsettings set org.freedesktop.ibus.general.hotkey triggers "['<Super>space']"