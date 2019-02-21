#!/usr/bin/env bash
source-myscript 'environment/brew.sh'
source-myscript 'environment/android.sh'
source-myscript 'environment/java.sh'
source-myscript 'environment/nodejs.sh'
source-myscript 'environment/php.sh'
source-myscript 'environment/python.sh'
source-myscript 'environment/ruby.sh'
source-myscript 'environment/vim.sh'
source-myscript 'environment/golang.sh'
source-myscript 'environment/rust.sh'
if [[ ! -z $CHINA_PROXY ]]; then
  source-myscript "environment/china.sh"
fi
if is-zsh; then
  source-myscript 'environment/zsh.zsh'
  try-source "$HOME/.fzf.zsh"
  try-source /usr/share/skim/key-bindings.zsh
else
  try-source /usr/share/skim/key-bindings.bash
fi
