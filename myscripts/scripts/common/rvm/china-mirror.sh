#!/usr/bin/env bash
cp ~/.rvm/config/db ~/.rvm/config/db.bak
sed -e 's#cache\.ruby-lang\.org/pub/ruby#cache\.ruby-china\.com/pub/ruby#g' ~/.rvm/config/db.bak > ~/.rvm/config/db
