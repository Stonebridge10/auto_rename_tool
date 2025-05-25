#!/bin/bash

echo "==============================="
echo " AUTO RENAME TOOL - TERMINAL "
echo "==============================="
echo "1. Renommer des vidéos"
echo "2. Renommer des scans"
echo "3. Renommer des musiques"
echo "4. Quitter"
echo "-------------------------------"

read -p "Votre choix (1-4) : " choix

case $choix in
  1)
    echo "Lancement du renommage vidéo..."
    python3 auto_rename.py
    ;;
  2)
    echo "Lancement du renommage de scans..."
    python3 auto_rename.py
    ;;
  3)
    echo "Lancement du renommage musical..."
    python3 auto_rename.py
    ;;
  4)
    echo "À bientôt !"
    exit 0
    ;;
  *)
    echo "Choix invalide."
    ;;
esac
