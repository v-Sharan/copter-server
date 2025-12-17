import os
import sys
import subprocess
import time

simulation_process = None


def simulation_exe(
    home_lat: float,
    home_lon: float,
    home_alt=0,
    count: int = 1,
    spacing: int = 30,
    col: int = 0,
    row: int = 0,
    server_address="127.0.0.1",
    pattern="Line",
):

    # Path where master.exe is running
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to simulation.exe
    server_exe = os.path.join(base_dir, "../simulator", "sim_launcher.exe")
    ardu_exe_path = os.path.join(base_dir, "../simulator", "arducopter.exe")
    print("Looking for:", server_exe, ardu_exe_path)

    if not os.path.exists(server_exe) and not os.path.exists(ardu_exe_path):
        print("ERROR: simulator.exe not found!")
        flag_exe = False
        pass
    else:
        flag_exe = True

    cmdlist = [
        server_exe,
        "--exe",
        ardu_exe_path,
        "--model",
        "quad",
        "-n",
        count,
        "--spacing",
        spacing,
        "--home-lat",
        str(home_lat),
        "--home-lon",
        str(home_lon),
        "--sec-address",
        server_address,
        "--pattern",
        pattern.lower(),
    ]
    if col not in (None, "None"):
        cmdlist.extend(["--col", str(col)])

    if row not in (None, "None"):
        cmdlist.extend(["--row", str(row)])

    print("Command List:", cmdlist)
    if flag_exe:
        print("Starting Simulation...")
        simulation_process = subprocess.Popen(
            cmdlist, creationflags=subprocess.CREATE_NEW_CONSOLE
        )  # run silently
        print("Server started!", simulation_process)


def stop_simulation():
    global simulation_process
    if not simulation_process:
        print("No simulation process found")
        return

    if simulation_process.poll() is None:
        print("Stopping Simulation...")
        simulation_process.terminate()  # Graceful stop

        try:
            simulation_process.wait(timeout=5)
            print("Simulation stopped successfully")
        except subprocess.TimeoutExpired:
            print("Force killing simulation...")
            simulation_process.kill()
    else:
        print("Simulation already stopped")

    simulation_process = None
