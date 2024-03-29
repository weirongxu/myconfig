#!/usr/bin/env bash
alias ptping="prettyping.sh"
alias tp="trash-put"
alias tmux="tmux -2"
alias ta="tmux attach"
alias tn="tmux new -s"
# alias tl="trash-list"
# alias te="trash-empty"

if exists-cmd 'lsd'; then
  alias ls=lsd
elif exists-cmd 'exa'; then
  alias ls=exa
  alias la="exa -laa"
fi

if exists-cmd 'batcat'; then
  alias bat="batcat"
fi

if exists-cmd 'bat'; then
  alias cat="bat -p"
fi
