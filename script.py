#!/usr/bin/env python3

import os
import textwrap
from typing import List

from core.cli import Cli
from core.config import Config, OriginConfigPath
from core.env import env, unwrap

sync_paths: List[OriginConfigPath] = [
    '.config/Zeal/Zeal.conf',
    '.config/fish/conf.d/my.fish',
    '.config/wezterm/wezterm.lua',
    '_gdbinit',
    '.ctags',
    '.gitconfig',
    '.gitignore',
    '.editorconfig',
    '.aria2/aria2.conf',
    '.asdfrc',
    '.config/nvim/init.vim',
    '.config/starship.toml',
    '.tmux.conf',
    '.ideavimrc',
]

china_sync_paths: List[OriginConfigPath] = [
    '.npmrc',
    '.composer/config.json',
    '.pip/pip.conf',
]

# powershell
if env.isWin:
    profile_path = unwrap(
        env.get_power_shell_var("PROFILE"), '$PROFILE')
    profile_rel_path = os.path.relpath(
        profile_path, env.user_home)
    sync_paths.append(profile_rel_path)

config = Config(
    ignores=['.DS_Store'],
    sync_paths=sync_paths,
    china_sync_paths=china_sync_paths,
)


cli = Cli(config)

if cli.subcommand == 'to-home':
    # install config
    config_path = os.path.join(env.app_root, 'config')

    shell_script = textwrap.dedent(f"""
    [[ -s "{config_path}/boot.sh" ]] && . "{config_path}/boot.sh" "{config_path}"
    """)
    cli.install_bash_script('99_myconfig.sh', shell_script)

    fish_script = textwrap.dedent(f"""
    if status is-interactive
        if test -s "{config_path}/boot.fish"
            . "{config_path}/boot.fish" "{config_path}"
        end
    end
    """)
    cli.install_fish_script('99-myconfig.fish', fish_script)
