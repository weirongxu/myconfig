#!/usr/bin/env bash

export MYSCRIPTS_HOME="$1"
. "$MYSCRIPTS_HOME/common.sh"
. "$MYSCRIPTS_HOME/common-local.sh"

add-path "$HOME/bin"
add-path "$HOME/.local/bin"

source-myscript 'environment/index.sh'
source-myscript "commands/index.sh"
# source-myscript "keyboard.sh"
