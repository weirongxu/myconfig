#!/usr/bin/env bash
try-source "/usr/local/bin/virtualenvwrapper.sh"
export WORKON_HOME="$HOME/.virtualenv"
export PYTHONPATH="$HOME/Program/pydebug/pythonlib/"
if exists-cmd brew; then
  export CFLAGS="-I$(brew --prefix openssl)/include"
  export LDFLAGS="-L$(brew --prefix openssl)/lib"
fi
if exists-cmd pyenv; then
  eval "$(pyenv init -)"
fi
