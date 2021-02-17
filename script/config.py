from __future__ import annotations
from argparse import ArgumentTypeError
from glob import glob
import os
import copy
import shutil
import subprocess
from dataclasses import dataclass
from types import LambdaType
from typing import Any, Callable, List, Literal, Optional, Union, overload

from script.core import Platform, env, unwrap


class ConfigPath():
    """
    @example
    ```
    ConfigPath('path/glob').glob('/**/*')
    # ~/path/glob/**/* <-> ./home/path/glob/**/*

    ConfigPath('path/glob').glob('/**/*').local('path/glob2')
    # ~/path/glob/**/* <-> ./home/path/glob2/**/*

    ConfigPath.path('path/to/filename.conf')
    # ~/path/to/filename.conf <-> ./home/path/to/filename.conf

    ConfigPath.path('path/to/filename.config').local('path2/to/filename.config')
    # ~/path/to/filename.conf <-> ./home/path2/to/filename.conf
    ```
    """

    path: str
    _local_path: Optional[str] = None
    _user_path: Optional[str] = None
    platform: Optional[Platform] = None
    glob_path: Optional[str] = None

    def __init__(self, path: str) -> None:
        self.path = os.path.normpath(path)

    def clone(self) -> ConfigPath:
        return copy.copy(self)

    def glob(self, glob_path: str):
        c = self.clone()
        c.glob_path = os.path.normpath(glob_path)
        return c

    def local(self, local_path: str):
        c = self.clone()
        c._local_path = os.path.normpath(local_path)
        return c

    @property
    def local_path(self):
        return os.path.join(env.local_home, self._local_path if self._local_path else self.path)

    @property
    def local_path_china(self):
        return os.path.join(env.local_home_china, self._local_path if self._local_path else self.path)

    def user(self, user_path: str):
        c = self.clone()
        c._user_path = os.path.normpath(user_path)
        return c

    @property
    def user_path(self):
        return os.path.join(env.user_home, self._user_path if self._user_path else self.path)

    def only(self, platform: Platform):
        c = self.clone()
        c.platform = platform
        return c

    def matched_platform(self):
        if self.platform is None:
            return True
        else:
            return self.platform == env.platform


OriginConfigPath = Union[str, ConfigPath]


class Config():
    def __init__(
        self,
        ignores: List[str],
        sync_paths: List[OriginConfigPath],
        china_sync_paths: List[OriginConfigPath],
    ) -> None:
        _user_home_dir = os.getenv('HOME')
        if not _user_home_dir and env.isWin:
            _user_home_dir = env.get_power_shell_var("HOME")
        self.user_home_dir = unwrap(_user_home_dir, "$HOME")

        if env.isWin:
            profile_path = unwrap(
                env.get_power_shell_var("PROFILE"), '$PROFILE')
            profile_rel_path = os.path.relpath(
                profile_path, self.user_home_dir)
            sync_paths.append(profile_rel_path)

        self.ignores = ignores
        self.sync_paths = list(map(self.to_config_path, sync_paths))
        self.china_sync_paths = list(
            map(self.to_config_path, china_sync_paths))

    def to_config_path(self, p: OriginConfigPath) -> ConfigPath:
        if isinstance(p, str):
            return ConfigPath(p)
        else:
            return p

    ignores: List[str]

    sync_paths: List[ConfigPath]

    china_sync_paths: List[ConfigPath]
