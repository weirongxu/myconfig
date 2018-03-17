export NVM_DIR="$HOME/.nvm"
try-source "$NVM_DIR/nvm.sh"
try-source "$NVM_DIR/bash_completion"
if exists-cmd npm; then
  add-path $(npm -g bin)
fi
