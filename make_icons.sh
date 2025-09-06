#!/bin/bash

# Nom du fichier source
SRC="icon.png"

# Vérification
if [ ! -f "$SRC" ]; then
  echo "❌ $SRC introuvable"
  exit 1
fi

# --- Windows (.ico) ---
convert "$SRC" -define icon:auto-resize=256,128,64,48,32,16 icon.ico
echo "✔ icon.ico généré (Windows)"

# --- macOS (.icns) ---
mkdir -p MyIcon.iconset
sips -z 16 16   "$SRC" --out MyIcon.iconset/icon_16x16.png
sips -z 32 32   "$SRC" --out MyIcon.iconset/icon_32x32.png
sips -z 64 64   "$SRC" --out MyIcon.iconset/icon_64x64.png
sips -z 128 128 "$SRC" --out MyIcon.iconset/icon_128x128.png
sips -z 256 256 "$SRC" --out MyIcon.iconset/icon_256x256.png
sips -z 512 512 "$SRC" --out MyIcon.iconset/icon_512x512.png
sips -z 1024 1024 "$SRC" --out MyIcon.iconset/icon_1024x1024.png
iconutil -c icns MyIcon.iconset
rm -rf MyIcon.iconset
echo "✔ MyIcon.icns généré (macOS)"

# --- Linux (PNG multi-tailles) ---
mkdir -p linux_icons
for size in 16 32 48 64 128 256; do
  convert "$SRC" -resize ${size}x${size} linux_icons/icon_${size}x${size}.png
done
echo "✔ Icônes PNG générées dans ./linux_icons (Linux)"
