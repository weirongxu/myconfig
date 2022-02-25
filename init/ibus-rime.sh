#!/usr/bin/env bash
init_root=$(pwd)
repo_path=~/repos/plum

git clone https://github.com/rime/plum $repo_path
cd $repo_path
git pull
rime_frontend=ibus-rime ./rime-install wubi pinyin-simp

cd $init_root
cp ./rime/default.custom.yaml ~/.config/ibus/rime/default.custom.yaml
