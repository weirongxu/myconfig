if type -q "starship"
  starship init fish | source

  functions --copy fish_prompt fish_original_prompt

  function truncate_line
    set max_length (math $COLUMNS - 5)
    while read -l line
      set length (string replace -a -r "\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]" '' $line | string length)
      if [ $length -lt $max_length ]
        echo -e $line
      else
        set sep (string match -r '\\b(?:is|via)\\b' $line)
        if [ -n "$sep" ]
          string replace -r '\\b(?:is|via)\\b' \n$sep $line
        else
          echo $line | fmt -w $max_length
        end
      end
    end
  end

  function fish_prompt
    fish_original_prompt | truncate_line
  end
end
