#!/usr/bin/env bash
sudo add-apt-repository -y ppa:ondrej/php5
sudo add-apt-repository -y ppa:nginx/stable
apt-get update

sudo apt-get install -y --force-yes php5-cli php5-fpm php5-mysql php5-pgsql php5-sqlite php5-curl\
                     php5-gd php5-mcrypt php5-intl php5-imap php5-tidy
