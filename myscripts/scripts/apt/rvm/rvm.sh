#!/usr/bin/env bash
# clear
sudo apt-get remove --purge ruby-rvm ruby
sudo rm -rf /usr/share/ruby-rvm /etc/rmvrc /etc/profile.d/rvm.sh
rm -rf ~/.rvm* ~/.gem/ ~/.bundle*

gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
curl -sSL https://get.rvm.io | bash -s stable --autolibs=enabled --ruby
