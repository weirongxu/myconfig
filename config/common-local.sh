#!/usr/bin/env bash

add-myscript-path() {
  add-path "$MYSCRIPTS_HOME/$1"
}

source-myscript() {
  source "$MYSCRIPTS_HOME/$1"
}
