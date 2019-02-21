#!/usr/bin/env bash
add-path "$HOME/bin"
add-path "$HOME/.local/bin"

source-myscript 'environment/index.sh'
try-source "$HOME/apps/rc.sh"
