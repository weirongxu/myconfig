#!/usr/bin/env bash
export LANG=en_US.UTF-8
export LC_CTYPE=en_US.UTF-8
source-myscript 'environment/asdf.sh'
source-myscript 'environment/linux-brew.sh'
source-myscript 'environment/macos-port.sh'
source-myscript 'environment/android.sh'
source-myscript 'environment/java.sh'
source-myscript 'environment/llvm.sh'
source-myscript 'environment/dart.sh'
source-myscript 'environment/nodejs.sh'
source-myscript 'environment/php.sh'
source-myscript 'environment/python.sh'
source-myscript 'environment/ruby.sh'
source-myscript 'environment/vim.sh'
source-myscript 'environment/golang.sh'
source-myscript 'environment/rust.sh'
source-myscript 'environment/starship.sh'
if [[ ! -z $CHINA_PROXY ]]; then
  source-myscript 'environment/china.sh'
fi
if is-zsh; then
  source-myscript 'environment/zsh.zsh'
  try-source "$HOME/.fzf.zsh"
  try-source /usr/share/skim/key-bindings.zsh
else
  try-source /usr/share/skim/key-bindings.bash
fi
if [[ -z $XDG_CACHE_HOME ]]; then
  export XDG_CACHE_HOME="$HOME/.cache"
fi
