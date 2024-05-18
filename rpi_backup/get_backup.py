import os
import datetime
import subprocess

base_directory = r"D:\Raspberry Pi Service Backups"
filename = f"services-{datetime.date.today()}.zip"

if os.path.exists(fr"{base_directory}\filename"):
    exit(0)

remote_user = "aleksandar"
remote_host = "192.168.100.3"
remote_path = r"~\services"
local_path = fr"{base_directory}\{filename}"

subprocess.run(fr'scp {remote_user}@{remote_host}:{remote_path}/{filename} "{local_path}"')

print(filename)