import argparse
from enum import Enum
import glob
import os
import shutil
from typing import List, Literal, Tuple

from core.io import textFs

from .initrc import Initrc
from .config import Config, ConfigPath
from .env import env

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
        self.args = self.parse_args()
        self.initrc = Initrc(self)
        self.subcommand: Literal['to-home', 'from-home'] = self.args.subcommand
        if self.subcommand == 'to-home':
            self.update_to_home()
        elif self.subcommand == 'from-home':
            self.fetch_from_home()

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser(
            prog='myconfig script', description="myconfig")
        parser.add_argument('--china',
                            type=bool,
                            default=False,
                            help='include china proxy configuration')
        subparsers = parser.add_subparsers(required=True, dest='subcommand')
        subparsers.add_parser('to-home')
        subparsers.add_parser('from-home')
        return parser.parse_args()

    @property
    def is_china(self) -> bool:
        return self.args.china == True

    def install_initrc(self):
        self.initrc.install()

        if self.is_china:
            # china proxy
            self.install_bash_script('00-env.sh', 'CHINA_PROXY=1')
            self.install_fish_script('00-env.fish', 'set -g CHINA_PROXY 1')

    def install_base_script(self, dir: str, filename: str, content: str):
        script_path = os.path.join(dir, filename)
        exists_content = textFs.read(script_path)
        if exists_content != content:
            textFs.write(script_path, content)
            self.output(f'{script_path} installed', 'info')

    def install_bash_script(self, filename: str, content: str):
        self.install_base_script(self.initrc.initrc_dir, filename, content)

    def install_fish_script(self, filename: str, content: str):
        self.install_base_script(os.path.expanduser(
            '~/.config/fish/conf.d/'), filename, content)

    def ignored(self, filepath: str):
        return any([(ignore in filepath) for ignore in self.config.ignores])

    def simplify_path(self, position: Position, path: str):
        """simplify path for print in output"""
        if position == 'user_home':
            return f'~{os.path.sep}{os.path.relpath(path, env.user_home)}'
        elif position == 'store' or position == 'store_china':
            return f'.{os.path.sep}{os.path.relpath(path, env.app_root)}'
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
        source_path: str,
        target_path: str,
    ):
        if os.path.isfile(source_path):
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            shutil.copyfile(source_path, target_path, follow_symlinks=True)
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
                self.print_copy_to(transfer, source_path, target_path)
                self.copy_to(source_path, target_path)
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
                        filepath,
                        target_filepath,
                    )
                    self.output(
                        f'    {rel_target_path} => *', 'info')

    def update_to_home(self):
        self.glob_copy_to(self.config.sync_paths, ('store', 'user_home'))
        if self.is_china:
            self.glob_copy_to(self.config.china_sync_paths,
                              ('store_china', 'user_home'))
        self.install_initrc()
        self.output('Done: to-home', 'info')

    def fetch_from_home(self):
        self.glob_copy_to(self.config.sync_paths, ('user_home', 'store'))
        if self.is_china:
            self.glob_copy_to(self.config.china_sync_paths,
                              ('user_home', 'store_china'))
        self.output('Done: from-home', 'info')
