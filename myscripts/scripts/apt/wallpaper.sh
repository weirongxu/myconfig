#!/usr/bin/env bash
sudo add-apt-repository -y ppa:peterlevi/ppa
sudo apt-get update
sudo apt-get install -y variety

gem install hb_exporter
