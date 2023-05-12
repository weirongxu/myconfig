#!/usr/bin/env bash
add-path "$HOME/.dotnet/tools"

if is-zsh; then
  _dotnet_zsh_complete()
  {
    local completions=("$(dotnet complete "$words")")

    # If the completion list is empty, just continue with filename selection
    if [ -z "$completions" ]
    then
      _arguments '*::arguments: _normal'
      return
    fi

    # This is not a variable assignment, don't remove spaces!
    _values = "${(ps:\n:)completions}"
  }

  compdef _dotnet_zsh_complete dotnet
else if is-bash
  function _dotnet_bash_complete()
  {
    local cur="${COMP_WORDS[COMP_CWORD]}" IFS=$'\n'
    local candidates

    read -d '' -ra candidates < <(dotnet complete --position "${COMP_POINT}" "${COMP_LINE}" 2>/dev/null)

    read -d '' -ra COMPREPLY < <(compgen -W "${candidates[*]:-}" -- "$cur")
  }

  complete -f -F _dotnet_bash_complete dotnet
fi
