#!/usr/bin/env bash
init_root=$(pwd)
repo_path=~/repos/plum

git clone https://github.com/rime/plum $repo_path
cd $repo_path
git pull
rime_frontend=fcitx5-rime ./rime-install wubi pinyin-simp

cd $init_root
cp ./fcitx5-rime/default.custom.yaml ~/.local/share/fcitx5/rime/default.custom.yaml
