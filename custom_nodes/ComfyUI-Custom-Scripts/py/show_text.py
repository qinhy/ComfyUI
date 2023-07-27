class ShowText:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "text": ("STRING", {"forceInput": True}),
        }}

    INPUT_IS_LIST = True
    RETURN_TYPES = ("STRING",)
    FUNCTION = "notify"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True,)

    CATEGORY = "utils"

    def notify(self, text):
        import json
        try:
            res = json.loads(text[0])
            text = json.dumps(res, ensure_ascii=False, indent=2)
            text = (text,)
        except Exception as e :
            print(e)
        return {"ui": {"text": text}, "result": (text,)}


NODE_CLASS_MAPPINGS = {
    "ShowText|pysssss": ShowText,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShowText|pysssss": "Show Text 🐍",
}
