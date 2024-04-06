# Upon an exception, functions here will only Exit() if crucial to program function

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
    """Retrieve the path of the GSX Profile folder specified in setup (stored in scan_config)"""
    
    from json import load
    from rich import print as rich_print
    from typer import Exit

    # Retrieve path of GSX profiles folder (only for user after setup)
    try:
        with open("./configs/scan_config.json","r") as scan_config_file:
            scan_config = load(scan_config_file)
            return scan_config["profile_folder_path"]
    except Exception as error:
        rich_print("[red]Error while trying to retrieve GSX Profile Folder[/red]")
        log("error", f"Could not retrieve GSX Profile folder (retrieve_path()) with error: {error}")
        raise Exit()

def open_profile_folder() -> None:
    """Open the GSX Profile folder using stored path"""
    from os import startfile
    from rich import print as rich_print
    from typer import Exit
    # Open GSX profiles folder in file explorer
    try:
        startfile(retrieve_path())
    except Exception as error:
        rich_print("[red]Error while trying to open GSX Profile Folder[/red]")
        log("error", f"Could not open GSX Profile folder (open_profile_folder()) with error: {error}")
        raise Exit()


def print_line() -> None:
    from rich import print as rich_print
    from rich.markdown import Markdown
    try:
        rich_print(Markdown("---"))
    except Exception as error:
        log("warn", f"Failed to print_line() with error: {error}")

def retrieve_config(config_file: str, config_item: str):
    """Retrieve one item from either program_config or scan_config"""
    from json import load
    from rich import print as rich_print
    from typer import Exit
    try:
        with open(f"./configs/{config_file}.json", "r") as file:
            config_data: dict = load(file)
        log("info",f"Successfully retrieved item ({config_item}) from file ({config_file})")
    except Exception as error:
        log("warn", f"retrieve_config() failed to retrieve config_item ({config_item}) from file ({config_file}) with error: {error}")
        return False
    try:
        return config_data[config_item]
    except Exception as error:
        rich_print(f"[red]Error when returning requested config item: {error}[/red]")
        raise Exit()

def print_profiles_folder(profiles_folder_path: str=None):
    from os import scandir
    from rich.tree import Tree
    from rich import print as rich_print

    if profiles_folder_path == None:
        profiles_folder_path = retrieve_path()

    tree = Tree("Profiles Folder", style="green bold", guide_style="grey39 bold")
    try:
        with scandir(profiles_folder_path) as profiles_folder:
            for file in profiles_folder:
                tree.add(file.name, style="bold dark_green")
    except FileNotFoundError as error:
        rich_print(f"[orange1]Profile folder could not be displayed, because the folder could not be found with error: {error}")

    rich_print(tree)

def yes_or_no() -> bool:
    from rich import print as rich_print
    import typer

    while True:
        decision_input: str = typer.prompt("y/n").lower()[0]
        match decision_input:
            case "y":
                return True
            case "n":
                return False
            case _:
                rich_print("[red]Invalid input, try again[/red]")
                continue


if __name__ == "__main__":
    pass