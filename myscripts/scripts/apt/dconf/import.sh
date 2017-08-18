#!/usr/bin/env bash

dconf write /org/compiz/profiles/unity/plugins/core/hsize 2
dconf write /org/compiz/profiles/unity/plugins/core/vsize 3

dconf write /org/compiz/profiles/unity/plugins/unityshell/icon-size 35

dconf write /org/compiz/profiles/unity/plugins/unityshell/show-launcher '"<Super>space"'

for script in `ls dconf`; do
    ./dconf/$script
done
