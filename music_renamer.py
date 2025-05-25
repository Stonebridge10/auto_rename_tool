import os
import re
import json
import shutil
from datetime import datetime

CONFIG_PATH = "config.json"
BACKUP_PATH = "backups/music_renames.json"
LOG_PATH = "logs/music_log.txt"

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

def clean_title(text):
    # Supprime les underscores, tirets inutiles, etc.
    return re.sub(r"[_\-]+", " ", text).strip().title()

def rename_music(directory):
    config = load_config()
    extensions = config["file_types"]["musics"]
    separator = config.get("music_separator", "-")

    for filename in os.listdir(directory):
        base, ext = os.path.splitext(filename)
        if ext.lower() not in extensions:
            continue

        # Essaye de séparer le nom en Artiste - Titre
        match = re.split(r"[-–—]+", base, maxsplit=1)
        if len(match) < 2:
            print(f"[!] Format inconnu : {filename}")
            continue

        artist = clean_title(match[0])
        title = clean_title(match[1])

        new_name = f"{artist} {separator} {title}{ext}"
        src = os.path.join(directory, filename)
        dst = os.path.join(directory, new_name)

        if os.path.exists(dst):
            print(f"[!] Fichier déjà existant : {new_name}")
            continue

        os.rename(src, dst)
        log_action(filename, new_name)
        backup_original(filename, new_name)
        print(f"[✓] {filename} → {new_name}")
