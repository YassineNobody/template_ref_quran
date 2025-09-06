#!/bin/bash
set -e

APP_NAME="QuranReference"
ENTRYPOINT="ui/ui.py"

# Détecter l'OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*|MINGW*|MSYS*) machine=Windows;;
    *)          machine="UNKNOWN:${OS}"
esac

echo "➡️  Build pour ${machine}"

# Nettoyer anciens builds
rm -rf build dist

# Commande PyInstaller selon OS
if [ "$machine" = "Windows" ]; then
    pyinstaller --onefile --windowed --name "$APP_NAME" --icon=icon.ico "$ENTRYPOINT"
elif [ "$machine" = "Mac" ]; then
    pyinstaller --onefile --windowed --name "$APP_NAME" --icon=MyIcon.icns "$ENTRYPOINT"
elif [ "$machine" = "Linux" ]; then
    pyinstaller --onefile --windowed --name "$APP_NAME" --icon=linux_icons/icon_256x256.png "$ENTRYPOINT"
else
    echo "❌ OS non supporté : $OS"
    exit 1
fi

echo "✔ Build terminé. Binaire disponible dans dist/"
