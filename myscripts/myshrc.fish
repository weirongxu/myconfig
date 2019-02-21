#!/usr/bin/env fish

if type -q "fenv"
  function try-bash-source
    if test -s $argv[1]
      fenv source $argv[1]
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
    try-source "$MYSCRIPTS_HOME/$argv[1]"
  end

  fenv export CHINA_PROXY=$CHINA_PROXY >/dev/null
  fenv export MYSCRIPTS_HOME=$MYSCRIPTS_HOME
  try-bash-source "$MYSCRIPTS_HOME/myshrc"

  function myscripts
    fenv source "$MYSCRIPTS_HOME/common.sh" ";" \
      source "$MYSCRIPTS_HOME/myscripts.sh" ";" \
      myscripts $argv
  end
else if type -q "bass"
  function try-bash-source
    if test -s $argv[1]
      bass source $argv[1]
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
    try-source "$MYSCRIPTS_HOME/$argv[1]"
  end

  bass export CHINA_PROXY=$CHINA_PROXY >/dev/null
  bass export MYSCRIPTS_HOME=$MYSCRIPTS_HOME

  function myscripts
    bass source "$MYSCRIPTS_HOME/common.sh" ";" \
      source "$MYSCRIPTS_HOME/myscripts.sh" ";" \
      myscripts $argv
  end
end

if type -q try-bash-source
  try-bash-source "$MYSCRIPTS_HOME/myshrc"
  source-myscript "fish/index.fish"
end
