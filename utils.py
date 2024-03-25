# Use a class here for sessionlog (so timestamp can be got in __init__ and then be used for getting file loc when needed)
import os
from datetime import datetime
from json import load

def prefix(severity: str) -> str:
    return f"[{severity}] [{datetime.isoformat(datetime.now())}]"

def log(severity: str, message: str) -> None:
    """
What {message} to send to log: string
The {severity} of message: 'info', 'error', 'warn'
    """
    if not os.path.exists("./logs"):
        os.mkdir("./logs")
        
    with open(f"./logs/log.txt", "a") as log_file:

        if severity not in ['info', 'error', 'warn']:
            log_file.write(f"\n{prefix("UNKNOWN")} {message.strip()}")
        else:
            log_file.write(f"\n{prefix(severity)} {message.strip()}")

def retrieve_path():
    # Retrieve path of GSX profiles folder - only for user AFTER SETUP
    # TODO: Add validation
    with open("./configs/scan_config.json","r") as scan_config_file:
        scan_config = load(scan_config_file)
        return scan_config["profile_folder_path"]
