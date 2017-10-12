#!/usr/bin/env bash
exists-container() {
  docker ps -a -q -f name=$1
}
export -f exists-container

created-container() {
  [[ $1 -ne 'rm' || $(exists-container $2) ]]
}
export -f created-container
