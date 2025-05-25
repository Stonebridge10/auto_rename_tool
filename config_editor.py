# config_editor.py

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import shutil
from datetime import datetime

CONFIG_PATH = "config.json"
BACKUP_DIR = "backups"

class ConfigEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Éditeur de Configuration - Auto Rename Tool")
        self.geometry("600x400")
        self.resizable(False, False)

        self.file_type_var = tk.StringVar(value="scans")
        self.config_data = {}
        self.ignore_listbox = None
        self.ignore_entry = None

        self.load_config()
        self.create_widgets()

    def load_config(self):
        if not os.path.exists(CONFIG_PATH):
            messagebox.showerror("Erreur", f"Fichier {CONFIG_PATH} introuvable.")
            self.destroy()
        else:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                self.config_data = json.load(f)

    def save_config(self):
        # Backup avant modification
        os.makedirs(BACKUP_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        shutil.copy(CONFIG_PATH, f"{BACKUP_DIR}/config_backup_{timestamp}.json")

        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.config_data, f, indent=4, ensure_ascii=False)

        messagebox.showinfo("Sauvegardé", "Configuration enregistrée avec succès.")

    def create_widgets(self):
        title = tk.Label(self, text="Éditeur de Configuration", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        frame = tk.Frame(self)
        frame.pack(pady=5)

        tk.Label(frame, text="Type de fichiers à configurer :").pack(side=tk.LEFT, padx=5)

        file_type_menu = ttk.Combobox(frame, textvariable=self.file_type_var, values=["scans", "videos"], state="readonly", width=15)
        file_type_menu.pack(side=tk.LEFT)

        tk.Button(self, text="Configurer", command=self.open_config_section, bg="#4CAF50", fg="white").pack(pady=10)

    def open_config_section(self):
        for widget in self.winfo_children()[3:]:
            widget.destroy()

        config_frame = tk.Frame(self)
        config_frame.pack(fill="both", expand=True, pady=10)

        tk.Label(config_frame, text="Mots-clés ignorés :", font=("Arial", 12, "bold")).pack(pady=5)

        self.ignore_listbox = tk.Listbox(config_frame, width=50, height=8)
        self.ignore_listbox.pack()

        ignore_keywords = self.config_data[self.file_type_var.get()].get("keywords_ignore", [])
        for kw in ignore_keywords:
            self.ignore_listbox.insert(tk.END, kw)

        entry_frame = tk.Frame(config_frame)
        entry_frame.pack(pady=5)

        self.ignore_entry = tk.Entry(entry_frame, width=30)
        self.ignore_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(entry_frame, text="Ajouter", command=self.add_keyword).pack(side=tk.LEFT)
        tk.Button(entry_frame, text="Supprimer", command=self.remove_keyword).pack(side=tk.LEFT, padx=5)

        tk.Button(self, text="💾 Sauvegarder les modifications", command=self.save_and_reload, bg="#2196F3", fg="white").pack(pady=10)

    def add_keyword(self):
        new_kw = self.ignore_entry.get().strip()
        if new_kw:
            self.ignore_listbox.insert(tk.END, new_kw)
            self.ignore_entry.delete(0, tk.END)

    def remove_keyword(self):
        selected = self.ignore_listbox.curselection()
        if selected:
            self.ignore_listbox.delete(selected[0])

    def save_and_reload(self):
        new_keywords = list(self.ignore_listbox.get(0, tk.END))
        self.config_data[self.file_type_var.get()]["keywords_ignore"] = new_keywords
        self.save_config()
        self.load_config()


if __name__ == "__main__":
    app = ConfigEditorApp()
    app.mainloop()

