import os
import re
import json
import shutil
from datetime import datetime

CONFIG_PATH = "config.json"
BACKUP_PATH = "backups/original_names.json"
LOG_PATH = "logs/rename_log.txt"

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def log_action(old_name, new_name):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} : {old_name} → {new_name}\n")

def backup_original(old_name, new_name):
    os.makedirs("backups", exist_ok=True)
    data = {}
    if os.path.exists(BACKUP_PATH):
        with open(BACKUP_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    data[old_name] = new_name
    with open(BACKUP_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def rename_scans(directory):
    config = load_config()
    keywords = config["keywords"]
    aliases = config["aliases"]
    extensions = config["file_types"]["scans"]

    for filename in os.listdir(directory):
        base, ext = os.path.splitext(filename)
        if ext.lower() not in extensions:
            continue

        lowered = base.lower()
        original = filename

        # Détection du nom de l’œuvre via alias
        title_found = None
        for alias, official in aliases.items():
            if alias in lowered:
                title_found = official
                break

        if not title_found:
            print(f"[!] Nom d'œuvre non reconnu dans : {filename}")
            continue

        # Détection du chapitre ou tome
        chapter_number = None
        tome_number = None

        # Chercher tous les mots-clés pour chapitre et tome
        for ch_kw in keywords["chapter"]:
            match = re.search(rf"{ch_kw}[- ]?(\d+)", lowered)
            if match:
                chapter_number = match.group(1)
                break

        for t_kw in keywords["tome"]:
            match = re.search(rf"{t_kw}[- ]?(\d+)", lowered)
            if match:
                tome_number = match.group(1)
                break

        if not chapter_number and not tome_number:
            print(f"[!] Aucun numéro détecté dans : {filename}")
            continue

        # Construire le nouveau nom
        new_name_parts = [title_found]
        if tome_number:
            new_name_parts.append(f"Tome {tome_number}")
        if chapter_number:
            new_name_parts.append(f"Chapitre {chapter_number}")

        new_name = " - ".join(new_name_parts) + ext
        src = os.path.join(directory, filename)
        dst = os.path.join(directory, new_name)

        if os.path.exists(dst):
            print(f"[!] Le fichier existe déjà : {new_name}")
            continue

        os.rename(src, dst)
        log_action(filename, new_name)
        backup_original(filename, new_name)
        print(f"[✓] {filename} → {new_name}")
