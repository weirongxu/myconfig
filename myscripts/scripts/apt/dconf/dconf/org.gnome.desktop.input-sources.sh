#!/usr/bin/env sh
gsettings set org.gnome.desktop.input-sources show-all-sources "false"
gsettings set org.gnome.desktop.input-sources per-window "false"
gsettings set org.gnome.desktop.input-sources current "uint32 0"
gsettings set org.gnome.desktop.input-sources sources "[('xkb', 'cn'), ('fcitx', 'rime')]"
gsettings set org.gnome.desktop.input-sources xkb-options "['terminate:ctrl_alt_bksp', 'caps:ctrl_modifier']"