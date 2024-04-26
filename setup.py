# External imports
import os
import typer
from rich import print as rich_print
from rich.panel import Panel
from rich.table import Table
from rich import box
from json import dumps
from typing import List

# Internal imports
from utils import log, print_line, print_folder_tree, display_data

def setup():
    # Setup the program by creating the necessary files, folders and configs

    # The configs that will be written to the json files once setup is complete
    scan_config: dict = {}
    program_config: dict = {}

    rich_print("[bold blue]GSX Pro Profile Scanner setup[/bold blue]\nThis will setup all configs for the program to function how you want it to.")
    rich_print("Enter [bold green]'continue'[/bold green] or type [bold red]'cancel'[/bold red] to stop setup.")
    while True:
        input: str = typer.prompt("Action").lower()
        if input not in ["continue", "cancel"]:
            log("info", "Invalid input (did not match required 'continue' or 'cancel')")
            rich_print("[red]Invalid input. Please try again.[/red]")
            continue
        else:
            break
    
    if input == "cancel":
        log("info", "User cancelled setup")
        rich_print("Setup cancelled.")
        raise typer.Exit()

    if not os.path.exists("./configs"):
        log("warn","'configs' folder does not exist but is now being created")
        os.mkdir("./configs")
        log("info","Configs folder created")

        
    # if system username not found, get user to manually enter it
    username: str
    try:
        username = os.getlogin() 
    except Exception as error:
        log("warn", f"Could not successfully automatically retrieve user's username from system with error: {error}")
        rich_print("[bold red]Error![/bold red] Your system username could not be retrieved automatically. Enter it yourself below.")
        username = typer.prompt("Enter username")
        
    profiles_folder_path: str = f"C:/Users/{username}/AppData/Roaming/virtuali/GSX/MSFS"

    # Check within expected profiles folder path for either a .ini or .py file to verify that this is (likely) the profiles folder
    valid_filetype_found: bool = False
    with os.scandir(profiles_folder_path) as profiles_folder:
        for file in profiles_folder:
                if file.is_file() and (file.name.endswith(".ini") or file.name.endswith(".py")):
                    log("info",f"Valid filetype found within the specified path of ({profiles_folder_path})")
                    valid_filetype_found = True
                    break
    if not valid_filetype_found:
        rich_print("[bold dark_orange]Could not find a valid .ini or .py file within the expected profiles folder[/bold dark_orange]")
        rich_print("[italic]Note: This error will occur if your profiles folder is empty yet valid; if this is the case respond with 'y'[/italic]")
        if confirm_path() == True:
            profiles_folder_path = manual_path_entry()

    scan_config: dict = {
            "profile_folder_path": profiles_folder_path
    }
    log("info",f"Scan config created with profile folder path: {profiles_folder_path}")

    scan_config = display_data(scan_config)

    # Get user to decide on what file extensions will be recognised as profiles
    print_line()
    rich_print("Enter [green]'continue'[/green] to proceed with default profile file extensions of [blue]'.ini'[/blue] and [blue]'.py'[/blue] files or [green]'custom'[/green] to select file extensions")
    while True:
        extension_decision_input: str = typer.prompt("Action").lower()
        if extension_decision_input not in ["continue", "custom"]:
            log("info", "Invalid input (did not match required 'continue' or 'update')")
            rich_print("[red]Invalid input. Please try again.[/red]")
            continue
        else:
            log("info",f"User selected {extension_decision_input} as file extensions decision")
            break
    
    match extension_decision_input:
        case "continue":
            scan_config["recognised_profile_extensions"] = [
                "ini",
                "py"
            ]
            log("info", "User chose to use default file extensions of .ini and .py")
        case "custom":
            while True:
                rich_print("Manually enter a list of file extensions you want to be recognised as profiles; [bold]separated by commas[/bold] (e.g. 'ini,py,txt')")
                rich_print("[yellow]Note: Do not include the '.' before the extension and no default extensions (ini, py) are included with a custom configuration[/yellow]")
                recognised_extensions: List[str] = typer.prompt("Extensions").split(",").strip()
                print(f"[italic green]Accepted extensions: {recognised_extensions}[/italic green]")
                
                rich_print("[yellow]Are you sure wish to continue with the specified extensions:?")
                for extension in recognised_extensions:
                    print(f"\n- {extension.lower()}")
                rich_print("Enter [green]'continue' if yes, or 'restart' to enter your choices again")
                while True:
                    continue_decision = typer.prompt("Action")
                    if continue_decision not in ["continue", "restart"]:
                        rich_print("[red]Invalid input. Please try again.[/red]")
                        log("error", "User entered incorrect decision for continuing/restarting custom file extensions")
                        continue
                    else:
                        log("info", "User accepted their file extensions custom choices")
                        break
                if continue_decision == "restart":
                    print_line()
                    continue

                print_line()
                rich_print("[bold]Custom extensions:[/bold]")
                for extension in recognised_extensions:
                    print(f"\n- {extension}")
                rich_print("Enter [green]'continue'[/green] to proceed with the specified file extensions above or [red]'restart'[/red] to reenter the custom file extensions, or [yellow]'default'[/yellow]")
                while True:
                    confirm_extensions_decision: str = typer.prompt("Action").lower()
                    if confirm_extensions_decision not in ["continue", "restart", "default"]:
                        log("info", "Invalid input (did not match required 'continue' or 'restart' or 'default')")
                        rich_print("[red]Invalid input. Please try again.[/red]")
                        continue
                    else:
                        log("info",f"User selected {confirm_extensions_decision} as file extensions decision")
                        break

                match confirm_extensions_decision:
                    case "continue":
                        program_config["recognised_profile_extensions"] = recognised_extensions
                        log("info", f"User chose have a custom set of extensions: {recognised_extensions}")
                    case "restart":
                        log("info", "User chose to restart custom file extensions process")
                        continue
                    case "default":
                        log("info", "User chose to use default file extensions of .ini and .py (after cancelling custom extensions)")
                        scan_config["recognised_profile_extensions"] = [
                            "ini",
                            "py"
                        ]

    # Check if there is a overrides.json file in the configs folder and ask user if they want to use it or replace it
    if os.path.exists("./data/overrides.json"):
        rich_print("[bold yellow]Overrides.json file found in data folder[/bold yellow]")
        rich_print("[bold]Would you like to use this file for your scan? Otherwise this file will be reset.[/bold]")
        while True:
            use_overrides_decision: str = typer.prompt("y/n").lower().strip()
            if use_overrides_decision not in ["y", "n"]:
                log("info", "Invalid input (did not match required 'y' or 'n')")
                rich_print("[red]Invalid input. Please try again.[/red]")
                continue
            else:
                log("info",f"User selected {use_overrides_decision} as decision for using overrides.json file")
                break
        if use_overrides_decision == "n":
            with open("./data/overrides.json", "w") as overrides_file:
                overrides_file.write(dumps({}))
            log("info", "User chose to use the overrides.json file for their scan")
        else:
            log("info", "User chose not to use the overrides.json file for their scan")
    else:
        log("info", "No overrides.json file found in configs folder")
        

    print_line()
    rich_print("[italic yellow]Note: Profile filename split types set to '-' and '_' as default (can be changed later in settings)[/italic yellow]")
    scan_config["recognised_profile_name_split_types"] = [
        "-",
        "_"
    ]
    

    # Write the scan and program configs to json files
    try:
        with open("./configs/scan_config.json","w") as scan_config_file:
            scan_config_file.write(dumps(scan_config))
        log("info","Scan config created successfully")
    except Exception as error:
        log("error", f"Error writing scan config to file with error: {error}")
        rich_print("[bold red]Error![/bold red] An error occurred writing the scan config to file. Setup failed.")
        raise typer.Exit()
    
    program_config["successful_configuration"] = True

    try:
        with open("./configs/program_config.json","w") as program_config_file:
            program_config_file.write(dumps(program_config))
        log("info","Successfully wrote to program_config file")
    except Exception as error:
        log("error", f"Error writing to program config file with error: {error}")
        rich_print("[bold red]Error![/bold red] An error occurred writing to the program config to file. Setup failed.")
        raise typer.Exit()
    
    rich_print("[green bold]Setup compelete![/green bold]")
    
def manual_path_entry() -> str:
    # Allow user to manually enter the path of their GSX Profile folder
    print_line()
    rich_print("The system is unable to identify your GSX Pro Profile Path. Please enter it manually below")
    while True:
        path_input = prompt("Profile Folder Path")
        if isdir(path_input):
            log("info", "User successfully manually entered the path for GSX Profile folder")
            rich_print("[green]Path accepted[/green]")
            return path_input
        else:
            log("info","User provided an invalid path (system could not find it)")
            rich_print("[red bold]Invalid directory path, try again[/red bold]")
            continue

def confirm_path(profiles_folder_path: str):
    print_folder_tree(folder_path=profiles_folder_path)

    rich_print(f"Confirm the following path '{profiles_folder_path}' is correct")
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