import argparse
import logging
import pathlib
import sys

from app import demo, move_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str, help="Command to execute")
    parser.add_argument("path", type=pathlib.Path, help="Path to directory")
    parser.add_argument("--producer", type=str, help="Producer to use: ollama/groq/claude/openai", default="ollama")
    parser.add_argument("--apikey", type=str, help="API key for Groq/Claude/OpenAI", default="sk-proj-dpKFPzwwKO2c8HkTOQABT3BlbkFJB4h5AjAMqAvY9cfmVwYx")
    parser.add_argument("--text-model", type=str, help="Text model to use", default=None)
    parser.add_argument("--image-model", type=str, help="Image model to use", default=None)
    parser.add_argument("--preference", type=str, help="Preferences to how the new directory should be sorted", default="")
    parser.add_argument("--ignore", type=str, help="Folders to ignore", default="") # A hard coded implementation of this would probably be better than LLM solution
    args = parser.parse_args()
    print(args.command, args.path)

    if args.text_model is None:
        if args.producer == "ollama":
            args.text_model = "llama3"
        elif args.producer == "groq":
            args.text_model = "llama3-70b-8192"
        elif args.producer == "openai":
            args.text_model = "gpt-4o"
    if args.image_model is None:
        if args.producer == "ollama":
            args.image_model = "llava"

    if args.command == "demo":
        treedict = demo(args.path, args.producer, args.preference, args.ignore, args.text_model, args.image_model, args.apikey)
    else:
        print("Unknown command")
    
    # time to adjust here, improve the below code for more user control 
    for file in treedict['files']:
        move_file(args.path, file)
    
if __name__ == "__main__":
    main()
