import os
import sys
import subprocess
import time

import psutil


def is_server_running(exe_name):
    """Check if a process with the given exe_name is running."""
    for proc in psutil.process_iter(["name"]):
        try:
            if proc.info["name"] == exe_name:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


def run_server_exe(sim_enable=False, server_address="127.0.0.1"):

    # Path where master.exe is running
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to swarm.exe
    sim_flag = "--sim-enable" if sim_enable else ""

    server_exe = os.path.join(
        base_dir,
        "../swarm_server",
        "copter_swarm.exe",
    )

    print("Looking for:", server_exe)

    if not os.path.exists(server_exe):
        print("ERROR: swarm.exe not found!")
        flag_exe = False
        pass
    else:
        flag_exe = True
        cmdlist = [server_exe, "--server-address", server_address, sim_flag]

    if flag_exe:
        print("Starting Swarm Server...")
        subprocess.Popen(
            cmdlist, creationflags=subprocess.CREATE_NEW_CONSOLE
        )  # run silently
        print("Server started!")


# if __name__ == "__main__":
#     run_server_exe()
