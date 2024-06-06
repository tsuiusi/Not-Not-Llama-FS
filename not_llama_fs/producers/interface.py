import abc
import logging
import pathlib
import time
import os

from not_llama_fs.fs.tree import TreeObject


class ABCProducer(abc.ABC):
    def __init__(self):
        self.files: list[pathlib.Path] = []
        self.prepared_files: list[tuple[str, str]] = []

    @abc.abstractmethod
    def produce(self) -> TreeObject:
        pass

    @abc.abstractmethod
    def setup(self, prompt: str, model: str, options: dict | None = None):
        pass

    def load_file(self, path: pathlib.Path):
        self.files.append(path)

    def load_directory(self, path: pathlib.Path):
        dirs = [path]
        while dirs:
            for directory in dirs:
                for file in directory.iterdir():
                    print(file)
                    if file.is_file():
                        self.load_file(file)
                    elif file.is_dir():
                        dirs.append(file)
                    else:
                        logging.warning(f"Skipping {file} as it is not a file nor a directory")
                dirs.pop(0)

def clean_filename(filename):
    extension = os.path.dirname(filename)
    base_name = os.path.basename(filename)
    if base_name.endswith('_part_0'):
        base_name = base_name[:-7]
    return os.path.join(extension, base_name) 

