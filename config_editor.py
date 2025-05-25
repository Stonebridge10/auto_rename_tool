# config_editor.py

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

CONFIG_PATH = "config.json"

class ConfigEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Éditeur de Configuration - Auto Rename Tool")
        self.geometry("500x300")
        self.resizable(False, False)

        # Choix du type de fichier
        self.file_type_var = tk.StringVar(value="scans")

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="Éditeur de Configuration", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Choix du type de fichier
        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="Type de fichiers à configurer :").pack(side=tk.LEFT, padx=5)

        file_type_menu = ttk.Combobox(frame, textvariable=self.file_type_var, values=["scans", "videos"], state="readonly", width=15)
        file_type_menu.pack(side=tk.LEFT)

        # Bouton Continuer
        tk.Button(self, text="Configurer", command=self.open_config_section, bg="#4CAF50", fg="white").pack(pady=20)

    def open_config_section(self):
        choice = self.file_type_var.get()
        messagebox.showinfo("Sélection", f"Tu as choisi : {choice}. (Les options s'afficheront à la prochaine étape.)")

if __name__ == "__main__":
    app = ConfigEditorApp()
    app.mainloop()
