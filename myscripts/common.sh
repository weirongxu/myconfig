#!/usr/bin/env bash

if [[ "$(uname)" == "Darwin" ]]; then
  export SYSTEM_TYPE='darwin'
elif [[ "$(expr substr $(uname -s) 1 5)" == "Linux" ]]; then
  export SYSTEM_TYPE='linux'
elif [[ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]]; then
  export SYSTEM_TYPE='win'
elif [[ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]]; then
  export SYSTEM_TYPE='win'
fi

if [ -n "$ZSH_VERSION" ]; then
  export SHELL_TYPE='zsh'
elif [ -n "$FISH_VERSION" ]; then
  export SHELL_TYPE='fish'
elif [ -n "$BASH_VERSION" ]; then
  export SHELL_TYPE='bash'
fi

is_zsh() {
  [[ "$SHELL_TYPE" == 'zsh' ]]
}

exists_cmd() {
  command -v $1 >/dev/null 2>&1
}

is_darwin() {
  [[ "$SYSTEM_TYPE" == 'darwin' ]]
}

is_linux() {
  [[ "$SYSTEM_TYPE" == 'linux' ]]
}

is_brew() {
  exists_cmd 'brew'
}

is_apt() {
  exists_cmd 'apt'
}

add_path() {
  if [[ -s "$1" ]]; then
    export PATH="$1:$PATH"
  fi
}

add_myscript_path() {
  add_path "$MYSCRIPTS_HOME/$1"
}

try_source() {
  if [[ -s "$1" ]]; then
    . "$1"
  fi
}

source_myscript() {
  try_source "$MYSCRIPTS_HOME/$1"
}
