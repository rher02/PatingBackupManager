#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

APP="PatingBackupManager"
MAIN="src/backup_manager/main.py"

echo "=== Compilando Backup Manager para Linux ==="

# Comprobar GTK4
python3 -c "
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
"

# Entorno virtual
if [ ! -d .venv-build ]; then
    python3 -m venv --system-site-packages .venv-build
fi

source .venv-build/bin/activate

python -m pip install --upgrade pip pyinstaller

# Limpiar
rm -rf build dist

# Compilar
pyinstaller \
    --noconfirm \
    --clean \
    --onedir \
    --name "$APP" \
    --paths src \
    --collect-all gi \
    --collect-all cairo \
    --hidden-import=gi.repository.Gtk \
    --hidden-import=gi.repository.Gio \
    --hidden-import=gi.repository.GLib \
    --add-data "assets:assets" \
    "$MAIN"

echo "=== Linux compilado ==="