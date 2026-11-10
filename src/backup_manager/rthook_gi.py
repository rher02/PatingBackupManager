import os
import sys

# Directorio interno de PyInstaller
base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))

# Añadir las DLL empaquetadas al PATH
os.environ["PATH"] = (
    base
    + os.pathsep
    + os.environ.get("PATH", "")
)

# Directorio de introspección GObject
typelib_dir = os.path.join(base, "gi_typelibs")

os.environ["GI_TYPELIB_PATH"] = (
    typelib_dir
    + os.pathsep
    + os.environ.get("GI_TYPELIB_PATH", "")
)