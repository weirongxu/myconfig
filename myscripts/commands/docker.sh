#!/usr/bin/env bash
exists-container() {
[[ $(docker ps -a -q -f name=$1) ]]
}
export -f exists-container
