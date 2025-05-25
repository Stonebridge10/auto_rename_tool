import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re
import json
import shutil
from datetime import datetime

CONFIG_FILE = "config.json"
BACKUP_FOLDER = "backups"
LOG_FOLDER = "logs"

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def log_action(content):
    os.makedirs(LOG_FOLDER, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d")
    with open(f"{LOG_FOLDER}/renaming_log_{now}.txt", "a", encoding="utf-8") as f:
        f.write(content + "\n")

def backup_file(file_path):
    os.makedirs(BACKUP_FOLDER, exist_ok=True)
    shutil.copy(file_path, os.path.join(BACKUP_FOLDER, os.path.basename(file_path)))

def rename_files(folder, config):
    renamed = 0
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if not os.path.isfile(file_path):
            continue

        for mode in config["modes"]:
            if file.lower().endswith(tuple(mode["extensions"])):
                new_name = apply_rename_logic(file, mode["patterns"], mode["output_format"], config["common_keywords"])
                if new_name and new_name != file:
                    backup_file(file_path)
                    os.rename(file_path, os.path.join(folder, new_name))
                    log_action(f"{file} → {new_name}")
                    renamed += 1
                break
    return renamed

def apply_rename_logic(filename, patterns, output_format, keywords):
    name = filename
    for kw in keywords:
        name = name.replace(kw, "").strip()

    for pattern in patterns:
        match = re.search(pattern["regex"], name, re.IGNORECASE)
        if match:
            try:
                return pattern["output"].format(*match.groups()) + os.path.splitext(filename)[-1]
            except IndexError:
                continue
    return None

def choose_folder_and_rename():
    folder = filedialog.askdirectory(title="Choisissez le dossier à renommer")
    if not folder:
        return
    config = load_config()
    count = rename_files(folder, config)
    messagebox.showinfo("Terminé", f"{count} fichier(s) renommé(s).")

def main():
    root = tk.Tk()
    root.title("Auto Rename Tool")
    root.geometry("400x200")

    label = tk.Label(root, text="Renommage Automatique de Fichiers", font=("Arial", 14))
    label.pack(pady=20)

    btn = tk.Button(root, text="Sélectionner un dossier", command=choose_folder_and_rename)
    btn.pack(pady=10)

    quit_btn = tk.Button(root, text="Quitter", command=root.quit)
    quit_btn.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
