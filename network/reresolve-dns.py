import platform
import subprocess
import os
import re
import time

if platform.system() == "Windows":
    # Run with admin privileges.
    config_dir = f"{os.getenv('USERPROFILE')}\\Documents\\WireGuard Configurations"
    for filename in os.listdir(config_dir):
        interface_name = filename.split(".")[0]
        with open(f"{config_dir}\\{filename}") as config_file:
            endpoint_line = list(filter(lambda line: "Endpoint" in line, config_file.readlines()))[0]
            endpoint_name = re.split(':|\s', endpoint_line)[-2]
            nslookup = subprocess.run(["nslookup", endpoint_name, "8.8.8.8"], capture_output=True).stdout
            address_line = nslookup.decode().splitlines()[-2]
            address = address_line.split()[-1]
            wg = subprocess.run(["wg", "show", interface_name], capture_output=True).stdout
            wg_lines = wg.decode().splitlines()
            endpoint_line = list(filter(lambda line: "endpoint" in line, wg_lines))[0]
            endpoint_ip = endpoint_line.split()[-1].split(":")[0]

        if address != endpoint_ip:
            subprocess.run(["wireguard", "/uninstalltunnelservice", interface_name])
            time.sleep(1)
            subprocess.run(["wireguard", "/installtunnelservice", f"{config_dir}\\{filename}"])
            print("Old ip "+address+" new ip "+endpoint_ip)
        else:
            print("Address is up to date")
else:
    print("OS not supported yet")
