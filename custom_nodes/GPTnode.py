
# ComfyUI
# https://github.com/pythongosssss/ComfyUI-Custom-Scripts/tree/main
# put in ComfyUI\custom_nodes\

import os
import requests
import json
import folder_paths
#import openpyxl
from datetime import datetime

output_dir = os.path.abspath("output_folder")

PARAMS = {
    'url' : f"http://127.0.0.1:7860/run/textgen", #"127.0.0.1",  # define the server address here
    'max_new_tokens': 200,
    'temperature': 0.5,
    'top_p': 0.9,
    'typical_p': 1,
    'n': 1,
    'stop': None,
    'do_sample': True,
    'return_prompt': False,
    'return_metadata': False,
    'typical_p': 0.95,
    'repetition_penalty': 1.05,
    'encoder_repetition_penalty': 1.0,
    'top_k': 0,
    'min_length': 0,
    'no_repeat_ngram_size': 2,
    'num_beams': 1,
    'penalty_alpha': 0,
    'length_penalty': 1.0,
    'pad_token_id': None,
    'eos_token_id': None,
    'use_cache': True,
    'num_return_sequences': 1,
    'bad_words_ids': None,
    'seed': -1,
}

class GPTInput:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_text": ("STRING", {
                    "multiline": True,
                    "default": "Enter text here"
                })
            }
        }
        
    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"
    CATEGORY = "GPT"
    
    def execute(self, input_text):
        return ({"text": input_text},)

class GPTOutput:
    def __init__(self):
        self.output_dir = output_dir
        self.type = "output"
        self.text = ""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Output_Text": ("TEXT", {"input_format": {"text": "STRING"}}),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save_text"
    OUTPUT_NODE = True
    CATEGORY = "GPT"

    def save_text(self, Output_Text, filename_prefix="ComfyUI"):
        Output_Text = Output_Text.get("text")
        self.text = Output_Text

        full_output_folder = os.path.join(self.output_dir, "TextOutput")

        if os.path.commonpath((self.output_dir, os.path.abspath(full_output_folder))) != self.output_dir:
            print("Saving text outside the output folder is not allowed.")
            return {}

        try:
            counter = max([int(f[:-4].split('_')[-1]) for f in os.listdir(full_output_folder) if f.startswith(filename_prefix) and f.endswith('.txt')]) + 1
        except ValueError:
            counter = 1
        except FileNotFoundError:
            os.makedirs(full_output_folder, exist_ok=True)
            counter = 1

        file = f"{filename_prefix}_{counter:05}.txt"
        with open(os.path.join(full_output_folder, file), 'w', encoding='utf-8') as text_file:
            text_file.write(Output_Text)

        print("Text saved")

        return {"text": Output_Text}

class GPTGenerator:

    do_sample = True
    early_stopping = False
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("TEXT", {"input_format": {"text": "STRING"}}),
            },
            "optional": {
                "model_name": ("STRING", {"default": "Does not matter anyway"}),
                "max_new_tokens": ("INT", {"default": PARAMS['max_new_tokens']}),
                "temperature": ("FLOAT", {"default": PARAMS['temperature']}),
                "top_p": ("FLOAT", {"default": PARAMS['top_p']}),
                "typical_p": ("FLOAT", {"default": PARAMS['typical_p']}),
                "repetition_penalty": ("FLOAT", {"default": PARAMS['repetition_penalty']}),
                "encoder_repetition_penalty": ("FLOAT", {"default": PARAMS['encoder_repetition_penalty']}),
                "top_k": ("INT", {"default": PARAMS['top_k']}),
                "min_length": ("INT", {"default": PARAMS['min_length']}),
                "no_repeat_ngram_size": ("INT", {"default": PARAMS['no_repeat_ngram_size']}),
                "num_beams": ("INT", {"default": PARAMS['num_beams']}),
                "penalty_alpha": ("FLOAT", {"default": PARAMS['penalty_alpha']}),
                "length_penalty": ("FLOAT", {"default": PARAMS['length_penalty']}),
                "seed": ("INT", {"default": PARAMS['seed']})
            }
        }
        
    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_text"
    CATEGORY = "GPT"
    
    def generate_text(self,url, model_name, prompt, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed):
        self.sever = url
        self.model_name = model_name
        self.prompt = prompt.get("text", "")
        self.max_new_tokens = max_new_tokens
        self.do_sample = GPTGenerator.do_sample
        self.temperature = temperature
        self.top_p = top_p
        self.typical_p = typical_p
        self.repetition_penalty = repetition_penalty
        self.encoder_repetition_penalty = encoder_repetition_penalty
        self.top_k = top_k
        self.min_length = min_length
        self.no_repeat_ngram_size = no_repeat_ngram_size
        self.num_beams = num_beams
        self.penalty_alpha = penalty_alpha
        self.length_penalty = length_penalty
        self.early_stopping = GPTGenerator.early_stopping
        self.seed = seed
        
        # Make request to API to generate text
        # url = f"http://{server}:7860/run/textgen"
        headers = {"Content-Type": "application/json"}
        params = {
            'max_new_tokens': self.max_new_tokens,
            'do_sample': self.do_sample,
            'temperature': self.temperature,
            'top_p': self.top_p,
            'typical_p': self.typical_p,
            'repetition_penalty': self.repetition_penalty,
            'encoder_repetition_penalty': self.encoder_repetition_penalty,
            'top_k': self.top_k,
            'min_length': self.min_length,
            'no_repeat_ngram_size': self.no_repeat_ngram_size,
            'num_beams': self.num_beams,
            'penalty_alpha': self.penalty_alpha,
            'length_penalty': self.length_penalty,
            'early_stopping': self.early_stopping,
            'seed': self.seed,
        }
        payload = json.dumps([self.prompt, params])
        response = requests.post(url, headers=headers, json={
            "data": [
                payload
            ]
        }) 
        
        # Check for errors in API response
        if response.status_code != 200:
            self.generated_text = None
            print(f"Error generating text: {response.text}")
            return {}
        
        # Parse generated text from API response
        response_data = response.json()["data"]
        if len(response_data) < 1:
            self.generated_text = None
            print("Error generating text: Empty response from API")
            return {}
        generated_text = response_data[0]
        
        # Save generated text and return it
        self.generated_text = generated_text[len(self.prompt_text):len(generated_text)]
        return ({"text": self.generated_text},)


class OpenaiChatSingleMessage:    
    _INPUT_TYPES = {
                "required": {
                    # {"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}
                    "role": ("STRING", {"default": "system"}),
                    "content": ("STRING", {"default": "You are a helpful assistant."}),
                },
                "optional": {
                    #The name of the author of this message. name is required if role is function, and it should be the name of the function whose response is in the content. May contain a-z, A-Z, 0-9, and underscores, with a maximum length of 64 characters.
                    "name": ("STRING", {"default": None}),
                    "function_call": ("STRING", {"default": None}),
                }
            }
    @classmethod
    def INPUT_TYPES(cls):
        return OpenaiChatSingleMessage._INPUT_TYPES
        
    RETURN_TYPES = ("STRING",)
    CATEGORY = "GPT"
    FUNCTION = "execute"
    
    def execute(self,*args, **kwargs):
        return (str(kwargs), )
    

class OpenaiChatMergeMessage:    
    _INPUT_TYPES = {
                "required": {
                    "msg0": ("STRING", {"forceInput": True}),
                },
                "optional": {
                    "msg1": ("STRING", {"forceInput": True}),
                    "msg2": ("STRING", {"forceInput": True}),
                    "msg3": ("STRING", {"forceInput": True}),
                    "msg4": ("STRING", {"forceInput": True}),
                    "msg5": ("STRING", {"forceInput": True}),
                    "msg6": ("STRING", {"forceInput": True}),
                    "msg7": ("STRING", {"forceInput": True}),
                    "msg8": ("STRING", {"forceInput": True}),
                    "msg9": ("STRING", {"forceInput": True}),
                }
            }
    @classmethod
    def INPUT_TYPES(cls):
        return OpenaiChatMergeMessage._INPUT_TYPES
        
    RETURN_TYPES = ("STRING",)
    CATEGORY = "GPT"
    FUNCTION = "execute"
    
    def execute(self,*args, **kwargs):
        res = ''
        for i in range(10):
            if f'msg{i}' in kwargs.keys() and kwargs[f'msg{i}'] is not None:
                res += f'{kwargs[f"msg{i}"]}\n,\n'
        return (res, )


class OpenaiChatCompletion:    
    @classmethod
    def INPUT_TYPES(cls):
        import openai
        return {
                "required": {
                    # "prompt": ("TEXT", {"input_format": {"text": "STRING"}}),
                    "url": ("STRING", {"default": openai.api_base}),
                    "key": ("STRING", {"default": "xxxxxxxxxxxxxxx"}),
                    "model": ("STRING", {"default": "gpt-3.5-turbo"}),
                    "messages": ("STRING", {"forceInput": True}),
                },
                "optional": {
                    "name": ("STRING", {"default": "gpt"}),
                    # "function_call": ("STRING", {"default": "none"}),
                    # "functions": ("ARRAY", {"default": None}),
                    # "description": ("STRING", {"default": None}),
                    # "temperature": ("FLOAT", {"default": 1.0}),
                    # "top_p": ("FLOAT", {"default": 1.0}),
                    # "n": ("INT", {"default": 1}),
                    # "stream": ("BOOLEAN", {"default": False}),
                    # "stop": ("STRING_OR_ARRAY", {"default": None}),
                    # "max_tokens": ("INT", {"default": float('inf')}),
                    # "presence_penalty": ("FLOAT", {"default": 0.0}),
                    # "frequency_penalty": ("FLOAT", {"default": 0.0}),
                    # "logit_bias": ("MAP", {"default": None}),
                    # "user": ("STRING", {"default": "user"})
                }
            }

        
    RETURN_TYPES = ("STRING",)
    CATEGORY = "GPT"
    FUNCTION = "execute"

    def _filternull(self,d):
        return { k:v for k,v in d.items() if len(v)>0}
    
    def execute(self,url,key,model,messages=None,name="gpt"):
        import json,openai
        openai.api_key = key
        openai.api_base = url
        if messages is None:messages = []
        res = {
            'model':model,
            'messages':[self._filternull(json.loads(m.replace("'",'"'))) for m in messages.split('\n,\n') if len(m)>0]
        }
        response = openai.ChatCompletion.create(**res)
        return (str(response),)
    # FUNCTION = "generate_text"    
    # def generate_text(self,url, model_name, prompt, max_new_tokens, temperature, top_p, typical_p, repetition_penalty, encoder_repetition_penalty, top_k, min_length, no_repeat_ngram_size, num_beams, penalty_alpha, length_penalty, seed):
    #     self.sever = url
    #     self.model_name = model_name
    #     self.prompt = prompt.get("text", "")
    #     self.max_new_tokens = max_new_tokens
    #     self.do_sample = GPTGenerator.do_sample
    #     self.temperature = temperature
    #     self.top_p = top_p
    #     self.typical_p = typical_p
    #     self.repetition_penalty = repetition_penalty
    #     self.encoder_repetition_penalty = encoder_repetition_penalty
    #     self.top_k = top_k
    #     self.min_length = min_length
    #     self.no_repeat_ngram_size = no_repeat_ngram_size
    #     self.num_beams = num_beams
    #     self.penalty_alpha = penalty_alpha
    #     self.length_penalty = length_penalty
    #     self.early_stopping = GPTGenerator.early_stopping
    #     self.seed = seed
        
    #     # Make request to API to generate text
    #     # url = f"http://{server}:7860/run/textgen"
    #     headers = {"Content-Type": "application/json"}
    #     params = {
    #         'max_new_tokens': self.max_new_tokens,
    #         'do_sample': self.do_sample,
    #         'temperature': self.temperature,
    #         'top_p': self.top_p,
    #         'typical_p': self.typical_p,
    #         'repetition_penalty': self.repetition_penalty,
    #         'encoder_repetition_penalty': self.encoder_repetition_penalty,
    #         'top_k': self.top_k,
    #         'min_length': self.min_length,
    #         'no_repeat_ngram_size': self.no_repeat_ngram_size,
    #         'num_beams': self.num_beams,
    #         'penalty_alpha': self.penalty_alpha,
    #         'length_penalty': self.length_penalty,
    #         'early_stopping': self.early_stopping,
    #         'seed': self.seed,
    #     }
    #     payload = json.dumps([self.prompt, params])
    #     response = requests.post(url, headers=headers, json={
    #         "data": [
    #             payload
    #         ]
    #     }) 
        
    #     # Check for errors in API response
    #     if response.status_code != 200:
    #         self.generated_text = None
    #         print(f"Error generating text: {response.text}")
    #         return {}
        
    #     # Parse generated text from API response
    #     response_data = response.json()["data"]
    #     if len(response_data) < 1:
    #         self.generated_text = None
    #         print("Error generating text: Empty response from API")
    #         return {}
    #     generated_text = response_data[0]
        
    #     # Save generated text and return it
    #     self.generated_text = generated_text[len(self.prompt_text):len(generated_text)]
    #     return ({"text": self.generated_text},)


# A dictionary that contains all nodes you want to export with their names
NODE_CLASS_MAPPINGS = {
    "GPTInput": GPTInput,
    "GPTOutput": GPTOutput,
    "GPTGenerator": GPTGenerator,
    "OpenaiChatSingleMessage": OpenaiChatSingleMessage,
    "OpenaiChatCompletion": OpenaiChatCompletion,
    "OpenaiChatMergeMessage": OpenaiChatMergeMessage,
}
