import subprocess
import threading
import time
import os
import platform

__current_dir_path = os.path.dirname(os.path.abspath(__file__))

__LAUNCH_CONFIG = [
    (  # vr_kitchen
        # venv path
        os.path.join(__current_dir_path, "vr_kitchen", "venv"),
        # script directory
        os.path.join(__current_dir_path, "vr_kitchen"),
        # script path
        "main.py",
        # launch args
        [
            "--mode", "vr",  # ['headless', 'headless_tensor', 'gui_non_interactive', 'gui_interactive', 'vr']
            "--kitchen", "none",  # file path of the kitchen layout
            "--config", "steak_mid_2.tml",  # name of the config file
        ],
        # retry args
        (
            1,  # max retries
            4   # relaunch interval in seconds
        ),
    ),
    (  # fov_aware_planner
        # venv path
        os.path.join(__current_dir_path, "fov_aware_planner", "venv"),
        # script directory
        os.path.join(__current_dir_path, "fov_aware_planner", "overcooked_ai_py"),
        # script path
        "steak_api_test.py",
        # launch args
        [
            "--layout", "steak_mid_2",  # name of the layout map to load
            "--vision", "1",  # 0 for fov unaware and 1 for fov aware robot agent
        ],
        # retry args
        (
            5,  # max retries
            4   # relaunch interval in seconds
        ),
    )
]

def run_and_monitor(command, max_retries, relaunch_interval):
    tries = 0
    while tries < max_retries:
        tries += 1
        try:
            print(f"Launching attempt {tries}/{max_retries}: {command}")
            process = subprocess.Popen(command, shell=True)
            process.wait()
            if process.returncode == 0:
                print(f"Process completed successfully: {command}")
                break
            else:
                print(f"Process exited with code {process.returncode}. Restarting...")
        except Exception as exc:
            print(f"Error occurred: {exc}")
        time.sleep(relaunch_interval)
    else:
        print(f"Exceeded max retries for command: {command}")

def launch_in_terminal(venv_path, script_dir, script_name, launch_args, retry_args):
    python_executable = os.path.join(venv_path, "Scripts", "python.exe") if platform.system() == "Windows" \
        else os.path.join(venv_path, "bin", "python")

    if not os.path.exists(python_executable):
        raise FileNotFoundError(f"Python executable not found in virtual environment: {python_executable}")

    command = f'cd "{script_dir}" && "{python_executable}" "{script_name}" ' + " ".join(launch_args)

    thread = threading.Thread(target=run_and_monitor, args=(command, *retry_args,))
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    try:
        for config in __LAUNCH_CONFIG:
            launch_in_terminal(*config)

        print("All processes have been launched and are being monitored.")

        while threading.active_count() > 1:
            time.sleep(1)

    except Exception as e:
        print(f"[ERROR]:\n{e}")
