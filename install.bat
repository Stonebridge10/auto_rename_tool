@echo off
echo Installation des dépendances...
pip install -r requirements.txt

echo Création des dossiers nécessaires...
mkdir logs
mkdir backups

echo Installation terminée !
pause
