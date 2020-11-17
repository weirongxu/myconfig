#!/usr/bin/env python3

import glob
import os
import shutil
from enum import Enum
from pathlib import PurePath
import argparse
import textwrap
from typing import List


class Config():
    ignores = [
        '.DS_Store'
    ]

    sync_paths = [
        '.config/mpv/mpv.conf',
        '.config/variety/variety.conf',
        '.config/Zeal/Zeal.conf',
        '.config/fish/conf.d/my.fish',
        '_gdbinit',
        '.ctags',
        '.gitconfig',
        '.gitignore',
        '.editorconfig',
        '.aria2/aria2.conf',

        '.thefuck/settings.py',
        '.thefuck/rules/**',

        '.config/ibus/rime/wubi_pinyin.schema.yaml',
        '.config/ibus/rime/pinyin_simp.schema.yaml',

        'wallpaper/sync.sh',
        'document/ref/get-php-en-ref.sh',
        'document/ref/get-php-zh-ref.sh',

        '.vimrc',
        '.config/nvim/init.vim',

        '.config/starship.toml',

        '.spacemacs',
    ]

    china_sync_paths = [
        '.npmrc',
        '.composer/config.json',
        '.pip/pip.conf',
    ]


config = Config()
user_home_dir_ = os.getenv('HOME')
if user_home_dir_ is None:
    raise Exception('$HOME not found')
user_home_dir = user_home_dir_
current_dir = os.path.dirname(os.path.realpath(__file__))


class Cli:
    class Color(Enum):
        INFO = '\033[34m'
        ERROR = '\033[31m'

    @staticmethod
    def print_color(line: str, color: Color):
        print(color.value + line + '\\e[0m')

    def print_info(self, line: str):
        self.print_color(line, Cli.Color.INFO)

    def print_error(self, line: str):
        self.print_color(line, Cli.Color.ERROR)

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
                    self.print_info(f'Install scripts to {path}')

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
            self.print_info(
                f'Install scripts to {fish_script_path}')

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
                    self.print_info(f'COPY: {filepath} => {target_path}')

    def update_to_home(self):
        self.copy_by_glob(os.path.join(current_dir, 'home'),
                          config.sync_paths, user_home_dir)
        if self.is_china:
            self.copy_by_glob(os.path.join(
                current_dir, 'home_china'), config.china_sync_paths, user_home_dir)
        self.install_myscripts()
        self.print_info('Update done')

    def fetch_from_home(self):
        self.copy_by_glob(user_home_dir, config.sync_paths,
                          os.path.join(current_dir, 'home'))
        if self.is_china:
            self.copy_by_glob(user_home_dir, config.china_sync_paths,
                              os.path.join(current_dir, 'home_china'))
        self.print_info('Push done')


if __name__ == '__main__':
    Cli()
