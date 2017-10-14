#!/usr/bin/env bash
sudo apt-get install -y fcitx-rime librime-data-emoji librime-data-pinyin-simp librime-data-wubi
mkdir -p ~/.config/fcitx/rime/
sudo cp /usr/share/rime-data/wubi86.schema.yaml ~/.config/fcitx/rime/
sudo cp /usr/share/rime-data/emoji.schema.yaml ~/.config/fcitx/rime/
sudo cp /usr/share/rime-data/pinyin_simp.schema.yaml ~/.config/fcitx/rime/
sudo cp /usr/share/rime-data/wubi_pinyin.schema.yaml ~/.config/fcitx/rime/
sudo chown $USER ~/.config/fcitx/rime
echo "add emoji wubi_pinyin to $HOME/.config/fcitx/rime/default.yaml schema_list"
