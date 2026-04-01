import os


class TextFs:
    def read(self, filepath: str):
        if not os.path.exists(filepath):
            return ''
        with open(filepath) as f:
            return f.read()

    def readLines(self, filepath: str):
        if not os.path.exists(filepath):
            return []
        with open(filepath) as f:
            return f.readlines()

    def write(self, filepath: str, content: str):
        with open(filepath, 'w') as f:
            f.write(content)

    def writeLines(self, filepath: str, content: list[str]):
        with open(filepath, 'w') as f:
            f.writelines(content)

textFs = TextFs()
