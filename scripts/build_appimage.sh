#!/usr/bin/env bash
set -euo pipefail

echo "=== Generando AppImage ==="

if [[ "$(uname -s)" != "Linux" ]]; then
    echo "ERROR: Este script debe ejecutarse desde Linux."
    echo "No es compatible con MSYS2, Git Bash ni Windows."
    exit 1
fi

if [[ "$(uname -m)" != "x86_64" ]]; then
    echo "ERROR: Este script requiere Linux x86_64."
    exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR"

echo "Sistema: $(uname -s)"
echo "Arquitectura: $(uname -m)"

set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

APP="PatingBackupManager"
VERSION="1.0.0"
TOOLS="$ROOT/build/tools"
APPDIR="$ROOT/build/AppDir"

mkdir -p "$TOOLS" releases/appimage

echo "=== Generando AppImage ==="

# Compilar aplicación
bash scripts/build_linux.sh

# Descargar linuxdeploy
if [ ! -f "$TOOLS/linuxdeploy-x86_64.AppImage" ]; then
    wget -O "$TOOLS/linuxdeploy-x86_64.AppImage" \
      https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
fi

chmod +x "$TOOLS/linuxdeploy-x86_64.AppImage"

export APPIMAGE_EXTRACT_AND_RUN=1

# Preparar AppDir
rm -rf "$APPDIR"

mkdir -p "$APPDIR/usr/lib/$APP"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"

cp -a "dist/$APP/." "$APPDIR/usr/lib/$APP/"

# Iconos
cp assets/icon.png "$APPDIR/$APP.png"

cp assets/icon.png \
    "$APPDIR/usr/share/icons/hicolor/256x256/apps/$APP.png"

# Escritorio
cat > "$APPDIR/$APP.desktop" <<EOF
[Desktop Entry]
Name=Pating Backup Manager
Exec=$APP
Icon=$APP
Type=Application
Categories=Utility;System;
Terminal=false
EOF

cp "$APPDIR/$APP.desktop" \
    "$APPDIR/usr/share/applications/"

# Lanzador
cat > "$APPDIR/AppRun" <<EOF
#!/bin/sh
HERE="\$(dirname "\$(readlink -f "\$0")")"
exec "\$HERE/usr/lib/$APP/$APP" "\$@"
EOF

chmod +x "$APPDIR/AppRun"

# Generar AppImage
ARCH=x86_64 "$TOOLS/linuxdeploy-x86_64.AppImage" \
    --appdir "$APPDIR" \
    --executable "$APPDIR/usr/lib/$APP/$APP" \
    --desktop-file "$APPDIR/$APP.desktop" \
    --icon-file "$APPDIR/$APP.png" \
    --output appimage

# Mover resultado
find "$ROOT" -maxdepth 1 -name "*.AppImage" \
    -exec mv {} "$ROOT/releases/appimage/$APP-$VERSION-x86_64.AppImage" \;

echo "AppImage generado."