# Not Not LLama FS
> didn't accept my PR so i made my own repo

An extension of [Not Llama FS](https://github.com/drforse/not-llama-fs), which in turn is an extension of [Llama FS](https://github.com/iyaja/llama-fs).
* Llama FS didn't work on anybody's computer, so Not Llama FS was made to prove the concept, but it only proposes a hypothetical new directory structure
* Not^2 Llama FS actually reorganizes it for you. I'm working on making the directory structure better, and for users to specify how they want to organize it
* I also include an electron-app GUI that you can use to sort your folders. Drag a folder in and press the button, your folder is sorted. 

The usage is basically identical to Not Llama FS, but with a few more parameters. I'll work on the documentation later. I also need to update some things (including updating to llama 3.1)

![](src/demo.mov)

(the rest of the docs here is from not llama fs)

### Prerequisites

Before installing, ensure you have the following requirements:  
- Python 3.10 or higher  
- pip (Python package installer)  

If you want to use NotLlamaFS with local llama models, you need to install [Ollama](https://ollama.com/) and pull the llama3 and llava models like that:  
```bash
ollama pull llama3 
ollama pull llava
```

If you want to use Groq, ChatGPT or Claude, you will need to get the API keys.  

## Usage

To see the demo of the resulting file structure, run the command:

For local llama3+llava (requires their installation! check [prerequisites section](#prerequisites) for more details)    
   ```bash
   python -m app demo "path/to/directory/with/files/to/organize" --producer ollama 
   ```

For groq  
```bash
python -m app demo "path/to/directory/with/files/to/organize" --producer groq --apikey "your-groq-api-key" 
```  

For OpenAI (ChatGPT)  
```bash 
python -m app demo "path/to/directory/with/files/to/organize" --producer openai --apikey "your-openai-api-key"
```  

For Claude
```bash
python -m app demo "path/to/directory/with/files/to/organize" --producer claude --apikey "your-claude-api-key" 
```  

More settings for your run:  
`--text-model`: model for text files    
Defaults are:  
- llama3 for local ollama models  
- llama3-70b-8192 for groq  
- gpt-4o for openai  
- claude-3-haiku-20240307 for claude  

`--image-model`: model for image files  
Defaults are:  
- llava for local ollama models  
- claude-3-haiku-20240307 for claude  
- text model is used for groq (setting ignored, code here is not completely alright)  
- text model is used for openai (setting ignored, code here is not completely alright)  

## Credits
This was the original credits:
> https://github.com/iyaja/llama-fs - for the idea, inspiration and making me angry (for nothing working!) enough to write this.

https://github.com/drforse/not-llama-fs - for the sorting implementation, and not accepting my PR.
