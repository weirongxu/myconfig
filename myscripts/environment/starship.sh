if is-zsh; then
  eval "$(starship init zsh)"
elif ! is-fish; then
  eval "$(starship init bash)"
fi
