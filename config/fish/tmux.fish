function __fish_tmux_sessions -d 'available sessions'
    tmux list-sessions -F "#S	#{session_windows} windows created: #{session_created_string} [#{session_width}x#{session_height}]#{session_attached}" | sed 's/0$//;s/1$/ (attached)/' 2>/dev/null
end

alias tmux="tmux -2"
function ta
    if count $argv > /dev/null
        tmux attach -t $argv
    else
        tmux attach
    end
end
complete -c ta -a '(__fish_tmux_sessions)' -d target-session
