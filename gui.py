import tkinter as tk
from tkinter import ttk
from device_info import get_ios_device_info, save_to_csv
import subprocess
import time

class DeviceInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Device Info")
        self.root.geometry("400x200")

        # Set the background color and font for the main frame
        self.main_frame = ttk.Frame(self.root, style='Main.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a header with "Creator" text
        self.header_label = ttk.Label(self.main_frame, text="Creator", font=("Helvetica", 16), foreground='green', background='black')
        self.header_label.pack(pady=10)

        # Set the style for the main frame
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Main.TFrame', background='black')
        self.style.configure('TLabel', foreground='white', background='black')

        # Create a label to display the connected device
        self.label = ttk.Label(self.main_frame, text="Connected Device: None")
        self.label.pack(pady=10)

    def scan_devices(self):
        ios_devices = subprocess.run(['/usr/local/bin/ideviceenumerate'], capture_output=True, text=True)
        android_devices = subprocess.run(['adb', 'devices'], capture_output=True, text=True)

        if not ios_devices.stdout and not android_devices.stdout:
            self.label.config(text="Connected Device: None")
        else:
            for line in ios_devices.stdout.splitlines():
                serial_number = line.strip()
                try:
                    device_info = get_ios_device_info(serial_number)
                    save_to_csv(device_info)
                    self.label.config(text=f"iOS Device info saved to CSV. Serial: {device_info['serial']}")
                except Exception as e:
                    print(f"Error processing iOS device {serial_number}: {e}")

            for line in android_devices.stdout.splitlines():
                if 'device' in line and not line.startswith('List of devices attached'):
                    serial_number = line.strip().split('\t')[0]
                    try:
                        device_info = get_android_device_info(serial_number)
                        save_to_csv(device_info)
                        self.label.config(text=f"Android Device info saved to CSV. Serial: {device_info['serial']}")
                    except Exception as e:
                        print(f"Error processing Android device {serial_number}: {e}")

    def run(self):
        while True:
            self.scan_devices()
            time.sleep(5 + (time.time() % 2))  # Sleep for 5-7 seconds

if __name__ == "__main__":
    root = tk.Tk()
    app = DeviceInfoApp(root)
    app.run()
