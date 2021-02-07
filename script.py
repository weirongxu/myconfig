#!/usr/bin/env python3

import argparse
import glob
import importlib
import os
import platform
import pprint
import shutil
import subprocess
import textwrap
from enum import Enum
from pathlib import PurePath
from typing import List, Literal

pp = pprint.PrettyPrinter(indent=2)


class Config():
    ignores = [
        '.DS_Store'
    ]

    sync_paths = [
        '.config/mpv/mpv.conf',
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

        '.spacemacs',
        '.ideavimrc',
    ]

    china_sync_paths = [
        '.npmrc',
        '.composer/config.json',
        '.pip/pip.conf',
    ]

def getPowerShellProfile():
    completed = subprocess.run(['powershell', '-Command', 'echo $PROFILE'], capture_output=True)
    return completed.stdout.decode().strip()


config = Config()
user_home_dir_ = os.getenv('HOME')
if user_home_dir_ is None:
    raise Exception('$HOME not found')
user_home_dir = user_home_dir_
current_dir = os.path.dirname(os.path.realpath(__file__))
if platform.system() == 'Windows':
    profile_path = getPowerShellProfile()
    if profile_path is not None:
        profile_rel_path = os.path.relpath(profile_path, user_home_dir)
        config.sync_paths.append(profile_rel_path)
    else:
        raise Exception('$PROFILE not found')


class Cli:
    class Color(Enum):
        info = '\033[34m'
        error = '\033[31m'

    @staticmethod
    def output(line: str, type: Literal['info', 'error'] = 'info'):
        print(getattr(Cli.Color, type).value + line + '\033[0m')

    def __init__(self) -> None:
        self.args = self.parse()
        if self.args.subcommand == 'update-to-home':
            self.update_to_home()
        elif self.args.subcommand == 'fetch-from-home':
            self.fetch_from_home()

    @staticmethod
    def parse():
        parser = argparse.ArgumentParser(
            prog='myconfig script', description="myconfig")
        parser.add_argument('--china',
                            type=bool,
                            default=False,
                            help='include china proxy configuration')
        subparsers = parser.add_subparsers(required=True, dest='subcommand')
        subparsers.add_parser('update-to-home')
        subparsers.add_parser('fetch-from-home')
        return parser.parse_args()

    @property
    def is_china(self) -> bool:
        return self.args.china == True

    def install_myscripts(self):
        myscripts_path = os.path.join(current_dir, 'myscripts')

        shell_script = textwrap.dedent(f"""
        export MYSCRIPTS_HOME="{myscripts_path}"
        [[ -s "$MYSCRIPTS_HOME/myshrc" ]] && . "$MYSCRIPTS_HOME/myshrc"
        """)

        if self.is_china:
            shell_script = "\nCHINA_PROXY=1\n" + shell_script

        for path in ['~/.bashrc', '~/.zshrc']:
            with open(os.path.expanduser(path), 'a+') as f:
                f.seek(0)
                if shell_script not in f.read():
                    f.write(shell_script)
                    self.output(f'Install scripts to {path}', 'info')

        fish_script = textwrap.dedent(f"""
        if status is-interactive
        set -g MYSCRIPTS_HOME "{myscripts_path}"
        if test -s "$MYSCRIPTS_HOME/myshrc.fish"
            . "$MYSCRIPTS_HOME/myshrc.fish"
        end
        end
        """)

        if self.is_china:
            shell_script = "\nset -g CHINA_PROXY 1\n" + fish_script

        fish_script_path = os.path.expanduser(
            '~/.config/fish/conf.d/myscripts.fish')
        with open(fish_script_path, 'w') as f:
            f.write(fish_script)
            self.output(
                f'Install scripts to {fish_script_path}', 'info')

    def copy_by_glob(self, source_home: str, paths: List[str], target_home: str):
        for path in paths:
            for filepath in glob.glob(os.path.join(source_home, path), recursive=True):
                if any([(ignore in filepath) for ignore in config.ignores]):
                    continue
                relative_path = PurePath(filepath).relative_to(source_home)
                target_path = os.path.join(target_home, str(relative_path))
                if os.path.isfile(filepath):
                    os.makedirs(os.path.dirname(
                        target_path), exist_ok=True)
                    shutil.copyfile(filepath, target_path,
                                    follow_symlinks=True)
                    self.output(f'COPY: {filepath} => {target_path}', 'info')

    def update_to_home(self):
        self.copy_by_glob(os.path.join(current_dir, 'home'),
                          config.sync_paths, user_home_dir)
        if self.is_china:
            self.copy_by_glob(os.path.join(
                current_dir, 'home_china'), config.china_sync_paths, user_home_dir)
        self.install_myscripts()
        self.output('Update done', 'info')

    def fetch_from_home(self):
        self.copy_by_glob(user_home_dir, config.sync_paths,
                          os.path.join(current_dir, 'home'))
        if self.is_china:
            self.copy_by_glob(user_home_dir, config.china_sync_paths,
                              os.path.join(current_dir, 'home_china'))
        self.output('Push done', 'info')


if __name__ == '__main__':
    Cli()
