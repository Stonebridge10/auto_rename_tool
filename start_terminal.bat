@echo off
title AUTO RENAME TOOL - WINDOWS TERMINAL
color 0A

:menu
cls
echo ===================================
echo      AUTO RENAME TOOL - WINDOWS
echo ===================================
echo [1] Renommer des vidéos
echo [2] Renommer des scans
echo [3] Renommer des musiques
echo [4] Quitter
echo -----------------------------------
set /p choix=Votre choix (1-4) : 

if "%choix%"=="1" goto launch
if "%choix%"=="2" goto launch
if "%choix%"=="3" goto launch
if "%choix%"=="4" exit

echo Choix invalide.
pause
goto menu

:launch
echo Lancement de l'interface graphique...
python auto_rename.py
pause
goto menu
