#!/usr/bin/env bash
sudo add-apt-repository -y ppa:pipelight/stable
sudo apt-get update
sudo apt-get install -y --install-recommends pipelight-multi
sudo pipelight-plugin --update
