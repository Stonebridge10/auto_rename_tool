@echo off
echo.
echo [*] Installation des dépendances Python...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [*] Création des dossiers nécessaires...
if not exist logs mkdir logs
if not exist backups mkdir backups

echo.
echo [✓] Installation terminée.
pause