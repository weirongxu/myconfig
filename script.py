#!/usr/bin/env python3

import os
from typing import List

from script.cli import Cli
from script.config import Config, ConfigPath, OriginConfigPath
from script.core import env, unwrap

mpv = ConfigPath('.config/mpv/mpv.conf')

sync_paths: List[OriginConfigPath] = [
    '.config/Zeal/Zeal.conf',
    '.config/fish/conf.d/my.fish',
    '_gdbinit',
    '.ctags',
    '.gitconfig',
    '.gitignore',
    '.editorconfig',
    '.aria2/aria2.conf',

    '.config/ibus/rime/wubi_pinyin.schema.yaml',
    '.config/ibus/rime/pinyin_simp.schema.yaml',

    'document/ref/get-php-en-ref.sh',
    'document/ref/get-php-zh-ref.sh',

    '.vimrc',
    '.config/nvim/init.vim',

    '.config/starship.toml',

    '.tmux.conf.local',

    '.ideavimrc',
]

if env.isWin:
    sync_paths.append(mpv.user(os.path.join(
        unwrap(os.getenv('APPDATA')), 'mpv.conf')))
else:
    sync_paths.append(mpv)

config = Config(
    ignores=['.DS_Store'],
    sync_paths=sync_paths,
    china_sync_paths=[
        '.npmrc',
        '.composer/config.json',
        '.pip/pip.conf',
    ]
)


if __name__ == '__main__':
    Cli(config)
