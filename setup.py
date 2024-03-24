# External imports
import os
import typer
from rich import print as prnt
from rich.panel import Panel

# Internal imports
from global_utils import log

def setup():
    prnt("[bold blue]GSX Pro Profile Scanner setup[/bold blue]\nThis will setup all configs so that you should [italic]never[/italic] have to touch them again (maybe).")
    prnt("Enter [bold green]'continue'[/bold green] to continue or type [bold red]'cancel'[/bold red] to stop setup.")
    while True:
        input = typer.prompt("Action")
        input = input.lower()
        if input not in ["continue", "cancel"]:
            log("info", "Invalid input (did not match required 'continue' or 'cancel')")
            prnt("[red]Invalid input. Please try again.[/red]")
            continue
        else:
            break
    
    if input == "cancel":
        log("info", "User cancelled setup")
        prnt("Setup cancelled.")
        raise typer.Exit()


    if not os.path.exists("./configs"):
        log("warn","'configs' folder does not exist but is now being created")
        os.mkdir("./configs")
    
    # if found, verify that legit (can check for a suitable file-type within it)
    # if not found, tell user and get them to verify location that program is trying to find it as is correct
    try:
        username = os.getlogin()
        PROFILES_FOLDER_PATH = f"C:/Users/{username}/AppData/Roaming/virtuali/GSX/MSFS"
    except Exception as error:
        log("warn", f"Could not successfully retrieve user's username from system with error: {error}")
        print("Cannot get username")
        #TODO: Give option to manually enter username
        

    # Check within expected profiles folder path for either a .ini or .py file to verify that there is available (possible) profile files
    folder_valid = False
    with os.scandir(PROFILES_FOLDER_PATH) as profiles_folder:
        for file in profiles_folder:
            if file.is_file():
                if file.name.endswith(".ini") or file.name.endsw(".py"):
                    folder_valid = True
                    break
    if not folder_valid:
        print("fail")
        # TODO: Tell user could not be found
        # TODO: Add in manual entry of username
    else:
        print("successful")
    
    # TODO: Ask user to enter what attr they want displayed for each airport (values of "scan_display_data" in scan_config); give option to select all, recommended or custom


    



setup()