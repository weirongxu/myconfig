import os
import platform
import pprint
import subprocess
from typing import Literal, Optional, TypeVar

T = TypeVar("T")


def unwrap(v: Optional[T], desc: Optional[str] = None) -> T:
    if v is None:
        raise ValueError(f"Unexpected None {desc}")
    return v


Platform = Literal['win', 'unix']


class Env():
    isWin: bool = platform.system() == 'Windows'
    isUnix = not isWin
    platform: Platform = 'win' if isWin else 'unix'

    def __init__(self) -> None:
        _user_home = os.getenv('HOME')
        if not _user_home and Env.isWin:
            _user_home = self.get_power_shell_var("HOME")
        self.user_home = unwrap(_user_home, "$HOME")

        self.cwd = os.getcwd()

    def get_power_shell_var(self, varname: str):
        completed = subprocess.run([
            'powershell',
            '-Command',
            f'echo ${varname}',
        ], capture_output=True)
        return completed.stdout.decode().strip()

    @property
    def store_home(self) -> str:
        return os.path.normpath(os.path.join(self.cwd, 'dotfiles/home'))

    @property
    def store_home_china(self) -> str:
        return os.path.normpath(os.path.join(self.cwd, 'dotfiles/home_china'))


env = Env()


pp = pprint.PrettyPrinter(indent=2)
