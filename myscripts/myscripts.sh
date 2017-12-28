#!/usr/bin/env bash

MYSCRIPTS_SCRIPTS_DIR="$MYSCRIPTS_HOME/scripts"

_mysciprts_help() {
  cat <<-EOF
commands list
  run <name>        run some program
  cat <name>        cat some program
  list              list all program
  help              display help
EOF
  _myscripts_list $*
}

_myscripts_scripts_path_root() {
  if is_linux; then
    echo "$MYSCRIPTS_SCRIPTS_DIR/linux"
  fi
  if is_darwin; then
    echo "$MYSCRIPTS_SCRIPTS_DIR/darwin"
  fi
  if is_apt; then
    echo "$MYSCRIPTS_SCRIPTS_DIR/apt"
  fi
  if is_brew; then
    echo "$MYSCRIPTS_SCRIPTS_DIR/brew"
  fi
  echo "$MYSCRIPTS_SCRIPTS_DIR/common"
}

_myscripts_list_all() {
  all_path() {
    for _path in $(_myscripts_scripts_path_root); do
      if [ -d $_path  ]; then
        find $_path -type f -print | sed -e "s;^$_path/;;g;"
      fi
    done
  }
  all_path | sed -e 's;\..*?$;;g;s;.*\.DS_Store.*;;' | sed '/^\s*$/d' \
    | sed -e 's;^;  - ;' | sort | uniq
}

_myscripts_list() {
  echo 'runner list'
  if [[ "$1" == "--all" ]]; then
    _myscripts_list_all
  else
    _myscripts_list_all | sed -n 1,15p
    echo '  - ...'
  fi
}

_myscripts_command_list() {
  cat <<-EOF
run
cat
list
help
EOF
}

_myscripts_scripts_exts=(sh py fish)
_myscripts_scripts_path() {
  for _path in $(_myscripts_scripts_path_root); do
    for ext in ${_myscripts_scripts_exts[@]}; do
      if [[ -f "$_path/$1.$ext" ]]; then
        echo "$_path/$1.$ext"
        return
      fi
    done
  done
}

_myscripts_cat() {
  if [[ -z "$1" ]]; then
    _mysciprts_help
    return
  fi
  local _path="$(_myscripts_scripts_path $1)"
  if [[ ! -z "$_path"  ]]; then
    cat "$_path"
  else
    echo "cat name '$1' not exists"
  fi
}

_myscripts_run() {
  if [[ -z "$1" ]]; then
    _mysciprts_help
    return
  fi
  local _path="$(_myscripts_scripts_path $1)"
  if [[ ! -z "$_path"  ]]; then
    "$_path"
  else
    echo "run name '$1' not exists"
  fi
}

myscripts() {
  if [[ -z $1 ]]; then
    _mysciprts_help
  else
    case "$1" in
      "run")
        _myscripts_run $2
        ;;
      "cat")
        _myscripts_cat $2
        ;;
      "list")
        _myscripts_list --all
        ;;
      "command-list")
        _myscripts_command_list
        ;;
      "help")
        _mysciprts_help
        ;;
      *)
        echo "command $1 not found"
    esac
  fi
}

# function __myscripts_completion() {
#   __myscripts_name_list() {
#     find $MYSCRIPTS_SCRIPTS_DIR -type f -print | sed -e "s;^$MYSCRIPTS_SCRIPTS_DIR/;;g;s;\\.*?$;;g"
#   }
#   case $CURRENT in
#     0) # myscripts $1
#       compadd -- "$(myscripts command-list)"
#       ;;
#     1)  # myscripts run
#       if [[ $words[1] == 'run' ]]; then
#         compadd -- "$(__myscripts_name_list)"
#       fi
#       ;;
#   esac
# }

# compdef __myscripts_completion myscripts
