fish_vi_key_bindings
set -g theme_powerline_fonts no

function fish_user_key_bindings
  for mode in insert default visual
    bind -M $mode \ca beginning-of-line
    bind -M $mode \ce end-of-line
  end
end
