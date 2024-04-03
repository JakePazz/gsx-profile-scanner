
def prefix(severity: str) -> str:
    from datetime import datetime
    return f"[{severity}] [{datetime.isoformat(datetime.now())}]"

def log(severity: str, message: str, log_file: str = "log") -> None:
    """
What {message} to send to log: string
The {severity} of message: 'info', 'error', 'warn'
    """
    from os import path, mkdir
    if not path.exists("./logs"):
        mkdir("./logs")
        
    with open(f"./logs/{log_file}.txt", "a") as log_file:

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
    from rich import print as rich_print
    from rich.markdown import Markdown
    try:
        rich_print(Markdown("---"))
    except Exception as error:
        log("warn", f"Failed to print_line() with error: {error}")

def retrieve_config(config_file: str, config_item: str):
    # Retrieve one item from either program_config or scan_config
    from json import load
    try:
        with open(f"./configs/{config_file}.json", "r") as file:
            config_data: dict = load(file)
        log("info",f"Successfully retrieved item ({config_item}) from file ({config_file})")
    except Exception as error:
        log("warn", f"retrieve_config() failed to retrieve config_item ({config_item}) from file ({config_file}) with error: {error}")
        return False
    return config_data[config_item]
    # TODO: Add in error checking for the final return

if __name__ == "__main__":
    open_profile_folder()
    print(retrieve_config("program_config", "recognised_profile_name_split_types"))


