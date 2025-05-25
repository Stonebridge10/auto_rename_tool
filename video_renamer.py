import os
import re
import json
import shutil
from datetime import datetime

CONFIG_PATH = "config.json"
BACKUP_PATH = "backups/video_renames.json"
LOG_PATH = "logs/video_log.txt"

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

def rename_videos(directory):
    config = load_config()
    keywords = config["keywords"]
    aliases = config["aliases"]
    extensions = config["file_types"]["videos"]

    for filename in os.listdir(directory):
        base, ext = os.path.splitext(filename)
        if ext.lower() not in extensions:
            continue

        lowered = base.lower()
        title_found = None

        for alias, official in aliases.items():
            if alias in lowered:
                title_found = official
                break

        if not title_found:
            print(f"[!] Nom de série non reconnu : {filename}")
            continue

        season = None
        episode = None

        for s_kw in keywords["season"]:
            match = re.search(rf"{s_kw}[- ]?(\d+)", lowered)
            if match:
                season = match.group(1).zfill(2)
                break

        for e_kw in keywords["episode"]:
            match = re.search(rf"{e_kw}[- ]?(\d+)", lowered)
            if match:
                episode = match.group(1).zfill(2)
                break

        if not season and not episode:
            # Peut être un film
            new_name = f"{title_found} - Film{ext}"
        else:
            s = season if season else "01"
            e = episode if episode else "01"
            new_name = f"{title_found} - S{s}E{e}{ext}"

        src = os.path.join(directory, filename)
        dst = os.path.join(directory, new_name)

        if os.path.exists(dst):
            print(f"[!] Fichier déjà existant : {new_name}")
            continue

        os.rename(src, dst)
        log_action(filename, new_name)
        backup_original(filename, new_name)
        print(f"[✓] {filename} → {new_name}")
