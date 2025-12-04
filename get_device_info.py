# get_device_info.py
import yaml
from netmiko import ConnectHandler
from datetime import datetime
import os
from getpass import getpass

def load_devices(path="devices.yaml"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found. Copy devices.example.yaml -> devices.yaml and update.")
    with open(path) as f:
        data = yaml.safe_load(f)
    return data.get("devices", [])

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def connect_and_collect(dev, commands):
    device_dict = {
        "device_type": dev.get("device_type"),
        "ip": dev.get("host"),
        "username": dev.get("username"),
        "password": dev.get("password"),
    }
    # If password is missing in devices.yaml, prompt for it
    if not device_dict["password"]:
        device_dict["password"] = getpass(f"Password for {dev.get('name') or dev['host']}: ")

    if dev.get("secret"):
        device_dict["secret"] = dev.get("secret")

    connection = ConnectHandler(**device_dict)
    if device_dict.get("secret"):
        connection.enable()

    all_output = ""
    for cmd in commands:
        out = connection.send_command(cmd)
        header = f"\n\n=== {cmd} ===\n"
        all_output += header + out

    connection.disconnect()
    return all_output

def main():
    try:
        devices = load_devices()
    except Exception as e:
        print(e)
        return

    ensure_dir("backups")
    commands = ["show ip interface brief", "show version"]

    for dev in devices:
        host = dev.get("host")
        name = dev.get("name", host)
        print(f"\n--- Connecting to {name} ({host}) ---")
        try:
            output = connect_and_collect(dev, commands)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = name.replace(" ", "_")
            filename = f"backups/{safe_name}_{host}_{timestamp}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Saved output to {filename}")
        except Exception as e:
            print(f"Error connecting to {host}: {e}")

if __name__ == "__main__":
    main()
