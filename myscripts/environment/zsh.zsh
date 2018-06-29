#!/usr/bin/env zsh

fpath+=~/.zfunc

try-source /etc/zsh_command_not_found

if exists-cmd upgrade_oh_my_zsh; then
  local plugins=(
    git git-extras
    composer laravel
    node npm nvm
    pip python
    rvm rails bundler rake gem
    zsh-autosuggestions zsh-syntax-highlighting
    z dircycle
    extract
    rsync
    vi-mode
    themes nyan
  )

  for plugin ($plugins); do
    if is_plugin $ZSH_CUSTOM $plugin; then
      fpath=($ZSH_CUSTOM/plugins/$plugin $fpath)
    elif is_plugin $ZSH $plugin; then
      fpath=($ZSH/plugins/$plugin $fpath)
    fi
  done

  # Figure out the SHORT hostname
  if [[ "$OSTYPE" = darwin* ]]; then
    # macOS $HOST changes with dhcp, etc. Use ComputerName if possible.
    SHORT_HOST=$(scutil --get ComputerName 2>/dev/null) || SHORT_HOST=${HOST/.*/}
  else
    SHORT_HOST=${HOST/.*/}
  fi

  # Save the location of the current completion dump file.
  if [ -z "$ZSH_COMPDUMP" ]; then
    ZSH_COMPDUMP="${ZDOTDIR:-${HOME}}/.zcompdump-${SHORT_HOST}-${ZSH_VERSION}"
  fi

  if [[ $ZSH_DISABLE_COMPFIX != true ]]; then
    # If completion insecurities exist, warn the user without enabling completions.
    if ! compaudit &>/dev/null; then
      # This function resides in the "lib/compfix.zsh" script sourced above.
      handle_completion_insecurities
    # Else, enable and cache completions to the desired file.
    else
      compinit -d "${ZSH_COMPDUMP}"
    fi
  else
    compinit -i -d "${ZSH_COMPDUMP}"
  fi

  for plugin ($plugins); do
    if [ -f $ZSH_CUSTOM/plugins/$plugin/$plugin.plugin.zsh ]; then
      source $ZSH_CUSTOM/plugins/$plugin/$plugin.plugin.zsh
    elif [ -f $ZSH/plugins/$plugin/$plugin.plugin.zsh ]; then
      source $ZSH/plugins/$plugin/$plugin.plugin.zsh
    fi
  done

  ZSH_THEME="re5et"
  if [ -f "$ZSH_CUSTOM/$ZSH_THEME.zsh-theme" ]; then
    source "$ZSH_CUSTOM/$ZSH_THEME.zsh-theme"
  elif [ -f "$ZSH_CUSTOM/themes/$ZSH_THEME.zsh-theme" ]; then
    source "$ZSH_CUSTOM/themes/$ZSH_THEME.zsh-theme"
  else
    source "$ZSH/themes/$ZSH_THEME.zsh-theme"
  fi
fi
