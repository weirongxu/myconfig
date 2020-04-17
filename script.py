#!/usr/bin/env python3
from cleo import Application, Command
from pathlib import PurePath
import textwrap
import shutil
import glob
import os

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
    '.atom/.apmrc',
    '.composer/config.json',
    '.pip/pip.conf',
]

user_home_dir = os.getenv('HOME')
current_dir = os.path.dirname(os.path.realpath(__file__))

def copy_by_glob(self, source_home, paths, target_home):
    for path in paths:
        for filepath in glob.glob(os.path.join(source_home, path), recursive=True):
            if any([(ignore in filepath) for ignore in ignores]):
                continue
            relative_path = PurePath(filepath).relative_to(source_home)
            target_path = os.path.join(target_home, str(relative_path))
            if os.path.isfile(filepath):
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                shutil.copyfile(filepath, target_path, follow_symlinks=True)
                self.line('<info>copy {0} => {1}</info>'.format(filepath, target_path))

def install_myscripts(self):
    myscripts_path = os.path.join(current_dir, 'myscripts')

    shell_script = textwrap.dedent("""
    export MYSCRIPTS_HOME="{0}"
    [[ -s "$MYSCRIPTS_HOME/myshrc" ]] && . "$MYSCRIPTS_HOME/myshrc"
    """).format(myscripts_path)

    if self.option('china'):
        shell_script = "\nCHINA_PROXY=1\n" + shell_script

    for path in ['~/.bashrc', '~/.zshrc']:
        with open(os.path.expanduser(path), 'a+') as f:
            f.seek(0)
            if shell_script not in f.read():
                f.write(shell_script)
                self.line('<info>install scripts to {0}</info>'.format(path))

    fish_script = textwrap.dedent("""
    if status is-interactive
      set -g MYSCRIPTS_HOME "{0}"
      if test -s "$MYSCRIPTS_HOME/myshrc.fish"
        . "$MYSCRIPTS_HOME/myshrc.fish"
      end
    end
    """).format(myscripts_path)

    if self.option('china'):
        shell_script = "\nset -g CHINA_PROXY 1\n" + fish_script

    fish_script_path = os.path.expanduser('~/.config/fish/conf.d/myscripts.fish')
    with open(fish_script_path, 'w') as f:
        f.write(fish_script)
        self.line('<info>install scripts to {0}</info>'.format(fish_script_path))



class UpdateToHomeCommand(Command):
    """
    UpdateToHome Config

    update-to-home
    {--c|china : include china proxy configuration}
    """

    def handle(self):
        copy_by_glob(self, os.path.join(current_dir, 'home'), sync_paths, user_home_dir)
        if self.option('china'):
            copy_by_glob(self, os.path.join(current_dir, 'home_china'), china_sync_paths, user_home_dir)
        install_myscripts(self)
        self.line('<info>update done</info>')

class FetchFromHomeCommand(Command):
    """
    FetchFromHome Config

    fetch-from-home
    {--c|china : include china proxy configuration}
    """

    def handle(self):
        copy_by_glob(self, user_home_dir, sync_paths, os.path.join(current_dir, 'home'))
        if self.option('china'):
            copy_by_glob(self, user_home_dir, china_sync_paths, os.path.join(current_dir, 'home_china'))
        self.line('<info>push done</info>')

application = Application()
application.add(FetchFromHomeCommand())
application.add(UpdateToHomeCommand())

if __name__ == '__main__':
    application.run()
