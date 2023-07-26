
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


class RESTapi:    
    @classmethod
    def INPUT_TYPES(cls):
        return {
                "required": {
                    # {"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}
                    "type": ("STRING", {"default": "GET"}),
                    "url": ("STRING", {"default": "http://127.0.0.1:8188/history"}),
                    "data": ("STRING", {"default": "{\"data\":10}"}),
                    "headers": ("STRING", {"default": ""}),
                }
            }
        
    RETURN_TYPES = ("STRING",)
    CATEGORY = "REST"
    FUNCTION = "execute"
    
    def execute(self, type, url, data, headers):
        import requests
        try:
            data = json.loads(data)
        except Exception as e:
            print(e)
            data = {}
        try:
            if type.lower()=='get' :
                response = requests.get(url, params=data)
            elif type.lower()=='post' :
                response = requests.post(url, data=data, headers=headers)
            elif type.lower()=='put' :
                response = requests.put(url, data=data, headers=headers)
            elif type.lower()=='delete' :
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError()
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print ("Http Error:",errh)
            return (str(errh),)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
            return (str(errc),)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
            return (str(errt),)
        except requests.exceptions.RequestException as err:
            print ("Something went wrong",err)
            return (str(err),)        
        except Exception as err:
            print ("Something went wrong",err)
            return (str(err),)
        if response.ok:
            return (response.text, )
        else:
            return (response.reason,)
    

# class RESTget:    
#     @classmethod
#     def INPUT_TYPES(cls):
#         return {
#                 "required": {
#                     # {"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}
#                     "url": ("STRING", {"default": "http://127.0.0.1:8188/history"}),
#                     "data": ("STRING", {"default": "{\"data\":10}"}),
#                 }
#             }
        
#     RETURN_TYPES = ("STRING",)
#     CATEGORY = "REST"
#     FUNCTION = "execute"
    
#     def execute(self,url,data):
#         import requests
#         try:
#             j = json.loads(data)
#         except Exception as e:
#             print(e)
#             j = {}
#         r = requests.get(url, params=j)
#         if r.ok:
#             return (r.text, )
#         else:
#             return (r.reason,)
        
# class RESTpost:    
#     @classmethod
#     def INPUT_TYPES(cls):
#         return {
#                 "required": {
#                     # {"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}
#                     "url": ("STRING", {"default": "http://127.0.0.1:8188/history"}),
#                     "data": ("STRING", {"default": "{\"data\":10}"}),
#                     "headers": ("STRING", {"default": ""}),
#                 }
#             }
        
#     RETURN_TYPES = ("STRING",)
#     CATEGORY = "REST"
#     FUNCTION = "execute"
    
#     def execute(url, data, headers):
#         try:
#             response = requests.post(url, data=data, headers=headers)
#             response.raise_for_status()
#         except requests.exceptions.HTTPError as errh:
#             print ("Http Error:",errh)
#             return (str(errh),)
#         except requests.exceptions.ConnectionError as errc:
#             print ("Error Connecting:",errc)
#             return (str(errc),)
#         except requests.exceptions.Timeout as errt:
#             print ("Timeout Error:",errt)
#             return (str(errt),)
#         except requests.exceptions.RequestException as err:
#             print ("Something went wrong",err)
#             return (str(err),)
#         return (response.json(),)
    
# class RESTput:    
#     @classmethod
#     def INPUT_TYPES(cls):
#         return {
#                 "required": {
#                     # {"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}
#                     "url": ("STRING", {"default": "http://127.0.0.1:8188/history"}),
#                     "data": ("STRING", {"default": "{\"data\":10}"}),
#                     "headers": ("STRING", {"default": ""}),
#                 }
#             }
        
#     RETURN_TYPES = ("STRING",)
#     CATEGORY = "REST"
#     FUNCTION = "execute"
    
#     def execute(url, data, headers):
#         try:
#             response = requests.put(url, data=data, headers=headers)
#             response.raise_for_status()
#         except requests.exceptions.HTTPError as errh:
#             print ("Http Error:",errh)
#             return (str(errh),)
#         except requests.exceptions.ConnectionError as errc:
#             print ("Error Connecting:",errc)
#             return (str(errc),)
#         except requests.exceptions.Timeout as errt:
#             print ("Timeout Error:",errt)
#             return (str(errt),)
#         except requests.exceptions.RequestException as err:
#             print ("Something went wrong",err)
#             return (str(err),)
#         return (response.json(),)



# A dictionary that contains all nodes you want to export with their names
NODE_CLASS_MAPPINGS = {
    "RESTapi": RESTapi,
}
