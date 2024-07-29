import argparse
import logging
import pathlib
import sys
import time

from app import demo, move_files, review, revert


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str, help="Command to execute")
    parser.add_argument("path", type=pathlib.Path, help="Path to directory")
    parser.add_argument("--producer", type=str, help="Producer to use: ollama/groq/openai", default="ollama")
    parser.add_argument("--preference", type=str, help="Preferences to how the new directory should be sorted", default=None)
    parser.add_argument("--ignore", type=str, help="Folders to ignore", default=None)
    parser.add_argument("--apikey", type=str, help="API key for Groq/Claude/OpenAI", default="") # API_KEY_HERE
    args = parser.parse_args()
    print(args.command, args.path)

    if args.command == "demo":
        treedict = demo(args.path, args.producer, args.preference, args.ignore, args.apikey)
    else:
        print("Unknown command")
    
    # time to adjust here, improve the below code for more user control 
    move_files(args.path, treedict)
    
    if input("would you like to revert it back? y/n: ") == 'y':
        revert(args.path, treedict)
    
if __name__ == "__main__":
    tic = time.perf_counter()
    main()
    print(f'time taken: {(time.perf_counter() - tic):.2f}')
