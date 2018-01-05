#!/usr/bin/env bash
add_path "$HOME/bin"

source_myscript 'environment/android.sh'
source_myscript 'environment/java.sh'
source_myscript 'environment/nodejs.sh'
source_myscript 'environment/php.sh'
source_myscript 'environment/python.sh'
source_myscript 'environment/ruby.sh'
source_myscript 'environment/vim.sh'
source_myscript 'environment/brew.sh'
source_myscript 'environment/golang.sh'
source_myscript 'environment/rust.sh'
if [[ ! -z $CHINA_PROXY ]]; then
  source_myscript "environment/china.sh"
fi
if is_zsh; then
  source_myscript 'environment/zsh.zsh'
fi

try_source "$HOME/Programs/rc.sh"
try_source "$HOME/programs/rc.sh"
try_source "$HOME/.fzf.zsh"
