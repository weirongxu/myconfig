import argparse
from enum import Enum
import glob
import os
from pathlib import PurePath
from pprint import pp
import shutil
import textwrap
from typing import Dict, List, Literal, Optional, Tuple, TypedDict, Union

from script.config import Config, ConfigPath
from script.core import env

Position = Literal['user_home', 'store', 'store_china']
Transfer = Tuple[Position, Position]


class Cli:
    class Color(Enum):
        info = '\033[34m'
        error = '\033[31m'

    @staticmethod
    def output(line: str, type: Literal['info', 'error'] = 'info'):
        print(getattr(Cli.Color, type).value + line + '\033[0m')

    def __init__(self, config: Config) -> None:
        self.config = config
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
        myscripts_path = os.path.join(env.cwd, 'myscripts')

        shell_script = textwrap.dedent(f"""
        export MYSCRIPTS_HOME="{myscripts_path}"
        [[ -s "$MYSCRIPTS_HOME/myshrc" ]] && . "$MYSCRIPTS_HOME/myshrc"
        """)

        if self.is_china:
            shell_script = "\nCHINA_PROXY=1\n" + shell_script

        for path in ['~/.bashrc', '~/.zshrc']:
            path = os.path.normpath(path)
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

        fish_script_path = os.path.normpath(os.path.expanduser(
            '~/.config/fish/conf.d/myscripts.fish'))
        with open(fish_script_path, 'w') as f:
            f.write(fish_script)
            self.output(
                f'Install scripts to {fish_script_path}', 'info')

    def ignored(self, filepath: str):
        return any([(ignore in filepath) for ignore in self.config.ignores])

    def simplify_path(self, position: Position, path: str):
        if position == 'user_home':
            return f'~{os.path.sep}{os.path.relpath(path, env.user_home)}'
        elif position == 'store' or position == 'store_china':
            return f'.{os.path.sep}{os.path.relpath(path, env.cwd)}'
        else:
            raise TypeError(f"{position} not support")

    def path_by_position(self, position: Position, path: ConfigPath):
        if position == 'user_home':
            return path.user_home_path
        elif position == 'store':
            return path.store_path
        elif position == 'store_china':
            return path.store_china_path
        else:
            raise TypeError(f"{position} not support")

    def copy_to(
        self,
        transfer: Transfer,
        source_path: str,
        target_path: str,
    ):
        if os.path.isfile(source_path):
            os.makedirs(os.path.dirname(
                target_path), exist_ok=True)
            shutil.copyfile(source_path, target_path,
                            follow_symlinks=True)
        else:
            self.output(f'{source_path} not found', 'error')

    def print_copy_to(self, transfer: Transfer, source_path: str, target_path: str):
        self.output(
            f'''  {
                self.simplify_path(transfer[0], source_path)
            } => {
                self.simplify_path(transfer[1], target_path)
            }''', 'info')

    def glob_copy_to(self, paths: List[ConfigPath], transfer: Transfer):
        self.output(f'Copy: ({transfer[0]} -> {transfer[1]}):', 'info')
        for path in paths:
            if not path.matched_platform():
                continue
            source_pos = transfer[0]
            target_pos = transfer[1]
            source_path = self.path_by_position(source_pos, path)
            target_path = self.path_by_position(target_pos, path)

            if path.glob_path is None:
                if self.ignored(source_path):
                    continue
                self.copy_to(transfer, source_path, target_path)
                self.print_copy_to(transfer, source_path, target_path)
            else:
                self.print_copy_to(transfer, source_path, target_path)
                for filepath in glob.glob(os.path.join(
                        source_path, path.glob_path),
                        recursive=True):
                    if self.ignored(filepath):
                        continue
                    rel_target_path = os.path.relpath(filepath, source_path)
                    target_filepath = os.path.join(
                        target_path, rel_target_path)
                    self.copy_to(
                        transfer,
                        filepath,
                        target_filepath,
                    )
                    self.output(
                        f'    {rel_target_path} => ...', 'info')

    def update_to_home(self):
        self.glob_copy_to(self.config.sync_paths, ('store', 'user_home'))
        if self.is_china:
            self.glob_copy_to(self.config.china_sync_paths,
                              ('store_china', 'user_home'))
        self.install_myscripts()
        self.output('Done: update-to-home', 'info')

    def fetch_from_home(self):
        self.glob_copy_to(self.config.sync_paths, ('user_home', 'store'))
        if self.is_china:
            self.glob_copy_to(self.config.china_sync_paths,
                              ('user_home', 'store_china'))
        self.output('Done: fetch-from-home', 'info')
