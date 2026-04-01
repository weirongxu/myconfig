import os
import platform
import pprint
import subprocess
from os import path
from typing import Literal


def unwrap[T](v: T | None, desc: str | None = None) -> T:
    if v is None:
        raise ValueError(f"Unexpected None {desc}")
    return v


Platform = Literal['win', 'unix']


class Env:
    isWin: bool = platform.system() == 'Windows'
    isLinux: bool = platform.system() == 'Linux'
    isUnix = not isWin
    platform: Platform = 'win' if isWin else 'unix'

    def __init__(self) -> None:
        _user_home = os.getenv('HOME')
        if not _user_home and Env.isWin:
            _user_home = self.get_power_shell_var("HOME")
        self.user_home = unwrap(_user_home, "$HOME")

        self.app_root = path.normpath(path.join(path.dirname(__file__), '../'))

    def get_power_shell_var(self, varname: str):
        completed = subprocess.run([
            'powershell',
            '-Command',
            f'echo ${varname}',
        ], capture_output=True)
        return completed.stdout.decode().strip()

    @property
    def store_home(self) -> str:
        return path.normpath(path.join(self.app_root, 'dotfiles/home'))



env = Env()


pp = pprint.PrettyPrinter(indent=2)
