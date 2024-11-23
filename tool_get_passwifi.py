# ! py
# Tool get pass wifi
# Copyright in youtube 

import subprocess
data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split("\n")
profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
for i in profiles:
    try:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split("\n")
        key_content = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        password = key_content[0] if key_content else ""
        print("Wifi: {:<30}|  Pass: {:<}".format(i, password))
    except subprocess.CalledProcessError:
        print("Wifi: {:<30}|  Pass: {:<}".format(i, "Error retrieving password"))
