try-source $HOME/.asdf/asdf.sh
if is-zsh; then
  fpath=(${ASDF_DIR}/completions $fpath)
fi
