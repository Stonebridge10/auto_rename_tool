import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json

from scans_renamer import rename_scans
from video_renamer import rename_videos
from music_renamer import rename_music

CONFIG_PATH = "config.json"

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

class RenameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Rename Tool")

        self.folder_path = tk.StringVar()
        self.file_type = tk.StringVar(value="scans")

        self.create_widgets()
        self.update_keywords_area()

    def create_widgets(self):
        tk.Label(self.root, text="📁 Dossier à traiter :").pack()
        tk.Entry(self.root, textvariable=self.folder_path, width=60).pack(padx=10, pady=5)
        tk.Button(self.root, text="Parcourir", command=self.browse_folder).pack()

        tk.Label(self.root, text="📂 Type de fichiers :").pack(pady=(10, 2))
        for t in [("Scans / Mangas", "scans"), ("Vidéos", "videos"), ("Musiques", "musics")]:
            tk.Radiobutton(self.root, text=t[0], variable=self.file_type, value=t[1], command=self.update_keywords_area).pack(anchor='w', padx=20)

        tk.Label(self.root, text="🔤 Mots-clés à détecter :").pack(pady=(10, 2))
        self.keywords_entry = tk.Entry(self.root, width=50)
        self.keywords_entry.pack(padx=10, pady=5)

        tk.Button(self.root, text="✅ Lancer le renommage", command=self.rename).pack(pady=10)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def update_keywords_area(self):
        config = load_config()
        key_list = config.get("keywords", {}).get(self.file_type.get(), [])
        self.keywords_entry.delete(0, tk.END)
        self.keywords_entry.insert(0, ", ".join(key_list))

    def rename(self):
        folder = self.folder_path.get().strip()
        if not os.path.isdir(folder):
            messagebox.showerror("Erreur", "Chemin de dossier invalide.")
            return

        keywords = self.keywords_entry.get().strip()
        if keywords:
            config = load_config()
            config["keywords"][self.file_type.get()] = [k.strip() for k in keywords.split(",")]
            save_config(config)

        try:
            if self.file_type.get() == "scans":
                rename_scans(folder)
            elif self.file_type.get() == "videos":
                rename_videos(folder)
            elif self.file_type.get() == "musics":
                rename_music(folder)
            messagebox.showinfo("Succès", "Renommage terminé avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue :\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RenameGUI(root)
    root.mainloop()
