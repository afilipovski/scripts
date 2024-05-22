import logging
import os
import platform
import re
import subprocess
import time
from logging.handlers import TimedRotatingFileHandler

from dns import resolver

res = resolver.Resolver()
res.nameservers = ['8.8.8.8', '8.8.4.4', '1.1.1.1', '1.0.0.1']

logger = logging.getLogger("ReresolveDnsLogger")
logger.setLevel(logging.DEBUG)

handler = TimedRotatingFileHandler(
    r"C:\Users\Aleksandar\PycharmProjects\scripts\network\reresolve-dns.log",
    when="midnight",
    interval=1,
    backupCount=1
)

formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

def get_hostname_ip(hostname: str) -> str:
    answers = res.resolve(qname=hostname)
    for rdata in answers:
        return rdata.address


def get_hostname_config(filepath: str) -> str:
    with open(filepath) as config_file:
        endpoint_line = list(filter(lambda line: "Endpoint" in line, config_file.readlines()))[0]
        return re.split(':|\s', endpoint_line)[-2]


def get_wg_ip(interface_name: str) -> str:
    wg = subprocess.run(["wg", "show", interface_name], capture_output=True).stdout
    wg_lines = wg.decode().splitlines()
    endpoint_line = list(filter(lambda line: "endpoint" in line, wg_lines))[0]
    return endpoint_line.split()[-1].split(":")[0]


if platform.system() == "Windows":
    # Run with admin privileges.
    config_dir = f"{os.getenv('USERPROFILE')}\\Documents\\WireGuard Configurations"
else:
    print("OS not supported yet")
    exit(1)

for filename in os.listdir(config_dir):
    interface = filename.split(".")[0]
    endpoint_name = get_hostname_config(f"{config_dir}\\{filename}")

    try:
        address = get_hostname_ip(endpoint_name)
        endpoint_ip = get_wg_ip(interface)
        if address != endpoint_ip:
            subprocess.run(["wireguard", "/uninstalltunnelservice", interface])
            time.sleep(1)
            subprocess.run(["wireguard", "/installtunnelservice", f"{config_dir}\\{filename}"])
            logger.info("Old ip " + address + " new ip " + endpoint_ip)
        else:
            logger.info("Address is up to date")
    except resolver.LifetimeTimeout:
        logger.error(f"DNS could not be resolved for hostname {endpoint_name}")
    except IndexError:
        logger.error(f"Interface {interface} is not active.")
