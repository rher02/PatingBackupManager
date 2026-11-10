#!/usr/bin/env bash
set -Eeuo pipefail

# =====================================================
# CONFIGURACIÓN
# =====================================================

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
cd "$ROOT"

APP="PatingBackupManager"

# Detectar Python del entorno virtual
if [[ -f "$ROOT/.venv/bin/python.exe" ]]; then
    PYTHON="$ROOT/.venv/bin/python.exe"
elif [[ -f "$ROOT/.venv/Scripts/python.exe" ]]; then
    PYTHON="$ROOT/.venv/Scripts/python.exe"
else
    echo "ERROR: No se encuentra Python en .venv."
    exit 1
fi

GTK_ROOT="/ucrt64"
GTK_BIN="$GTK_ROOT/bin"
GTK_LIB="$GTK_ROOT/lib"
GTK_TYPELIBS="$GTK_LIB/girepository-1.0"

DIST="$ROOT/dist"
BUILD="$ROOT/build"
RELEASE="$ROOT/releases/windows/$APP"

MAIN="$ROOT/src/backup_manager/__main__.py"

# =====================================================
# FUNCIONES
# =====================================================

error() {
    echo ""
    echo "ERROR: $1"
    exit 1
}

# =====================================================
# INICIO
# =====================================================

echo "=========================================="
echo " COMPILACIÓN WINDOWS GTK4"
echo "=========================================="

echo "Proyecto: $ROOT"
echo "Python: $PYTHON"

# =====================================================
# COMPROBACIONES
# =====================================================

[[ "${MSYSTEM:-}" == "UCRT64" ]] ||
    error "Ejecuta desde MSYS2 UCRT64."

[[ -f "$PYTHON" ]] ||
    error "No existe Python: $PYTHON"

[[ -f "$MAIN" ]] ||
    error "No existe $MAIN"

[[ -d "$ROOT/assets" ]] ||
    error "No existe assets/"

[[ -d "$GTK_BIN" ]] ||
    error "No existe $GTK_BIN"

[[ -d "$GTK_TYPELIBS" ]] ||
    error "No existe $GTK_TYPELIBS"

command -v cygpath >/dev/null ||
    error "No se encuentra cygpath."

# =====================================================
# VARIABLES GTK
# =====================================================

export PATH="$GTK_BIN:$PATH"
export GI_TYPELIB_PATH="$GTK_TYPELIBS"
export GTK_DATA_PREFIX="$GTK_ROOT"
export GTK_EXE_PREFIX="$GTK_ROOT"

# =====================================================
# COMPROBAR PYTHON
# =====================================================

echo ""
echo "Comprobando Python..."

"$PYTHON" -c "
import sys
print('Versión:', sys.version)
print('Ejecutable:', sys.executable)
"

# =====================================================
# CONVERTIR RUTAS WINDOWS
# =====================================================

ROOT_WIN="$(cygpath -aw "$ROOT")"
MAIN_WIN="$(cygpath -aw "$MAIN")"
ASSETS_WIN="$(cygpath -aw "$ROOT/assets")"
TYPELIBS_WIN="$(cygpath -aw "$GTK_TYPELIBS")"

# =====================================================
# COMPROBAR GTK4
# =====================================================

echo ""
echo "Comprobando GTK4..."

"$PYTHON" -c "
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Gdk', '4.0')

from gi.repository import Gtk, Gdk, Gio, GLib

print('GTK4:', Gtk.get_major_version())
print('GTK4 importado correctamente')
" || error "No se puede importar GTK4."

# =====================================================
# COMPROBAR PYINSTALLER
# =====================================================

echo ""
echo "Comprobando PyInstaller..."

"$PYTHON" -m pip show pyinstaller >/dev/null 2>&1 ||
    error "PyInstaller no está instalado."

"$PYTHON" -m PyInstaller --version

# =====================================================
# CREAR RUNTIME HOOK
# =====================================================

echo ""
echo "Preparando runtime hook..."

HOOK_DIR="$BUILD/hooks"
mkdir -p "$HOOK_DIR"

HOOK="$HOOK_DIR/rthook_gtk.py"

cat > "$HOOK" <<'PYTHON'
import os
import sys

# Directorio de ejecución de PyInstaller
base = getattr(
    sys,
    "_MEIPASS",
    os.path.dirname(sys.executable)
)

# DLL empaquetadas
os.environ["PATH"] = (
    base + os.pathsep + os.environ.get("PATH", "")
)

# Tipelibs
typelib_dir = os.path.join(base, "gi_typelibs")

if os.path.isdir(typelib_dir):
    os.environ["GI_TYPELIB_PATH"] = (
        typelib_dir
        + os.pathsep
        + os.environ.get("GI_TYPELIB_PATH", "")
    )

# Datos GTK
os.environ["GTK_DATA_PREFIX"] = base
os.environ["GTK_EXE_PREFIX"] = base
PYTHON

HOOK_WIN="$(cygpath -aw "$HOOK")"

[[ -f "$HOOK" ]] ||
    error "No se pudo crear el runtime hook."

# =====================================================
# RECOPILAR DLL
# =====================================================

echo ""
echo "Recopilando DLL de GTK4..."

DLL_ARGS=()

shopt -s nullglob

for dll in "$GTK_BIN"/*.dll; do
    DLL_ARGS+=(--add-binary "$(cygpath -aw "$dll");.")
done

shopt -u nullglob

[[ ${#DLL_ARGS[@]} -gt 0 ]] ||
    error "No se encontraron DLL en UCRT64/bin."

echo "DLL encontradas: ${#DLL_ARGS[@]}"

# =====================================================
# COMPROBAR ICONO
# =====================================================

ICON_ARGS=()

if [[ -f "$ROOT/assets/icon.ico" ]]; then
    ICON_ARGS+=(--icon "$(cygpath -aw "$ROOT/assets/icon.ico")")
else
    echo "AVISO: No existe assets/icon.ico. Se compilará sin icono."
fi

# =====================================================
# LIMPIAR COMPILACIONES
# =====================================================

echo ""
echo "Limpiando compilaciones anteriores..."

rm -rf "$DIST" "$BUILD"

mkdir -p "$BUILD"

# Volver a crear el hook después de limpiar
mkdir -p "$HOOK_DIR"

cat > "$HOOK" <<'PYTHON'
import os
import sys

base = getattr(
    sys,
    "_MEIPASS",
    os.path.dirname(sys.executable)
)

os.environ["PATH"] = (
    base + os.pathsep + os.environ.get("PATH", "")
)

typelib_dir = os.path.join(base, "gi_typelibs")

if os.path.isdir(typelib_dir):
    os.environ["GI_TYPELIB_PATH"] = (
        typelib_dir
        + os.pathsep
        + os.environ.get("GI_TYPELIB_PATH", "")
    )

os.environ["GTK_DATA_PREFIX"] = base
os.environ["GTK_EXE_PREFIX"] = base
PYTHON

HOOK_WIN="$(cygpath -aw "$HOOK")"

# =====================================================
# COMPILAR
# =====================================================

echo ""
echo "Compilando aplicación..."

"$PYTHON" -m PyInstaller \
    --noconfirm \
    --clean \
    --onedir \
    --console \
    --name "$APP" \
    --paths "$ROOT_WIN/src" \
    --hidden-import=gi \
    --hidden-import=gi.repository \
    --hidden-import=gi.repository.Gtk \
    --hidden-import=gi.repository.Gdk \
    --hidden-import=gi.repository.Gio \
    --hidden-import=gi.repository.GObject \
    --hidden-import=gi.repository.GdkPixbuf \
    --collect-submodules=gi \
    --add-data "$(cygpath -aw "$ROOT/assets");assets" \
    --add-data "$TYPELIBS_WIN;gi_typelibs" \
    --runtime-hook "$HOOK_WIN" \
    "${DLL_ARGS[@]}" \
    "${ICON_ARGS[@]}" \
    "$MAIN_WIN"

# =====================================================
# COMPROBAR RESULTADO
# =====================================================

EXE="$DIST/$APP/$APP.exe"

[[ -f "$EXE" ]] ||
    error "PyInstaller no ha generado el ejecutable."

# =====================================================

# DISTRIBUCIÓN
# =====================================================

echo ""
echo "Preparando distribución..."

rm -rf "$RELEASE"
mkdir -p "$RELEASE"

cp -a "$DIST/$APP/." "$RELEASE/"

# =====================================================
# RESULTADO
# =====================================================

echo ""
echo "=========================================="
echo " COMPILACIÓN FINALIZADA"
echo "=========================================="

echo "Ejecutable:"
echo "$RELEASE/$APP.exe"

echo ""
echo "Distribución:"
echo "$RELEASE"

echo ""
echo "Distribuir toda la carpeta."
echo "=========================================="