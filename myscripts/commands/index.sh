#!/usr/bin/env bash
add-myscript-path "commands/common"
add-myscript-path "commands/docker"

add-myscript-path "commands/git"
if is-zsh; then
  source-myscript 'commands/git.zsh'
fi

source-myscript "commands/alias.sh"
