import os
import textwrap
from typing import TYPE_CHECKING, List

from core.io import textFs

if TYPE_CHECKING:
    from .cli import Cli

class InitrcLines(object):
    lines: List[str]

    def __init__(self, lines: List[str]):
        self.lines = lines
        self.stripped = [line.strip() for line in lines]

    def append(self, content: str):
        # remove trailing empty lines
        while self.lines and not self.lines[-1].strip():
            self.lines.pop()
        self.lines.append(content)

class Initrc(object):
    def __init__(self, cli: 'Cli') -> None:
        self.cli = cli
        self.start_marker = '# __WR_INITRC_START__'
        self.end_marker = '# __WR_INITRC_END__'
        self.initrc_dir = os.path.expanduser('~/.wr-initrc')

    def has_initrc_script(self, path: str, lines: InitrcLines) -> bool:
        start_count = lines.stripped.count(self.start_marker)
        end_count = lines.stripped.count(self.end_marker)
        if start_count > 1:
            raise Exception(f'Multiple start markers in {path}')
        if end_count > 1:
            raise Exception(f'Multiple end markers in {path}')
        if start_count != end_count:
            raise Exception(f'Missing start/end markers in {path}')
        return start_count == 1

    def remove_initrc_script(self, lines: InitrcLines):
        start_index = lines.stripped.index(self.start_marker)
        end_index = lines.stripped.index(self.end_marker)
        lines.lines = lines.lines[:start_index] + lines.lines[end_index + 1:]
        return lines

    def try_append_script(self, path: str):
        lines = InitrcLines(textFs.readLines(path))
        if self.has_initrc_script(path, lines):
            # already has initrc script
            lines = self.remove_initrc_script(lines)

        init_script = textwrap.dedent(f"""
        {self.start_marker}
        for file in {self.initrc_dir}/*; do
            [[ -f "$file" ]] && . "$file"
        done
        {self.end_marker}
        """)
        lines.append(init_script)
        textFs.writeLines(path, lines.lines)
        self.cli.output(f'Updated scripts to {path}', 'info')

    def install(self):
        if not os.path.exists(self.initrc_dir):
            os.makedirs(self.initrc_dir)
        for path in ['~/.bashrc', '~/.zshrc']:
            path = os.path.normpath(path)
            self.try_append_script(os.path.expanduser(path))
