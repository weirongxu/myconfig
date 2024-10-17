#!/usr/bin/env bash
init_root=$(pwd)
repo_path=~/repos/plum

git clone https://github.com/rime/plum $repo_path
cd $repo_path
git pull
rime_dir="/usr/share/rime-data" ./rime-install wubi pinyin-simp

cd $init_root
cp ./rime/default.custom.yaml /usr/share/rime-data/default.custom.yaml
