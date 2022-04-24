import os
from typing import List


class TextFs(object):
    def read(self, filepath: str):
        if not os.path.exists(filepath):
            return ''
        with open(filepath, 'r') as f:
            return f.read()

    def readLines(self, filepath: str):
        if not os.path.exists(filepath):
            return []
        with open(filepath, 'r') as f:
            return f.readlines()

    def write(self, filepath: str, content: str):
        with open(filepath, 'w') as f:
            f.write(content)

    def writeLines(self, filepath: str, content: List[str]):
        with open(filepath, 'w') as f:
            f.writelines(content)

textFs = TextFs()
