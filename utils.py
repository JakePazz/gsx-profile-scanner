# Upon an exception, functions here will only Exit() if crucial to program function
# Note: Some functions are not necessarily common utils but placed here to avoid circular imports

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

def display_data(scan_config):
    # Returns updated scan_config file
    from rich import print as rich_print
    from rich.table import Table
    from rich import box
    from typer import prompt
    from typing import List

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
        display_data_choice_input: str = prompt("Action").lower()
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
            options_list: List[str] = ["ident", "type", "name", "latitude_deg", "longitude_deg", "elevation_ft", "continent", "iso_country", "iso_region", "municipality", "scheduled_service", "gps_code", "iata_code", "keywords"]

            while True:
                display_data_choices: int = prompt("Selection").split(",").strip()
                if all(ele in options_list for ele in display_data_choices):
                    log("info", "Display data choices valid")
                    break
                else:
                    print("Invalid entry, try again.")
                    log("warn", "User entered invalid options ")
                    continue

            scan_config["scan_display_data"] = []
            
            for choice in display_data_choices:
                print(f"Choice: {choice.strip()}")
                scan_config["scan_display_data"].append(options_list[int(choice)-1])
            log("info",f"User selected {display_data_choices} as the display data values")
    return scan_config

if __name__ == "__main__":
    pass