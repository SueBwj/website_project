import json
import os

def load_json(file):
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(file, data):
    with open(file,'w',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False, indent=4)
