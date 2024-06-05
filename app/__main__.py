import argparse
import logging
import pathlib
import sys
import time

from app import demo, IMAGE_SUPPORT_PRODUCERS, move_file, review


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str, help="Command to execute")
    parser.add_argument("path", type=pathlib.Path, help="Path to directory")
    parser.add_argument("--producer", type=str, help="Producer to use: ollama/groq/claude/openai", default="ollama")
    parser.add_argument("--apikey", type=str, help="API key for Groq", default=None)
    parser.add_argument("--preference", type=str, help="Preferences to how the new directory should be sorted", default="")
    parser.add_argument("--ignore", type=str, help="Folders to ignore", default="") 

    args = parser.parse_args()
#     print(args.command, args.path)

    if args.command == "demo":
        treedict, producer = demo(args.path, args.producer, args.preference, args.ignore, args.apikey)
    else:
        print("Unknown command")

    # time to adjust here, improve the below code for more user control
    review(treedict, producer, args.producer, args.ignore, args.apikey)

    for file in treedict['files']:
        move_file(args.path, file)
    
if __name__ == "__main__":
    tic = time.perf_counter()
    main()
    print(f'time taken: {(time.perf_counter() - tic):.2f}')
