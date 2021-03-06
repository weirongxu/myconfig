if type -q "starship"
  starship init fish | source

  functions --copy fish_prompt fish_original_prompt

  function truncate_line
    set max_length $argv[1]
    while read -l line
      set length (string replace -a -r "\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]" '' $line | string length)
      if [ $length -lt $max_length ]
        echo $line
      else
        set sep (string match -r '\\s(is|via)\\b' $line)[-1]
        if [ -n "$sep" ]
          set result (string replace -r '\\s(?:is|via)\\b' \n$sep $line)
          echo $result[1] | truncate_line $max_length
          echo $result[-1] | truncate_line $max_length
        else
          echo $line | fmt -w $max_length
        end
      end
    end
  end

  function fish_prompt
    fish_original_prompt | truncate_line (math $COLUMNS)
  end
end
