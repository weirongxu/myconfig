if type -q "starship"
  starship init fish | source

  functions --copy fish_prompt fish_original_prompt

  function truncate_line
    set max_length (echo $COLUMNS "- 5" | bc)
    while read -l line
      set length (echo $line | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[mGK]//g" | wc -L)
      if [ $length -lt $max_length ]
        echo -e $line
      else
        set sep (string match -r 'is|via' $line)
        if [ -n $sep ]
          string replace $sep \n$sep $line
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
