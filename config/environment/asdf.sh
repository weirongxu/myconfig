try-source $HOME/.asdf/asdf.sh
add-path "${ASDF_DATA_DIR:-$HOME/.asdf}/shims"
if is-zsh; then
  fpath=(${ASDF_DIR}/completions $fpath)
fi
