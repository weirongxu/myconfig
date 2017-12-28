#!/usr/bin/env bash
add_path "$HOME/bin"

source_myscript 'variables/android.sh'
source_myscript 'variables/java.sh'
source_myscript 'variables/nodejs.sh'
source_myscript 'variables/php.sh'
source_myscript 'variables/python.sh'
source_myscript 'variables/ruby.sh'
source_myscript 'variables/vim.sh'
source_myscript 'variables/brew.sh'
if [[ ! -z $CHINA_PROXY ]]; then
  source_myscript "variables/china.sh"
fi
if is_zsh; then
  source_myscript 'variables/zsh.zsh'
fi

try_source "$HOME/Programs/rc.sh"
try_source "$HOME/programs/rc.sh"
try_source "$HOME/.fzf.zsh"
