# Use a class here for sessionlog (so timestamp can be got in __init__ and then be used for getting file loc when needed)


def prefix(severity: str) -> str:
    from datetime import datetime
    return f"[{severity}] [{datetime.isoformat(datetime.now())}]"

def log(severity: str, message: str) -> None:
    """
What {message} to send to log: string
The {severity} of message: 'info', 'error', 'warn'
    """
    from os import path, mkdir
    if not path.exists("./logs"):
        mkdir("./logs")
        
    with open(f"./logs/log.txt", "a") as log_file:

        if severity not in ['info', 'error', 'warn']:
            log_file.write(f"\n{prefix("UNKNOWN")} {message.strip()}")
        else:
            log_file.write(f"\n{prefix(severity)} {message.strip()}")

def retrieve_path() -> None:
    """
Retrieve the path of the GSX Profile folder specified in setup
    """
    
    from json import load

    # Retrieve path of GSX profiles folder - only for user AFTER SETUP
    # TODO: Add validation
    with open("./configs/scan_config.json","r") as scan_config_file:
        scan_config = load(scan_config_file)
        return scan_config["profile_folder_path"]

def open_profile_folder() -> None:
    from os import startfile
    # Open GSX profiles folder in file explorer
    startfile(retrieve_path())

def print_line() -> None:
    from rich import print as prnt
    from rich.markdown import Markdown
    prnt(Markdown("---"))

if __name__ == "__main__":
    open_profile_folder()