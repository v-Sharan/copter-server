import os
import subprocess
import time


class TerminalManager:
    def __init__(self, working_dir, venv_path, script_path):
        self.working_dir = working_dir
        self.venv_path = venv_path
        self.script_path = script_path
        self.process_name = "cmd.exe"

    def _kill_existing_terminal(self):
        try:
            output = subprocess.check_output(
                f'tasklist /FI "IMAGENAME eq {self.process_name}"', shell=True
            ).decode()
            if self.process_name in output:
                print(f"{self.process_name} is running, killing it...")
                subprocess.call(f"taskkill /F /IM {self.process_name}", shell=True)
                time.sleep(1)
        except Exception as e:
            print("Error checking/killing process:", e)

    def _build_command(self):
        """Build the full command safely using os.path"""
        script_name = os.path.basename(self.script_path)  # Just the script filename
        script_dir = os.path.dirname(self.script_path)  # Directory of the script

        cmd = (
            f"cd /d {self.working_dir} && "
            f"call {self.venv_path}\\activate && "
            f"cd {script_dir} && "
            f"python {script_name} && "
            "pause"
        )
        return cmd

    def restart_terminal(self):
        self._kill_existing_terminal()
        cmd = self._build_command()
        subprocess.Popen(f'start cmd /k "{cmd}"', shell=True)
        print("New terminal opened.")


# Example usage:
if __name__ == "__main__":
    tm = TerminalManager(
        working_dir=r"D:\nithya",
        venv_path=r"D:\nithya\myenv\Scripts",
        script_path=r"copter\swarm_tasks\Examples\basic_tasks\copter_swarm_modified.py",
    )
    tm.restart_terminal()
