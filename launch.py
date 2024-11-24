import subprocess
import os
import platform


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
    current_dir_path = os.path.dirname(os.path.abspath(__file__))

    # Paths to virtual environments
    venv1_path = os.path.join(current_dir_path, "vr_kitchen", "venv")
    venv2_path = os.path.join(current_dir_path, "fov_aware_planner", "venv")

    # Paths to Python scripts
    script1_path = os.path.join(current_dir_path, "vr_kitchen", "main.py")
    script2_path = os.path.join(current_dir_path, "fov_aware_planner", "overcooked_ai_py", "steak_api_test.py")

    # Command line arguments for each script
    script1_args = ["-m", "vr", "-c", "steak_mid_2.tml"]
    script2_args = ["-l", "steak_mid_2", "-v", "1"]

    try:
        launch_in_terminal(venv1_path, script1_path, script1_args)
        launch_in_terminal(venv2_path, script2_path, script2_args)

        print("Both processes have been launched in separate terminals.")

    except Exception as e:
        print(f"[ERROR]:\n{e}")
