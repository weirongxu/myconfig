#!/usr/bin/env fish

if type -q "bax"
  set -g BASH_RUNNER 'bax'
else if type -q "fenv"
  set -g BASH_RUNNER 'fenv'
else if type -q "bass"
  set -g BASH_RUNNER 'bass'
end

if test -n "$BASH_RUNNER"
  function try-bash-source
    if test -s $argv[1]
      $BASH_RUNNER "source $argv[1]"
    end
  end

  function try-bash-source-myscript
    try-bash-source "$MYSCRIPTS_HOME/$argv[1]"
  end

  function try-source
    if test -s $argv[1]
      . $argv[1]
    end
  end

  function source-myscript
    source "$MYSCRIPTS_HOME/$argv[1]"
  end

  $BASH_RUNNER "export CHINA_PROXY=$CHINA_PROXY >/dev/null"
  $BASH_RUNNER export MYSCRIPTS_HOME=$MYSCRIPTS_HOME

  function myscripts
    $BASH_RUNNER source "$MYSCRIPTS_HOME/common.sh" ";" \
      source "$MYSCRIPTS_HOME/myscripts.sh" ";" \
      myscripts $argv
  end

  try-bash-source "$MYSCRIPTS_HOME/myshrc"
  source-myscript "fish/index.fish"
end
