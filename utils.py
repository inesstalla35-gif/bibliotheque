import json   # Module pour lire/écrire des fichiers JSON
import os     # Module pour interagir avec le système de fichiers
from typing import Any  # Pour indiquer qu'une fonction accepte n'importe quel type


def ensure_data_dir(path: str):
    """
    Crée le dossier parent si celui-ci n'existe pas.
    
    Exemple :
        Si path = "data/livres.json"
        → Cette fonction créera le dossier "data/" s'il n'existe pas
    
    Args:
        path (str): Chemin complet du fichier (ex: "data/livres.json")
    """
    d = os.path.dirname(path)
    
    # AMÉLIORATION : Retirer le print() pour éviter d'encombrer la console
    # print(d)  # ← À supprimer en production
    
    if d and not os.path.exists(d):
        os.makedirs(d, exist_ok=True)


def save_json(path: str, data: Any):
    """
    Sauvegarde des données Python dans un fichier JSON.
    
    Args:
        path (str): Chemin du fichier JSON
        data (Any): Données à sauvegarder (dict, list, etc.)
    """
    ensure_data_dir(path)
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data, 
            f, 
            indent=2,
            ensure_ascii=False
        )


def load_json(path: str):
    """
    Charge des données depuis un fichier JSON.
    
    Args:
        path (str): Chemin du fichier JSON à charger
    
    Returns:
        Les données chargées (dict, list, etc.) ou None si le fichier n'existe pas
    """
    if not os.path.exists(path):
        return None
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)