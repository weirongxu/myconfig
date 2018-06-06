#!/usr/bin/env fish

if type -q "bass"
  function try-bass-source
    if test -s $argv[1]
      bass source $argv[1]
    end
  end

  function try-bass-source-myscript
    try-bass-source "$MYSCRIPTS_HOME/$argv[1]"
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
  try-bass-source "$MYSCRIPTS_HOME/myshrc"
  source-myscript "fish/git.fish"

  function myscripts
    bass source "$MYSCRIPTS_HOME/common.sh" ";" \
      source "$MYSCRIPTS_HOME/myscripts.sh" ";" \
      myscripts $argv
  end
end
