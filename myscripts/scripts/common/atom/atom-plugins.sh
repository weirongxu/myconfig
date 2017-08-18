#!/usr/bin/env bash
plugins=(
  activate-power-mode
  atom-keyboard-macros-vim
  ex-mode
  git-plus
  git-time-machine
  language-plantuml
  language-viml
  plantuml-viewer
  platformio-ide-terminal
  project-plus
  symbols-tree-view
  video-player
  vim-mode-plus
  vim-mode-plus-keymaps-for-surround
  emmet
)
for plugin in "${plugins[@]}"; do
  apm install $plugin
done
