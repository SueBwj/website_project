import json

def load_json(file):
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f) 