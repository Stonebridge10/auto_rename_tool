
#!/bin/bash

echo ""
echo "[*] Mise à jour de pip et installation des dépendances..."
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt

echo ""
echo "[*] Création des dossiers nécessaires..."
mkdir -p logs
mkdir -p backups

echo ""
echo "[✓] Installation terminée avec succès."