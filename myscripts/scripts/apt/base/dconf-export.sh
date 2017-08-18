#!/usr/bin/env bash
cd ~/project
git clone https://github.com/pixelastic/dconf-export.git
ln dconf-export/dconf-export ~/bin/dconf-export
sudo apt-get install -y dconf-editor
