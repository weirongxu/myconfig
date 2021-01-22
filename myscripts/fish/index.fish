set fish_greeting ""

set fish_vi_force_cursor
set fish_cursor_default     block      blink
set fish_cursor_insert      line       blink
set fish_cursor_replace_one underscore blink
set fish_cursor_visual      block

source-myscript fish/git.fish
source-myscript fish/skim.fish
source-myscript fish/starship.fish
source-myscript fish/tmux.fish
