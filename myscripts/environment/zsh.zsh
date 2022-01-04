#!/usr/bin/env zsh

autoload -U +X bashcompinit && bashcompinit
autoload -U +X compinit && compinit

zstyle ':completion:*' menu yes select
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'

HISTFILE=~/.zsh_history
HISTSIZE=1000
SAVEHIST=1000
WORDCHARS='*?_-.[]~=&;!#$%^(){}<>'

setopt appendhistory
setopt auto_cd
setopt multios

if exists-cmd zinit; then
  zinit light zdharma/fast-syntax-highlighting
  zinit light zsh-users/zsh-autosuggestions
  zinit light zsh-users/zsh-completions
  zinit load agkozak/zsh-z

  zinit snippet OMZ::lib/directories.zsh

  zinit snippet OMZP::git
  zinit snippet OMZP::git-extras
  zinit ice as"program"
  zinit load https://github.com/k4rthik/git-cal

  zinit snippet OMZP::extract

  zinit ice lucid wait
  zinit snippet OMZP::fzf

  # zinit ice as"completion"
  # zinit snippet OMZ::plugins/rustup/_rustup
  # zinit ice as"completion"
  # zinit snippet OMZ::plugins/rust/_rust
  # zinit ice as"completion"
  # zinit snippet OMZ::plugins/cargo/_cargo

  # zinit load softmoth/zsh-vim-mode
  zinit load jeffreytse/zsh-vi-mode
  ZVM_VI_SURROUND_BINDKEY=s-prefix
fi

function zsh_stats() {
  fc -l 1 \
    | awk '{ CMD[$2]++; count++; } END { for (a in CMD) print CMD[a] " " CMD[a]*100/count "% " a }' \
    | grep -v "./" | sort -nr | head -n 20 | column -c3 -s " " -t | nl
}
