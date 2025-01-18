import cv2
import numpy as np
import os
import platform
import subprocess
import threading
import time
import win32gui
import win32ui
import win32con

__current_dir_path = os.path.dirname(os.path.abspath(__file__))

__SCREEN_RECORDING_CONFIG = {
    'VR': {
        'window_title': 'VR',
        'output_path': os.path.join(__current_dir_path, 'recordings', 'vr_fov_aware_planner.avi'),
        'fps': 30
    },
    'PLANNER': {
        'window_title': 'PLANNER',
        'output_path': os.path.join(__current_dir_path, 'recordings', 'vr_fov_aware_planner.avi'),
        'fps': 30
    },
}

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
            "--vision", "1",  # 0 for fov unaware and 1 for fov aware robot agent
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

class WindowClosedException(Exception):
    pass

class Recorder:
    def __init__(self, window_title=None, output_path=None, fps=30, **kwargs):
        self.window_title = window_title
        self.window_handle = None
        self.output_path = output_path or f"recording_{int(time.time())}.avi"
        self.fps = fps
        self.is_recording = False
        self.video_writer = None
        self.record_thread = None

        if self.window_title:
            self.set_window_handle()

    def set_window_handle(self):
        self.window_handle = win32gui.FindWindow(None, self.window_title)
        if not self.window_handle:
            raise ValueError(f"Window with title '{self.window_title}' not found")

    def get_window_dimensions(self):
        if not self.window_handle:
            raise ValueError("Window handle not set")
        rect = win32gui.GetWindowRect(self.window_handle)
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        return width, height

    def window_exists(self):
        try:
            win32gui.GetWindowPlacement(self.window_handle)
            return True
        except Exception:
            return False

    def capture_window(self):
        if not self.window_handle:
            raise ValueError("Window handle not set")

        if not self.window_exists():
            raise WindowClosedException("Target window no longer exists")

        width, height = self.get_window_dimensions()

        window_dc = win32gui.GetWindowDC(self.window_handle)
        dc_obj = win32ui.CreateDCFromHandle(window_dc)
        compatible_dc = dc_obj.CreateCompatibleDC()

        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(dc_obj, width, height)
        compatible_dc.SelectObject(bitmap)

        compatible_dc.BitBlt((0, 0), (width, height), dc_obj, (0, 0), win32con.SRCCOPY)

        bitmap_info = bitmap.GetInfo()
        bitmap_bits = bitmap.GetBitmapBits(True)
        img = np.frombuffer(bitmap_bits, dtype=np.uint8)
        img.shape = (height, width, 4)  # RGBA

        win32gui.DeleteObject(bitmap.GetHandle())
        compatible_dc.DeleteDC()
        dc_obj.DeleteDC()
        win32gui.ReleaseDC(self.window_handle, window_dc)

        return cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)

    def record(self):
        width, height = self.get_window_dimensions()

        if not self.video_writer:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video_writer = cv2.VideoWriter(
                str(self.output_path), fourcc, self.fps, (width, height)
            )

        while self.is_recording:
            try:
                if not self.window_exists():
                    print(f"Window '{self.window_title}' was closed, stopping recording")
                    self.is_recording = False
                    break

                frame = self.capture_window()
                self.video_writer.write(frame)
                time.sleep(1 / self.fps)
            except WindowClosedException:
                print(f"Window '{self.window_title}' was closed, stopping recording")
                self.is_recording = False
                break
            except Exception as e:
                print(f"Error during recording: {e}")
                self.is_recording = False
                break

    def start_recording(self):
        if self.is_recording:
            print("Already recording")
            return

        self.is_recording = True
        self.record_thread = threading.Thread(target=self.record)
        self.record_thread.start()

    def stop_recording(self):
        self.is_recording = False
        if self.record_thread:
            self.record_thread.join()

        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None

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

        recorder1 = Recorder(**__SCREEN_RECORDING_CONFIG['VR'])
        recorder2 = Recorder(**__SCREEN_RECORDING_CONFIG['PLANNER'])

        recorder1.start_recording()
        recorder2.start_recording()

        while threading.active_count() > 1:
            time.sleep(1)

    except Exception as e:
        print(f"[ERROR]:\n{e}")

    finally:
        recorder1.stop_recording()
        recorder2.stop_recording()
