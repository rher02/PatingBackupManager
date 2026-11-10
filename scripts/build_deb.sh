#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

APP="pating-backup-manager"
VERSION="1.0.0"
PKG="$ROOT/build/deb/$APP"

echo "=== Generando paquete DEB ==="

rm -rf "$PKG"

mkdir -p "$PKG/DEBIAN"
mkdir -p "$PKG/opt/$APP/src"
mkdir -p "$PKG/opt/$APP/assets"
mkdir -p "$PKG/usr/bin"
mkdir -p "$PKG/usr/share/applications"
mkdir -p "$PKG/usr/share/icons/hicolor/256x256/apps"

# Copiar código
cp -a src/backup_manager "$PKG/opt/$APP/src/"
cp -a assets/. "$PKG/opt/$APP/assets/"

# Lanzador
cat > "$PKG/usr/bin/$APP" <<'EOF'
#!/bin/sh
cd /opt/backup-manager
export PYTHONPATH="/opt/backup-manager/src${PYTHONPATH:+:$PYTHONPATH}"
exec /usr/bin/python3 -m backup_manager.main "$@"
EOF

chmod 755 "$PKG/usr/bin/$APP"

# Icono
install -m 644 assets/icon.png \
    "$PKG/usr/share/icons/hicolor/256x256/apps/$APP.png"

# Escritorio
cat > "$PKG/usr/share/applications/$APP.desktop" <<EOF
[Desktop Entry]
Name=Backup Manager
Exec=$APP
Icon=$APP
Type=Application
Terminal=false
Categories=Utility;System;
EOF

# Dependencias
cat > "$PKG/DEBIAN/control" <<EOF
Package: $APP
Version: $VERSION
Section: utils
Priority: optional
Architecture: all
Maintainer: Backup Manager
Depends: python3, python3-gi, python3-cairo, gir1.2-gtk-4.0
Description: Backup Manager GTK4
 Aplicacion grafica para gestionar copias de seguridad.
EOF

mkdir -p releases/deb

dpkg-deb --root-owner-group --build \
    "$PKG" \
    "releases/deb/${APP}_${VERSION}_all.deb"

echo "DEB generado correctamente."