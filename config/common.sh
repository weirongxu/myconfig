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

is-bash() {
  [[ "$SHELL_TYPE" == 'bash' ]]
}

is-zsh() {
  [[ "$SHELL_TYPE" == 'zsh' ]]
}

is-fish() {
  [[ "$SHELL_TYPE" == 'fish' ]]
}

exists-cmd() {
  command -v $1 >/dev/null 2>&1
}

is-darwin() {
  [[ "$SYSTEM_TYPE" == 'darwin' ]]
}

is-linux() {
  [[ "$SYSTEM_TYPE" == 'linux' ]]
}

is-brew() {
  exists-cmd 'brew'
}

is-apt() {
  exists-cmd 'apt'
}

has-path() {
  [[ ":$PATH:" == *":$1:"* ]]
}

add-path() {
  if [[ -d "$1" ]]; then
    export PATH="$1:$PATH"
  fi
}

try-source() {
  if [[ -s "$1" ]]; then
    . "$1"
  fi
}
