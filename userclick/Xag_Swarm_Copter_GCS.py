import os
import sys
import subprocess
import time
import ctypes


# ---------- Admin elevation ----------
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if not is_admin():
    # Relaunch this script as admin
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()
# Path where master.exe is running
EXE_DIR = os.path.dirname(os.path.abspath(sys.executable))

server_path = os.path.join(
    EXE_DIR,
    "server",
    "operation_server.exe -c ./server/etc/conf/skybrush-outdoor.jsonc",
)
gui_path = os.path.join(EXE_DIR, "gui", "gui.exe")

print("SERVER:", server_path)
print("GUI:", gui_path)

subprocess.Popen(server_path)
time.sleep(5)
subprocess.Popen(gui_path)
