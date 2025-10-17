#
import json   
import os #système fichier
from typing import Any#tout type

def ensure_data_dir(path: str):
    d = os.path.dirname(path) #pour extraire la partie dossier du chemin. d represente le chemin per exemple home/user si path vaut home/user/data.json
    print(d)
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)


def save_json(path: str, data: Any):
    ensure_data_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(path: str):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
