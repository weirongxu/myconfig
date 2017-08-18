#!/usr/bin/env bash
rm -rf dconf
mkdir dconf
cd dconf

dconf-export org.compiz.integrated
# FIXME org.compiz.profiles.unity.plugins.core cannot found?
dconf-export org.compiz.profiles.unity.plugins.core
dconf-export org.compiz.profiles.unity.plugins.unityshell
dconf-export org.gnome.desktop.input-sources
dconf-export org.gnome.desktop.wm.keybindings
dconf-export org.gnome.desktop.wm.preferences
dconf-export org.gnome.settings-daemon.plugins.media-keys
dconf-export org.freedesktop.ibus.general.hotkey
