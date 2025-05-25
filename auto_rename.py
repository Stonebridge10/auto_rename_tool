import os
import sys

from scans_renamer import rename_scans
from video_renamer import rename_videos
from music_renamer import rename_music

def print_menu():
    print("\n===== Auto Rename Tool =====")
    print("1. Renommer des scans / mangas")
    print("2. Renommer des vidéos (animes, films, séries)")
    print("3. Renommer des musiques")
    print("4. Quitter")

def get_directory():
    folder = input("\nEntrez le chemin du dossier à traiter : ").strip()
    if not os.path.isdir(folder):
        print("[!] Dossier invalide. Réessayez.")
        return get_directory()
    return folder

def main():
    while True:
        print_menu()
        choice = input("\nSélectionnez une option (1-4) : ").strip()

        if choice == "1":
            folder = get_directory()
            rename_scans(folder)

        elif choice == "2":
            folder = get_directory()
            rename_videos(folder)

        elif choice == "3":
            folder = get_directory()
            rename_music(folder)

        elif choice == "4":
            print("Au revoir !")
            sys.exit()

        else:
            print("[!] Choix invalide.")

if __name__ == "__main__":
    main()
