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
from utils import log, print_line

def setup():
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
        rich_print(f"Confirm the following path '{profiles_folder_path}' is correct")
        rich_print("[italic]Note: This error will occur if your profiles folder is empty yet valid; if this is the case respond with 'y'[/italic]")
        while True:
            decision_input: str = typer.prompt("y/n").lower()[0]
            match decision_input:
                case "y":
                    break
                case "n":
                    profiles_folder_path = manual_path_entry()
                    break
                case _:
                    rich_print("[bold dark_orange]Invalid input, try again[/bold orange]")
                    continue
        log("Profile path found")
    
    # TODO: Show user tree of the folder (rich thing) and then ask for confirmation that path is correct - if not start again
    scan_config: dict = {
            "profile_folder_path": profiles_folder_path
    }
    log("info",f"Scan config created with profile folder path: {profiles_folder_path}")
    
    # Get user to decide on what data they want to be shown when using 'scan' command
    print_line()
    rich_print("When using the 'scan' command you will be shown a list of all airports found, corresponding to your installed profiles. You must now choose what information you wish to be displayed for each airport.")

    options_table = Table("Name","Description", "Included Information", style="dodger_blue2", box=box.HEAVY_EDGE, expand=True)
    options_table.add_row("Recommended", "The recommended, necessary and useful, information", "ident (ICAO), IATA, name, type (small, large, heli), continent")
    options_table.add_row("All", "All available information (not recommended).", "ident, type, name, latitude, longitude, elevation, continent, iso country, iso region, municipality, scheduled_service, gps_code, iata_code, keywords")
    options_table.add_row("Custom", "Choose what information you want displayed.", "TBD...")

    rich_print(options_table)
    rich_print("Enter [bold green]'recommended'[/bold green], [bold green]'all'[/bold green] or [bold green]'custom'[/bold green]")
    while True:
        display_data_choice_input: str = typer.prompt("Action").lower()
        if display_data_choice_input not in ["recommended", "all", "custom"]:
            log("info", "Invalid input (did not match required 'recommended', 'all' or 'custom')")
            rich_print("[red]Invalid input. Please try again.[/red]")
            continue
        else:
            log("info",f"User selected {display_data_choice_input} as the display data choice")
            break
    
    match display_data_choice_input:
        case "recommended":
            scan_config["scan_display_data"] = ["ident","iata_code","name","type","continent"]
        case "all":
            scan_config["scan_display_data"] = ["ident","type","name","latitude","longitude","elevation_ft","continent","iso_country","iso_region","municipality","scheduled_service","gps_code","iata_code","keywords"]
        case "custom":
            display_data_values_table = Table("No.","Name","Description", "Example", style="dodger_blue1", box=box.HEAVY_EDGE, expand=True)
            display_data_values_table.add_row("1", "Ident", "ICAO code for the airport", "EGLL")
            display_data_values_table.add_row("2", "Type", "Type of airport", "Large Airport")
            display_data_values_table.add_row("3", "Name", "Name of the airport", "London Heathrow Airport")
            display_data_values_table.add_row("4", "Latitude", "The latitude of the airport (degrees)", "51.4706")
            display_data_values_table.add_row("5", "Longitude", "The longitude of the airport (degrees)", "-0.461941")
            display_data_values_table.add_row("6", "Elevation", "The elevation of the airport (feet)", "83")
            display_data_values_table.add_row("7", "Continent", "The continent the airport is located on", "EU")
            display_data_values_table.add_row("8", "ISO Country", "The ISO country code the airport is in", "GB")
            display_data_values_table.add_row("9", "ISO Region", "The ISO region code the airport is in", "GB-ENG")
            display_data_values_table.add_row("10", "Municipality", "The municipality the airport is in", "London")
            display_data_values_table.add_row("11", "Scheduled Service", "Whether the airport has scheduled service", "yes")
            display_data_values_table.add_row("12", "GPS Code", "The GPS code for the airport", "EGLL")
            display_data_values_table.add_row("13", "IATA Code", "The IATA code for the airport", "LHR")
            display_data_values_table.add_row("14", "Keywords", "Keywords for the airport (Contents may vary)", "London, Heathrow, EGLL")
            rich_print(display_data_values_table)
            rich_print("Enter the numbers of the data values you would like to be displayed [bold]separated by commas[/bold] in the order you wish them to be displayed (e.g. '1,3,5')")
            display_data_choices: int = typer.prompt("Selection").split(",")
            # TODO: Validate that each value entered has a corresponding option
            scan_config["scan_display_data"] = []
            options_list: List[str] = ["ident", "type", "name", "latitude_deg", "longitude_deg", "elevation_ft", "continent", "iso_country", "iso_region", "municipality", "scheduled_service", "gps_code", "iata_code", "keywords"]
            for choice in display_data_choices:
                print(f"Choice: {choice.strip()}")
                scan_config["scan_display_data"].append(options_list[int(choice)-1])
            log("info",f"User selected {display_data_choices} as the display data values")

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
                recognised_extensions: List[str] = typer.prompt("Extensions").split(",")
                print(f"[italic green]Accepted extensions: {recognised_extensions}[/italic green]")
                # TODO: Add any validation possible
                rich_print("[yellow]Are you sure wish to continue with the specified extensions above?")
                rich_print("Enter [green]'contin")

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
    # TODO: Test custom system with confirmation

    print_line()
    rich_print("[italic yellow]Note: Profile filename split types set to '-' and '_' as default (can be changed later in settings)[/italic yellow]")
    scan_config["recognised_profile_name_split_types"] = [
        "-",
        "_"
    ]


    # Write the scan config to json file
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
    
    
    


def manual_path_entry():
    # Allow user to manually enter the path of their GSX Profile folder
    print_line()
    rich_print("The system is unable to identify your GSX Pro Profile Path. Please enter it manually below")
    while True:
        path_input = typer.prompt("Profile Folder Path")
        if os.path.isdir(path_input):
            log("info", "User successfully manually entered the path for GSX Profile folder")
            rich_print("[green]Path accepted[/green]")
            return path_input
        else:
            log("info","User provided an invalid path (system could not find it)")
            rich_print("[red bold]Invalid directory path, try again[/red bold]")
            continue



if __name__ == "__main__":
    setup()