#!/usr/bin/env bash
try-source "/usr/local/bin/virtualenvwrapper.sh"
export WORKON_HOME="$HOME/.virtualenv"
export PYTHONPATH="$HOME/Program/pydebug/pythonlib/"
if exists-cmd brew; then
  export CFLAGS="-I$(brew --prefix openssl)/include"
  export LDFLAGS="-L$(brew --prefix openssl)/lib"
fi
add-path $(pyenv root)/shims
