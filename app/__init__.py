import pathlib
import shutil
import os

from not_llama_fs.producers.groq_producer import GroqProducer
from not_llama_fs.producers.ollama_producer import OllamaProducer
from not_llama_fs.producers.openai_producer import OpenAIProducer

def demo(
        path: pathlib.Path,
        producer_name: str = "ollama",
        preference: str = "",
        ignore: str = "",
        apikey: str = None
):
    if not path.exists():
        raise ValueError(f"Path {path} does not exist")

    # Get prompts
    with open("file_process_prompt.txt", "r") as f:
        prompt = f.read()

    with open("tree_generation_prompt.txt", "r") as f:
        final_prompt = f.read()
        if ignore != "":
            final_prompt += f"\nIgnore and do not change {ignore} or its contents"
        if preference != "":
            final_prompt += f"\nUser Preference: {preference}"

    # Select producer to be used
    print(f"Using producer {producer_name}")
    options = {}
    produce_options = {}
    if producer_name == "ollama":
        model = "llama3"
        producer = OllamaProducer(host="localhost")
        options = {"num_predict": 128}
        produce_options = {"num_predict": -1}
    elif producer_name == "groq":
        model = "llama3-70b-8192"
        producer = GroqProducer(api_key=apikey)
    elif producer_name == 'openai':
        model = "gpt-4o"
        producer = OpenAIProducer(api_key=apikey)
    else:
        raise ValueError(f"Unknown producer {producer_name}")

    producer.load_directory(path)
    
    # Process files
    producer.setup(prompt, model=model, options=options)
    producer.prepare_files(path, ignore)

<<<<<<< HEAD
    producer.setup(prompt, model=model, options=options)
    producer.prepare_files_llamaindex(path, ignore)
    producer.setup(final_prompt, model=model, options=produce_options)
    treedict, tree = producer.produce() # issue here with how the model is producing , dictionaries for metadata is not consistent at all
    
    print(tree) # Show the ascii art for the new directory
    return treedict, producer
=======
    # Generate tree
    producer.setup(final_prompt, model=model, options=produce_options)
    treedict, tree = producer.produce() # issue here with how the model is producing , dictionaries for metadata is not consistent at all
   
    # Print the ASCII represented by the stage 
    print(tree) 
    return treedict
>>>>>>> 5f6b36be9eb49f139c17c0408c5b8a431d3218ce

def move_file(src, file):
    dst_path = os.path.dirname(file["dst_path"])
    dst_path = os.path.join(src, dst_path)
    os.makedirs(dst_path, exist_ok=True)

    # Move the file from the original directory to the new directory
    try:
        dst_path = os.path.join(dst_path, os.path.basename(file['dst_path']))
        shutil.move(file['src_path'], dst_path)
        print(f'Moved {file["src_path"]} to {dst_path}')

    except Exception as e:
        raise e

def review(
        treedict, 
        producer,
        producer_name: str = "ollama", # this and apikey will be added once it works, add the producer option like in the other thing.
        ignore: str = "",
        apikey: str = None
        ):
    old_treedict = treedict
    preference = input('Please review the changes. If you are satisfied, please enter "yes", and if not, please tell me whatever you want to change: ')

    with open('tree_generation_prompt.txt', 'r') as f:
        final_prompt = f.read()

    while preference != "yes":
#         producer = OllamaProducer(host="localhost")
#        producer.setup(prompt=final_prompt, model='llama3', options={'num_predict':-1})
        treedict, tree = producer.produce()

        print(tree) 
        preference = input("is this good?: ")

    return treedict

