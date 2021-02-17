import argparse
from enum import Enum
import glob
import os
from pathlib import PurePath
import shutil
import textwrap
from typing import List, Literal

from script.config import Config, ConfigPath
from script.core import env


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

    def ignored(self, filepath: str):
        return any([(ignore in filepath) for ignore in self.config.ignores])

    def copy_to(self, source: str, target: str):
        if os.path.isfile(source):
            os.makedirs(os.path.dirname(
                target), exist_ok=True)
            shutil.copyfile(source, target,
                            follow_symlinks=True)
            self.output(
                f'COPY: {source} => {target}', 'info')
        else:
            self.output(f'{source} not found', 'error')

    def glob_copy_to(self, paths: List[ConfigPath], target: Literal['user', 'local'], is_china: bool = False):
        for path in paths:
            if not path.matched_platform():
                continue
            local_path = path.local_path_china if is_china else path.local_path
            source_path = path.user_path if target == 'local' else local_path
            target_path = local_path if target == 'local' else path.user_path

            if path.glob_path is None:
                if self.ignored(source_path):
                    continue
                self.copy_to(source_path, target_path)
            else:
                for filepath in glob.glob(os.path.join(
                        source_path, path.glob_path),
                        recursive=True):
                    if self.ignored(filepath):
                        continue
                    relative_path = os.path.relpath(filepath, source_path)
                    target_filepath = os.path.join(target_path, relative_path)
                    self.copy_to(filepath, target_filepath)

    def update_to_home(self):
        self.glob_copy_to(self.config.sync_paths, target='user')
        if self.is_china:
            self.glob_copy_to(self.config.china_sync_paths,
                              target='user', is_china=True)
        self.install_myscripts()
        self.output('Update done', 'info')

    def fetch_from_home(self):
        self.glob_copy_to(self.config.sync_paths, target='local')
        if self.is_china:
            self.glob_copy_to(self.config.china_sync_paths,
                              target='local', is_china=True)
        self.output('Push done', 'info')
