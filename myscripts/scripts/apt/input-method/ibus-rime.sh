#!/usr/bin/env bash
sudo apt-get install -y ibus-rime librime-data-emoji librime-data-pinyin-simp librime-data-wubi
mkdir -p ~/.config/ibus/rime/
sudo cp /usr/share/rime-data/wubi86.schema.yaml ~/.config/ibus/rime/
sudo cp /usr/share/rime-data/emoji.schema.yaml ~/.config/ibus/rime/
sudo cp /usr/share/rime-data/pinyin_simp.schema.yaml ~/.config/ibus/rime/
sudo cp /usr/share/rime-data/wubi_pinyin.schema.yaml ~/.config/ibus/rime/
sudo chown $USER ~/.config/ibus/rime
echo "add emoji wubi_pinyin to $HOME/.config/ibus/rime/default.yaml schema_list"
