#!/usr/bin/env bash
mkdir ~/bin
mkdir ~/program
mkdir ~/share

mv ~/公共的 ~/public
mv ~/模板 ~/template
mv ~/图片 ~/picture
mv ~/文档 ~/document
mv ~/视频 ~/video
mv ~/下载 ~/download
mv ~/音乐 ~/music
mv ~/桌面 ~/desktop
mv ~/示例 ~/example
mv ~/.config/user-dirs.dirs ~/.config/user-dirs.dirs-backup

cat > ~/.config/user-dirs.dirs << EOF
# This file is written by xdg-user-dirs-update
# If you want to change or add directories, just edit the line you're
# interested in. All local changes will be retained on the next run
# Format is XDG_xxx_DIR="$HOME/yyy", where yyy is a shell-escaped
# homedir-relative path, or XDG_xxx_DIR="/yyy", where /yyy is an
# absolute path. No other format is supported.
# 
XDG_DESKTOP_DIR="$HOME/desktop/"
XDG_DOWNLOAD_DIR="$HOME/download/"
XDG_TEMPLATES_DIR="$HOME/template/"
XDG_PUBLICSHARE_DIR="$HOME/public/"
XDG_DOCUMENTS_DIR="$HOME/document/"
XDG_MUSIC_DIR="$HOME/music/"
XDG_PICTURES_DIR="$HOME/picture/"
XDG_VIDEOS_DIR="$HOME/video/"
EOF
