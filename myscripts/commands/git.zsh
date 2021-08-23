zstyle -g existing_user_commands ':completion:*:*:git:*' user-commands
zstyle ':completion:*:*:git:*' user-commands $existing_user_commands \
  pr-merge:'merge a pull request locally' \
  pr-rebase:'rebase a pull request locally'
