import os
import json
import logging
import pathlib

import magic
import ollama
from llama_index.core import SimpleDirectoryReader

from .interface import ABCProducer, clean_filename
from ..fs.tree import TreeObject


class OllamaProducer(ABCProducer):
    def __init__(self, host: str = "localhost",):
        super().__init__()
        self.host = host
        self.prompt = None
        self.model = None
        self.options = {}
        self._client = None

    def setup(
            self,
            prompt: str,
            model: str = "llama3",
            options: dict | None = None,
    ):
        self.prompt = prompt
        self.model = model
        if options is not None:
            self.options = options
        if self.options is None:
            self.options = {}

    @property
    def client(self) -> ollama.Client:
        if self._client is None:
            self._client = ollama.Client(
                host=self.host
            )
        return self._client
    
    def prepare_files(self, path, ignore):
        if self.model is None:
            raise ValueError("Model is not set")
        if self.prompt is None:
            raise ValueError("Prompt is not set")
        if self.options is None:
            raise ValueError("Options are not set")
       
        # Split ignore to take a single string as input
        if ignore is not None:
            ignore = ignore.split(',')
            for i in range(len(ignore)):
                ignore[i] = os.path.join(path, ignore[i].strip())
            print(f"Ignoring files/folder: {ignore}")
        else:
            ignore = []
            print("Not ignoring any files")

        reader = SimpleDirectoryReader(path, filename_as_id=True, recursive=True, exclude=["/Users/rtty/downloads/bigtest/goodclass-ai-tools-updated/", "/Users/rtty/downloads/bigtest/copy-gdrive-folder", "/Users/rtty/downloads/bigtest/librarian/"]) 
        # reader = SimpleDirectoryReader(path, filename_as_id=True, recursive=True, exclude=ignore) 
            
        for file in reader.iter_data():
            result = self.client.generate(
                    model = self.model,
                    system = self.prompt,
                    prompt = str(file),
                    options = self.options,
                    format = "json"
            )

            filepath = clean_filename(file[0].doc_id)

            print(f"Prepared {filepath}")
            self.prepared_files.append((filepath, result["response"]))        
    def produce(self) -> TreeObject:
        if self.model is None:
            raise ValueError("Model is not set")
        if self.prompt is None:
            raise ValueError("Prompt is not set")
        if self.options is None:
            raise ValueError("Options are not set")

        llama_response = self.client.generate(
            system=self.prompt,
            prompt=json.dumps(self.prepared_files),
            model=self.model,
            options=self.options,
            format="json"
        )["response"]

        try:
            llama_response_json = json.loads(llama_response)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON response: {e}")
            logging.error(f"Response: {llama_response}")
            raise e

        for n, file in enumerate(llama_response_json["files"]):
            src_path = pathlib.Path(file["src_path"])
            dst_path = pathlib.Path(file["dst_path"])
            if src_path.suffix != dst_path.suffix:
                dst_path = dst_path.with_suffix(src_path.suffix)
                llama_response_json["files"][n]["dst_path"] = dst_path.as_posix()

        return llama_response_json, TreeObject.from_json(llama_response_json)

