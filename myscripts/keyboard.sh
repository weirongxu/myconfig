if ! is-darwin && exists-cmd 'setxkbmap'; then
  setxkbmap -option "caps:ctrl_modifier"
fi
