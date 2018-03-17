export NVIM_LISTEN_ADDRESS="/tmp/neovim"
if exists-cmd 'nvim' ; then
  export VISUAL=nvim
  export EDITOR=nvim
elif exists-cmd 'vim' ; then
  export VISUAL=vim
  export EDITOR=vim
fi
