#!/bin/bash

echo "Installation des dépendances..."
pip install -r requirements.txt

echo "Création des dossiers nécessaires..."
mkdir -p logs
mkdir -p backups

echo "Installation terminée !"
