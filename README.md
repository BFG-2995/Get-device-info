# get-device-info

A **Python-based network automation tool** using **Netmiko** to SSH into Cisco devices and collect configuration and status outputs safely.  

This project demonstrates secure practices for automating network tasks, including managing credentials, using virtual environments, and saving outputs.

---

## Features

- Connects to multiple devices defined in a YAML file.
- Executes commands such as:
  - `show ip interface brief`
  - `show version`
- Saves output in `backups/` folder with timestamped filenames.
- Prompts for passwords at runtime if omitted, improving security.
- Supports easy expansion for additional commands or devices.

---

## Project Structure

get-device-info/
.venv/ # Local virtual environment (ignored by GitHub)
get_device_info.py # Main Python script
devices.example.yaml # Example device configuration (safe to commit)
devices.yaml # Local device configuration (do NOT commit)
requirements.txt # Python dependencies
.gitignore # Files/folders to ignore in Git
README.md # This file
backups/ # Script outputs (ignored by GitHub)

**Create and activate a virtual environment**
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

Install dependencies
pip install -r requirements.txt

Configure devices

Copy the example device file:
copy devices.example.yaml devices.yaml   # Windows
# cp devices.example.yaml devices.yaml  # macOS/Linux

Edit devices.yaml with your device info:
devices:
  - name: R1
    device_type: cisco_ios
    host: <DEVICE_IP>
    username: <USERNAME>
    password: ""        # Leave blank to be prompted
    secret: <ENABLE_PASSWORD>

Important: Never commit devices.yaml — it contains real credentials. .gitignore already excludes it.

Usage

Run the main script:
python get_device_info.py
If passwords are blank in devices.yaml, you will be prompted at runtime.

Script outputs are saved in backups/ with filenames like:

backups/R1_192.168.1.10_20251204_150102.txt
Security Best Practices

Keep real credentials out of GitHub.

.gitignore prevents committing:

devices.yaml (local credentials)

.venv/ (virtual environment)

backups/ (output logs)

*.pyc, __pycache__/ (Python cache)

For CI/CD or scheduled jobs, use GitHub Secrets or a secure vault instead of storing passwords in files.

Leave password blank in devices.yaml and enter it at runtime for safety.
Dependencies

Python 3.8+

Netmiko

PyYAML

Install all dependencies via:
pip install -r requirements.txt

Auther
Thiwanka Rathnayaka

