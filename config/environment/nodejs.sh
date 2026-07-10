# export NVM_DIR="$HOME/.nvm"
# if ! is-fish; then
#   try-source "$NVM_DIR/nvm.sh"
#   try-source "$NVM_DIR/bash_completion"
# fi
if exists-cmd npm; then
  add-path "$(npm config get prefix)/bin"
fi
