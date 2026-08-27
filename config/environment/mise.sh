#!/usr/bin/env bash

if exists-cmd 'mise'; then
  if is-zsh; then
    eval "$(mise activate zsh)"
  else
    eval "$(mise activate bash)"
  fi
fi
