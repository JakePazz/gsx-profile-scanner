# External imports
import os
import typer
from rich import print as prnt
from rich.panel import Panel
from rich.table import Table
from json import dump

# Internal imports
from utils import log

def setup():
    scan_config: dict = {} # The config that will be written to the scan_config json file once setup is complete

    prnt("[bold blue]GSX Pro Profile Scanner setup[/bold blue]\nThis will setup all configs so that you should [italic]never[/italic] have to touch them again (maybe).")
    prnt("Enter [bold green]'continue'[/bold green] or type [bold red]'cancel'[/bold red] to stop setup.")
    while True:
        input: str = typer.prompt("Action")
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
        
    

    # if system username not found, get user to manually enter it
    username: str
    try:
        username = os.getlogin() 
    except Exception as error:
        log("warn", f"Could not successfully automatically retrieve user's username from system with error: {error}")
        prnt("[bold red]Error![/bold red] Your system username could not be retrieved automatically. Enter it yourself below.")
        username = typer.prompt("Enter username")
        
    profiles_folder_path = f"C:/Users/{username}/AppData/Roaming/virtuali/GSX/MSFS"

    # Check within expected profiles folder path for either a .ini or .py file to verify that this is (likely) the profiles folder
    valid_filetype_found: bool = False
    with os.scandir(profiles_folder_path) as profiles_folder:
        for file in profiles_folder:
            if file.is_file():
                if file.name.endswith(".ini") or file.name.endswith(".py"):
                    log("info",f"Valid filetype found within the specified path of ({profiles_folder_path})")
                    valid_filetype_found = True
                    break
    if not valid_filetype_found:
        prnt("[bold dark_orange]Could not find a valid .ini or .py file within the expected profiles folder[/bold dark_orange]")
        prnt(f"Confirm the following path '{profiles_folder_path}' is correct")
        prnt("[italic]Note: This error will occur if your profiles folder is empty yet valid; if this is the case respond with 'y'[/italic]")
        while True:
            decision_input: str = typer.prompt("y/n").lower()[0]
            match decision_input:
                case "y":
                    break
                case "n":
                    profiles_folder_path = manual_path_entry()
                    break
                case _:
                    prnt("[bold dark_orange]Invalid input, try again[/bold orange]")
                    continue
        log("Profile path found")
    
    scan_config = {
            "profile_folder_path": profiles_folder_path
    }
    log("info",f"Scan config created with profile folder path: {profiles_folder_path}")
    
    # Get user to decide on what data they want to be shown when using 'scan' command
    prnt("When using the 'scan' command you will be shown a list of all found airports corresponding to your profiles. You must now choose what information you wish to be displayed for each airport.")
    prnt("Select what information you would like to be displayed for each airport")
    
    options_table = Table("Name","Description", "Included Information", style="bold dodger_blue2")
    options_table.add_row("Recommended", "The recommended, necessary and useful, information", "ident (ICAO), IATA, name, type (small, large, heli), continent")
    options_table.add_row("All", "All available information (not recommended).", "ident, type, name, latitude, longitude, elevation, continent, iso country, iso region, municipality, scheduled_service, gps_code, iata_code, keywords")
    options_table.add_row("Custom", "Choose what information you want displayed.", "N/A")

    prnt(options_table)
    prnt("Enter [bold green]'recommended'[/bold green], [bold green]'all'[/bold green] or [bold green]'custom'[/bold green]")
    while True:
        display_data_choice_input: str = typer.prompt("Choice")
        input = input.lower()
        if input not in ["recommended", "all", "custom"]:
            log("info", "Invalid input (did not match required 'recommended', 'all' or 'custom')")
            prnt("[red]Invalid input. Please try again.[/red]")
            continue
        else:
            log("info",f"User selected {display_data_choice_input} as the display data choice")
            break
    
    match display_data_choice_input:
        case "recommended":
            scan_config["scan_display_data"] = ["ident","iata","name","type","continent"]
        case "all":
            scan_config["scan_display_data"] = ["ident","type","name","latitude","longitude","elevation_ft","continent","iso_country","iso_region","municipality","scheduled_service","gps_code","iata_code","keywords"]
        case "custom":
            display_data_values_table = Table("No.","Name","Description", "Example")
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
            prnt(display_data_values_table)
            prnt("Enter the numbers of the data values you would like to be displayed separated by commas in the order you wish them to be displayed (e.g. '1,3,5')")
            display_data_choices: int = typer.prompt().split(",")
            scan_config["scan_display_data"] = []

            options_list = ["ident", "type", "name", "latitude_deg", "longitude_deg", "elevation_ft", "continent", "iso_country", "iso_region", "municipality", "scheduled_service", "gps_code", "iata_code", "keywords"]
            for choice in display_data_choices:
                scan_config["scan_display_data"].append(display_data_values_table[choice])
            log("info",f"User selected {display_data_choices} as the display data values")

    # Write the scan config to json file
    try:
        with open("./configs/scan_config.json","w") as scan_config_file:
            scan_config_file.write(dump(scan_config))
        log("info","Scan config created successfully")
    except Exception as error:
        log("error", f"Error writing scan config to file with error: {error}")
        prnt("[bold red]Error![/bold red] An error occurred writing the scan config to file. Setup failed.")
        raise typer.Exit()
    
    try:
        with open("./configs/program_config.json","w") as program_config_file:
            program_config_file.write(dump({"successfull_configuration":"true"}))
    except Exception as error:
        log("error", f"Error writing to program config file with error: {error}")
        prnt("[bold red]Error![/bold red] An error occurred writing to the program config to file. Setup failed.")
        raise typer.Exit()
    


def manual_path_entry():
    # Allow user to manually enter the path of their GSX Profile folder
    prnt("The system is unable to identify your GSX Pro Profile Path. Please enter it manually below")
    while True:
        path_input = typer.prompt("Profile Folder Path")
        if os.path.isdir(path_input):
            log("info", "User successfully manually entered the path for GSX Profile folder")
            prnt("[green]Path accepted[/green]")
            return path_input
        else:
            log("info","User provided an invalid path (system could not find it)")
            prnt("[red bold]Invalid directory path, try again[/red bold]")
            continue

setup()