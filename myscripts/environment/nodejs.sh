export NVM_DIR="$HOME/.nvm"
try_source "$NVM_DIR/nvm.sh"
try_source "$NVM_DIR/bash_completion"
if exists_cmd npm; then
  add_path $(npm -g bin)
fi
