import csv
from datetime import datetime
import subprocess
import time

# Mapping from numeric model codes to human-readable model names
model_codes = {
    'iPhone 12': 'iPhone 12',
    'iPhone 12 Pro': 'iPhone 12 Pro',
    'iPhone 12 Pro Max': 'iPhone 12 Pro Max',
    'iPhone 13': 'iPhone 13',
    'iPhone 13 Pro': 'iPhone 13 Pro',
    'iPhone 13 Pro Max': 'iPhone 13 Pro Max',
    'iPhone 14': 'iPhone 14',
    'iPhone 14 Plus': 'iPhone 14 Plus',
    'iPhone 14 Pro': 'iPhone 14 Pro',
    'iPhone 14 Pro Max': 'iPhone 14 Pro Max',
    # Add more mappings as needed
}

def get_ios_device_info(device):
    info = {}
    try:
        info['serial'] = device.serial_number
        
        # Get model name using ideviceinfo
        result = subprocess.run(['ideviceinfo', '-s', device.serial_number, '-k', 'ProductType'], capture_output=True, text=True)
        if result.returncode == 0:
            model_code = result.stdout.strip()
            if model_code in model_codes:
                info['model'] = model_codes[model_code]
            else:
                info['model'] = 'Unknown'
        else:
            print(f"Error getting model name: {result.stderr}")
        
        # Get OS version using ideviceinfo
        result = subprocess.run(['ideviceinfo', '-s', device.serial_number, '-k', 'ProductVersion'], capture_output=True, text=True)
        if result.returncode == 0:
            info['os_version'] = result.stdout.strip()
        else:
            print(f"Error getting OS version: {result.stderr}")
        
        # Get battery level using ideviceinfo
        result = subprocess.run(['ideviceinfo', '-s', device.serial_number, '-k', 'BatteryLevel'], capture_output=True, text=True)
        if result.returncode == 0:
            info['battery_level'] = float(result.stdout.strip())
        else:
            print(f"Error getting battery level: {result.stderr}")
        
        # Get network type using ideviceinfo
        result = subprocess.run(['ideviceinfo', '-s', device.serial_number, '-k', 'NetworkType'], capture_output=True, text=True)
        if result.returncode == 0:
            info['network_type'] = result.stdout.strip()
        else:
            print(f"Error getting network type: {result.stderr}")
        
        # Get WiFi address using ideviceinfo
        result = subprocess.run(['ideviceinfo', '-s', device.serial_number, '-k', 'WiFiAddress'], capture_output=True, text=True)
        if result.returncode == 0:
            info['wifi_address'] = result.stdout.strip()
        else:
            print(f"Error getting WiFi address: {result.stderr}")
        
        # Get cellular data enabled status using ideviceinfo
        result = subprocess.run(['ideviceinfo', '-s', device.serial_number, '-k', 'CellularDataEnabled'], capture_output=True, text=True)
        if result.returncode == 0:
            info['cellular_data_enabled'] = result.stdout.strip() == '1'
        else:
            print(f"Error getting cellular data enabled status: {result.stderr}")
        
        # Get touch ID enabled status using ideviceinfo
        result = subprocess.run(['ideviceinfo', '-s', device.serial_number, '-k', 'TouchIDEnrolled'], capture_output=True, text=True)
        if result.returncode == 0:
            info['touch_id_enabled'] = result.stdout.strip() == '1'
        else:
            print(f"Error getting touch ID enabled status: {result.stderr}")
        
        # Get storage capacity using ideviceinfo
        result = subprocess.run(['ideviceinfo', '-s', device.serial_number, '-k', 'DiskUsage'], capture_output=True, text=True)
        if result.returncode == 0:
            disk_info = result.stdout.strip().split()
            total_space = int(disk_info[0])
            free_space = int(disk_info[1])
            used_space = total_space - free_space
            info['storage_total'] = total_space
            info['storage_free'] = free_space
            info['storage_used'] = used_space
        else:
            print(f"Error getting storage capacity: {result.stderr}")
        
        # Get model color using ideviceinfo
        result = subprocess.run(['ideviceinfo', '-s', device.serial_number, '-k', 'ProductColor'], capture_output=True, text=True)
        if result.returncode == 0:
            info['model_color'] = result.stdout.strip()
        else:
            print(f"Error getting model color: {result.stderr}")
        
    except Exception as e:
        print(f"Error getting device info: {e}")
    return info

def get_android_device_info(serial_number):
    info = {}
    try:
        info['serial'] = serial_number
        
        # Get model name using adb
        result = subprocess.run(['adb', '-s', serial_number, 'shell', 'getprop', 'ro.product.model'], capture_output=True, text=True)
        if result.returncode == 0:
            info['model'] = result.stdout.strip()
        else:
            print(f"Error getting model name: {result.stderr}")
        
        # Get OS version using adb
        result = subprocess.run(['adb', '-s', serial_number, 'shell', 'getprop', 'ro.build.version.release'], capture_output=True, text=True)
        if result.returncode == 0:
            info['os_version'] = result.stdout.strip()
        else:
            print(f"Error getting OS version: {result.stderr}")
        
        # Get battery level using adb
        result = subprocess.run(['adb', '-s', serial_number, 'shell', 'dumpsys', 'battery'], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if 'level' in line:
                    info['battery_level'] = float(line.split(':')[1].strip())
                    break
        else:
            print(f"Error getting battery level: {result.stderr}")
        
        # Get network type using adb
        result = subprocess.run(['adb', '-s', serial_number, 'shell', 'dumpsys', 'connectivity'], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if 'connected' in line and 'wifi' in line:
                    info['network_type'] = 'WiFi'
                    break
                elif 'connected' in line and 'cellular' in line:
                    info['network_type'] = 'Cellular'
                    break
        else:
            print(f"Error getting network type: {result.stderr}")
        
        # Get WiFi address using adb
        result = subprocess.run(['adb', '-s', serial_number, 'shell', 'dumpsys', 'wifi'], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if 'BSSID' in line:
                    info['wifi_address'] = line.split(':')[1].strip()
                    break
        else:
            print(f"Error getting WiFi address: {result.stderr}")
        
        # Get storage capacity using adb
        result = subprocess.run(['adb', '-s', serial_number, 'shell', 'df'], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if '/data' in line and 'data' not in line:
                    parts = line.split()
                    total_space = int(parts[1])
                    free_space = int(parts[3])
                    used_space = total_space - free_space
                    info['storage_total'] = total_space
                    info['storage_free'] = free_space
                    info['storage_used'] = used_space
                    break
        else:
            print(f"Error getting storage capacity: {result.stderr}")
        
    except Exception as e:
        print(f"Error getting device info: {e}")
    return info

def save_to_csv(device_info, filename='device_info.csv'):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(['Date', 'Serial Number', 'Model', 'OS Version', 'Battery Level', 'Network Type', 'WiFi Address', 'Cellular Data Enabled', 'Touch ID Enabled', 'Storage Total', 'Storage Free', 'Storage Used', 'Model Color'])
        writer.writerow([datetime.now(), device_info['serial'], device_info['model'], device_info['os_version'], device_info.get('battery_level', ''), device_info.get('network_type', ''), device_info.get('wifi_address', ''), '', '', device_info.get('storage_total', ''), device_info.get('storage_free', ''), device_info.get('storage_used', ''), ''])

def main():
    while True:
        ios_devices = subprocess.run(['ideviceenumerate'], capture_output=True, text=True)
        android_devices = subprocess.run(['adb', 'devices'], capture_output=True, text=True)

        if not ios_devices.stdout and not android_devices.stdout:
            print("No devices found.")
        else:
            for line in ios_devices.stdout.splitlines():
                serial_number = line.strip()
                try:
                    device_info = get_ios_device_info(serial_number)
                    save_to_csv(device_info)
                    print(f"iOS Device info saved to CSV. Serial: {device_info['serial']}")
                except Exception as e:
                    print(f"Error processing iOS device {serial_number}: {e}")

            for line in android_devices.stdout.splitlines():
                if 'device' in line and not line.startswith('List of devices attached'):
                    serial_number = line.strip().split('\t')[0]
                    try:
                        device_info = get_android_device_info(serial_number)
                        save_to_csv(device_info)
                        print(f"Android Device info saved to CSV. Serial: {device_info['serial']}")
                    except Exception as e:
                        print(f"Error processing Android device {serial_number}: {e}")

        # Wait for 5-7 seconds before scanning again
        time.sleep(5 + (time.time() % 2))

if __name__ == "__main__":
    main()
