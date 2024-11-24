import subprocess
import os
import platform

__current_dir_path = os.path.dirname(os.path.abspath(__file__))

__LAUNCH_CONFIG = [
    (  # vr_kitchen
        # venv path
        os.path.join(__current_dir_path, "vr_kitchen", "venv"),
        # script path
        os.path.join(__current_dir_path, "vr_kitchen", "main.py"),
        # launch args
        [
            "--mode", "vr",  # ['headless', 'headless_tensor', 'gui_non_interactive', 'gui_interactive', 'vr']
            "--kitchen", "none",  # file path of the kitchen layout
            "--config", "steak_mid_2.tml",  # name of the config file
            # "--practice",  # Flag to indicate whether this is a practice session
        ]
    ),
    (  # fov_aware_planner
        # venv_path
        os.path.join(__current_dir_path, "fov_aware_planner", "venv"),
        # script path
        os.path.join(__current_dir_path, "fov_aware_planner", "overcooked_ai_py", "steak_api_test.py"),
        # launch args
        [
            "--layout", "steak_mid_2",  # name of the layout map to load
            "--vision", "1",  # 0 for fov unaware and 1 for fov aware robot agent
        ]
    )
]


def launch_in_terminal(venv_path, script_path, args):
    python_executable = os.path.join(venv_path, "Scripts", "python.exe") if platform.system() == "Windows" \
        else os.path.join(venv_path, "bin", "python")

    if not os.path.exists(python_executable):
        raise FileNotFoundError(f"Python executable not found in virtual environment: {python_executable}")

    command = f'"{python_executable}" "{script_path}" ' + " ".join(args)

    if platform.system() == "Windows":
        terminal_command = ["cmd.exe", "/c", f"start cmd.exe /k {command}"]
    elif platform.system() == "Linux":
        terminal_command = ["gnome-terminal", "--", "bash", "-c", f"{command}; exec bash"]
    elif platform.system() == "Darwin":
        escaped_command = command.replace('"', '\\"')
        terminal_command = ["osascript", "-e", f'tell application "Terminal" to do script "{escaped_command}"']
    else:
        raise NotImplementedError(f"Unsupported platform: {platform.system()}")

    subprocess.Popen(terminal_command)

if __name__ == "__main__":
    try:
        launch_in_terminal(*__LAUNCH_CONFIG[0])
        launch_in_terminal(*__LAUNCH_CONFIG[1])

        print("Both processes have been launched in separate terminals.")

    except Exception as e:
        print(f"[ERROR]:\n{e}")
