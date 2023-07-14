from __future__ import annotations
import copy
import os
from os import path
from typing import List, Optional, Union

from .env import Platform, env


class ConfigPath():
    """
    @example
    ```
    ConfigPath('path/glob').glob('**/*')
    # ~/path/glob/**/* <-> ./home/path/glob/**/*

    ConfigPath('path/glob').glob('**/*').store('path/glob2')
    # ~/path/glob/**/* <-> ./home/path/glob2/**/*

    ConfigPath.path('path/to/filename.conf')
    # ~/path/to/filename.conf <-> ./home/path/to/filename.conf

    ConfigPath.path('path/to/filename.config').store('path2/to/filename.config')
    # ~/path/to/filename.conf <-> ./home/path2/to/filename.conf
    ```
    """

    _store_path: str
    _user_home_path: str
    _platform: Optional[Platform] = None
    glob_path: Optional[str] = None

    def __init__(self, path: str) -> None:
        # get relative path
        relpath = os.path.normpath(path)
        if relpath.startswith(env.user_home):
            relpath = os.path.relpath(relpath, env.user_home)

        self._user_home_path = relpath
        self._store_path = relpath

    def clone(self) -> ConfigPath:
        return copy.copy(self)

    def glob(self, glob_path: str):
        c = self.clone()
        c.glob_path = path.normpath(glob_path)
        return c

    def store(self, store_path: str):
        """force to set the store path"""
        c = self.clone()
        c._store_path = path.normpath(store_path)
        return c

    @property
    def store_path(self):
        """get path store in this repo"""
        return path.join(env.store_home, self._store_path)

    @property
    def store_china_path(self):
        """get path store in this repo in china environment"""
        return path.join(env.store_home_china, self._store_path)

    def user_home(self, user_home_path: str):
        """force to set the user home path"""
        c = self.clone()
        c._user_home_path = path.normpath(user_home_path)
        return c

    @property
    def user_home_path(self):
        """get user home path"""
        return path.join(env.user_home, self._user_home_path)

    def only_platform(self, platform: Platform):
        """only for platform"""
        c = self.clone()
        c._platform = platform
        return c

    def matched_platform(self):
        if self._platform is None:
            return True
        else:
            return self._platform == env.platform


OriginConfigPath = Union[str, ConfigPath]


class Config():
    def __init__(
        self,
        ignores: List[str],
        sync_paths: List[OriginConfigPath],
        china_sync_paths: List[OriginConfigPath],
    ) -> None:
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
