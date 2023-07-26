
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


class RESTget:    
    @classmethod
    def INPUT_TYPES(cls):
        return {
                "required": {
                    # {"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}
                    "url": ("STRING", {"default": "http://127.0.0.1:8188/history"}),
                    "content": ("STRING", {"default": "{\"data\":10}"}),
                }
            }
        
    RETURN_TYPES = ("STRING",)
    CATEGORY = "REST"
    FUNCTION = "execute"
    
    def execute(self,url,content):
        import requests
        try:
            j = json.loads(content)
        except Exception as e:
            print(e)
            j = {}
        r = requests.get(url, params=j)
        if r.ok:
            return (r.text, )
        else:
            return (r.reason,)

# A dictionary that contains all nodes you want to export with their names
NODE_CLASS_MAPPINGS = {
    "RESTget": RESTget,
}
