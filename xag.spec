# -*- mode: python -*-

from importlib import import_module
from pathlib import Path
import os
import sys

from PyInstaller import __version__ as pyinstaller_version

# Increase recursion limit
sys.setrecursionlimit(sys.getrecursionlimit() * 10)

name = "skybrushd"
single_file = False   # <<< IMPORTANT: SET FOR onedir MODE

root_dir = Path.cwd()
src_dir = root_dir / "src"

###########################################################################
# Encryption (optional)
key = os.environ.get("PYINSTALLER_KEY")

if pyinstaller_version >= "4.0":
    if not key:
        import secrets
        key = secrets.token_urlsafe(24)
else:
    if key:
        raise RuntimeError("Encryption not supported")

###########################################################################
# Prevent TkInter from being bundled
sys.modules["FixTk"] = None

# Extra modules to include
extra_modules = set([
    "flockwave.server.config",
    "scipy._lib.array_api_compat.numpy.fft",
    "scipy._lib.array_api_compat.numpy.linalg",
    "scipy._lib.array_api_compat.numpy.random",
    "flockwave.spec"
])

# Modules to exclude
exclude_modules = [
    "FixTk", "tcl", "tk", "_tkinter", "tkinter", "Tkinter",
    "lxml"
]

###########################################################################
# Load the server configuration file
config_file = src_dir / "flockwave" / "server" / "config.py"
config = {}
exec(
    compile(open(config_file).read(), "config.py", "exec", dont_inherit=True),
    None,
    config
)

###########################################################################
# Extension helpers
def extension_module(name):
    return f"flockwave.server.ext.{name}"

def is_extension_module(name):
    return name.startswith("flockwave.server.ext.")

# Add ext manager + config extensions
extra_modules.add(extension_module("ext_manager"))
extra_modules.update(
    extension_module(ext)
    for ext in config["EXTENSIONS"]
    if not ext.startswith("_")
)

###########################################################################
# Resolve dependencies recursively
changed = True
while changed:
    changed = False
    for module_name in sorted(extra_modules):
        if is_extension_module(module_name):
            try:
                imported = import_module(module_name)
                deps = set()

                if hasattr(imported, "get_dependencies"):
                    deps.update(imported.get_dependencies())
                elif hasattr(imported, "dependencies"):
                    deps.update(imported.dependencies)

                new = {extension_module(d) for d in deps} - extra_modules
                if new:
                    extra_modules.update(new)
                    changed = True

            except ImportError:
                pass

###########################################################################
# PyInstaller analysis
a = Analysis(
    [str(src_dir / "flockwave" / "server" / "__main__.py")],
    pathex=[str(src_dir)],
    binaries=[],
    datas=[],
    hiddenimports=sorted(extra_modules),
    hookspath=[root_dir / "etc" / "deployment" / "pyinstaller"],
    runtime_hooks=[root_dir / "etc" / "deployment" / "pyinstaller" / "runtime_hook.py"],
    excludes=exclude_modules,
)

pyz = PYZ(a.pure, a.zipped_data)

###########################################################################
# Create EXE (onedir mode)
exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name=name,
    debug=False,
    strip=False,
    upx=True,
    console=True
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name=name
)
