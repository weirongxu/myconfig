export NVIM_LISTEN_ADDRESS="/tmp/neovim/neovim"
if exists_cmd 'vim' ; then
  export VISUAL=vim
  export EDITOR=vim
elif exists_cmd 'nvim' ; then
  export VISUAL=nvim
  export EDITOR=nvim
fi
