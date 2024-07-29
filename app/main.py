import argparse
import logging
import pathlib
import sys
import time
from flask import Flask, request, jsonify

from .functions import demo, move_files, review, revert


app = Flask(__name__)

@app.route('/process_file', methods=['POST'])
def process_file():
    data = request.json
    file_path = data.get('file_path')
    producer = data.get('producer', 'ollama')
    preference = data.get('preference', None)
    ignore = data.get('ignore', None)
    apikey = data.get('apikey', '') # API KEY HERE

    if not file_path:
        return jsonify({"status": "error", "message": "No file path provided"}), 400
    
    file_path = pathlib.Path(file_path)

    if not file_path.exists():
        return jsonify({"status": "error", "message": "File path does not exist"}), 400

    try:
        treedict = demo(file_path, producer, preference, ignore, apikey)
        return jsonify({"status": "success", "message": f"Processed file: {file_path}", "treedict": treedict}), 200

    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/revert', methods=['POST'])
def revert_endpoint():
    data = request.json
    file_path = data.get('file_path')
    treedict = data.get('treedict')

    if not file_path or not treedict:
        return jsonify({"status": "error", "message": "File path or treedict missing"}), 400

    try: 
        revert(file_path, treedict)
        return jsonify({"status": "success", "message": f"Moved files for: {file_path}"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/move_files', methods=['POST'])
def move_files_endpoint(): 
    data = request.json
    file_path = data.get('file_path')
    treedict = data.get('treedict')

    if not file_path or not treedict:
        return jsonify({"status": "error", "message": "File path or treedict missing"}), 400

    try: 
        move_files(file_path, treedict)
        return jsonify({"status": "success", "message": f"Moved files for: {file_path}"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str, help="Command to execute")
    parser.add_argument("path", type=pathlib.Path, help="Path to directory")
    parser.add_argument("--producer", type=str, help="Producer to use: ollama/groq/openai", default="ollama")
    parser.add_argument("--preference", type=str, help="Preferences to how the new directory should be sorted", default=None)
    parser.add_argument("--ignore", type=str, help="Folders to ignore", default=None)
    parser.add_argument("--apikey", type=str, help="API key for Groq/Claude/OpenAI", default="") # API KEY HERE
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
    if len(sys.argv) > 1:
        tic = time.perf_counter()
        cli()
        print(f'time taken: {(time.perf_counter() - tic):.2f}')
    else:
        app.run(port=5000)
