def scan():
    import os
    from utils import retrieve_path, retrieve_config
    from typing import List, Dict
    from json import dumps
    from rich.table import Table
    from rich import box
    from rich import print as rich_print
    import pandas as pd

    # TODO: Add progress bar
    
    PROFILE_FOLDER_PATH: str = retrieve_path()

    # Retrieve all filenames within the folder
    profiles: List[str] = os.listdir(PROFILE_FOLDER_PATH)

    # Loop through each filename and check it has a valid extension
    profile_files: List[Dict["filename": str, "valid": bool, "extension": str, "invalid_reason": str, "airport_index": int, "ident-found": str]] = []
    for profile in profiles:
        extension: str = profile.split(".")[-1]
        extensions: List[str] = retrieve_config("scan_config","recognised_profile_extensions")
        if extension not in extensions:
            profile_files.append({"filename": profile.split(".")[0], "valid": False,"extension": extension, "invalid_reason": "invalid_extension"})
        else:
            profile_files.append({"filename": profile.split(".")[0], "valid": True, "extension": extension})
    
    # Go through each valid file and find a valid airport_index (index is in airports.csv)
    for file in profile_files:
        if file["valid"] == True:
            for split_type in retrieve_config("scan_config", "recognised_profile_name_split_types"):
                filename_parts: List[str] = file["filename"].split(split_type)
                for part in filename_parts:
                    if len(part) == 4:
                        icao_search_result: int | None = search(part.upper(), "ident")
                        if icao_search_result != None:
                            file["airport_index"] = icao_search_result
                            file["ident-found"] = "icao"
                            break
                    elif len(part) == 3:
                        iata_search_result: int | None = search(part.upper(), "iata_code")
                        if iata_search_result != None:
                            file["airport_index"] = iata_search_result
                            file["ident-found"] = "iata"
                            break
                if "airport_index" in file.keys():
                    break
            if "airport_index" not in file.keys():
                file["valid"] = False
                file["invalid_reason"] = "no_code_found"
                # TODO: This is where a overrides.json can be added too

    # Check for duplicates based off airport_index values
    for file_index, file in enumerate(profile_files):
        for comparison_index, comparison_file in enumerate(profile_files):
            if (file["valid"] == True) and (comparison_file["valid"]) == True and (file_index != comparison_index):
                if file["airport_index"] == comparison_file["airport_index"]:
                    comparison_file["valid"] = False
                    comparison_file["invalid_reason"] = "duplicate"

    # Display results
    scan_results_table = Table(box=box.HEAVY_EDGE, expand=True, style="dodger_blue2")
    
    display_preference: List[str] = retrieve_config("scan_config","scan_display_data")
    for column_name in display_preference:
        scan_results_table.add_column(f"{column_name.upper()}")
    
    data = pd.read_csv("./data/airports.csv")

    table_data: List[tuple] = []
    invalid_data: List[tuple] = []

    for profile in profile_files:
        if profile["valid"] == True:
            data = pd.read_csv("./data/airports.csv")
            airport_info = data.iloc[profile["airport_index"]]
            current_airport: List = []
            for preference in display_preference:
                current_airport.append(str(airport_info[preference]))
            
            table_data.append(tuple(current_airport))
        else:
            # TODO: Add it to erroneous table w/reasons for break (cannot display info because not all may have it
            invalid_data.append((profile["filename"], profile["extension"], profile["invalid_reason"]))

    for row in table_data:
        scan_results_table.add_row(*row)

    if invalid_data != []:
        erroneous_results_table = Table("Filename", "Extension", "Invalid Reason", box=box.HEAVY_EDGE, expand=True, style="gold1")

        for row in invalid_data:
            erroneous_results_table.add_row(*row)

    # TODO: Once erroneous table created, if it exists then ask user if they want to review invalid filenames w/reasons then give option to manually enter icao or iata and then store in new data file with filename and corresponding icao and then check if file exists here if no airport can be found (Should also allow this for main data values incase it got it wrong)

    rich_print(scan_results_table)

# TODO: Allow user to update data for a file manually (including found airport files incase it was misidentified) and then save this in a json file in ./data to be scanned before outputting any other time for any matches to then replace existing info with what is in the file


def search(target: str, type: str) -> int | None:
    # Binary search algorithm, used to search for the target in the data (an airport code within the airports.csv file)
    import pandas as pd
    data = pd.read_csv("./data/airports.csv")
    data = data[type]
    low = 0
    high = len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid] == target:
            return mid
        elif data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return None


def settings():
    # Access settings from the program_config.json file and scan_config.json file

    from rich import print as rich_print
    from rich.table import Table
    from rich import box

    from datetime import datetime
    from os import listdir, path
    from typing import List, Tuple
    from typer import prompt
    import json

    from utils import display_data, log, print_line



    rich_print("[bold green]Settings[/bold green]")

    # Select what config file to view and edit
    rich_print("Enter one of the below [green]available configs[/green] using it's name")
    available_configs: List[str] = listdir("./configs")
    for index, config in enumerate(available_configs):
        available_configs[index] = config.split(".")[0].split("_", maxsplit=1)[0]
        rich_print(f"- {available_configs[index]}")
    
    while True:
        settings_file_decision: str = prompt("Action").lower().strip()
        if settings_file_decision not in available_configs:
            rich_print("[red]Invalid input, try again[/red]")
            continue
        else:
            break


    # Load config, display settings in a table w/current values and ask user to select a setting to change
    with open(f"./configs/{settings_file_decision}_config.json", "r") as config_file:
        config = json.load(config_file)
    
    options_table = Table("Setting","Current Value", box=box.HEAVY_EDGE, expand=True, style="dodger_blue2")

    for setting in config:
        options_table.add_row(str(setting), str(config[setting]))
    
    rich_print(options_table)

    rich_print("Enter either the [green]Setting[/green] that you would like to change or [red]'exit'[/red] to return to the menu")
    while True:
        selected_setting_key = prompt("Setting").lower()
        if selected_setting_key not in config and selected_setting_key != "exit":
            rich_print("[red]Invalid input, try again[/red]")
            continue
        else:
            break

    # If user not exiting, ask for new value
    # Note: Some hardcoded custom validation/alternative methods of input for certain settings
    if selected_setting_key in config:
        selected_setting_value = config[selected_setting_key]
        setting_type: Tuple[str] = setting_datatype(selected_setting_value)
        log("info",f"Setting type found to be {setting_type}")
        
        if setting_type[0] == "list":
            if selected_setting_key == "scan_display_data":
                config, prev_value, new_value = display_data(config, return_values=True)
            else:
                rich_print(f"Enter your new values for [green]'{selected_setting_value}'[/green] of datatype [green]{setting_type[0]}[/green] as a list seperated by ',' (eg: 2,3,5)\nCurrent value: {config[selected_setting_key]}")
                while True:
                    new_value = prompt("Value").split(",")
                    new_value = [value.strip() for value in new_value] # Remove any whitespace
                    if type(new_value).__name__ != setting_type[0]:
                        rich_print("[red]Invalid input, try again[/red]")
                        log("warn", "User inputted an invalid type for the new setting value")
                        continue
                    else:
                        break
        else:
            rich_print(f"Enter your new value for [green]'{selected_setting_value}'[/green] of datatype [green]{setting_type[0]}[/green]")
            while True:
                new_value = prompt("Value")
                if type(new_value).__name__ != setting_type[0]:
                    rich_print("[red]Invalid input, try again[/red]")
                    log("warn", "User inputted a invalid type for the new setting value")
                else:
                    # Validation, specifically for paths (where key ends with '_path')
                    if selected_setting_key.split("_")[-1] == "path":
                        if not path.exists(new_value):
                            rich_print("[red]Invalid value, path could not be found. Try again[/red]")
                            continue
                        else:
                            break
                    else:
                        break
    
    # Confirm change
    while True:
        print_line()
        rich_print(f"Setting: [yellow]{selected_setting_key}[/yellow]\nCurrent Value: [red]{selected_setting_value}[/red]\nNew Value: [green]{new_value}[/green]")

        print_line()
        rich_print(f"Enter [bold green]'continue'[/bold green] to complete the change shown above or [bold red]'cancel'[/bold red] to stop the change and return to the menu")
        continue_decision = prompt("Action")
        match continue_decision:
            case "cancel":
                log("info", f"User cancelled the change to {selected_setting_value} with potential new value of {new_value}")
                break
            case "continue":
                prev_value = config[selected_setting_key]
                config[selected_setting_key] = new_value
                try:
                    with open(f"./configs/{settings_file_decision}_config.json", "w") as config_file:
                        config_file.write(json.dumps(config))
                        log("info", "Successfully wrote new config to file")
                        log("info", f"Changed '{selected_setting_key}' to new value of '{new_value}' from '{prev_value}'", log_file="configs_audit")
                except Exception as error:
                    log("warn", f"Failed to write new config to file with error: {error}")
                    rich_print("[red]Failed to write new config to file, action cancelled[/red]")
                break
            case _:
                rich_print("[red]Invalid input, try again[/red]")
                continue


def setting_datatype(setting):
    # Return the datatype, list_item_datatype (if applicable) of a setting value
    datatype: str = type(setting).__name__
    list_datatype: str = None

    # If datatype is a string, return tuple with second value being the datatype of the list values
    if datatype == "list":
        list_datatype = type(setting[0]).__name__

    return datatype, list_datatype

def help():
    from utils import print_line
    from rich import print as rich_print
    from typer import prompt
    from webbrowser import open

    print_line()
    rich_print("[bold green]Help[/bold green]")
    rich_print("Help can be found on an external website.\nTo access it you can: go 'direct' to the webpage, 'copy' to clipboard, 'display' url")

    while True:
        HELP_PAGE_URL = "https://github.com/JakePazz" # TODO: Change to actual help website link
        help_decision = prompt("Action").lower().strip()

        match help_decision:
            case "direct":
                from webbrowser import open
                try:
                    open(HELP_PAGE_URL, autoraise=2)
                except Exception as error:
                    rich_print("[orange1]Cannot send you directly to the webpage. Instead view the url below[/orange1]")
                    rich_print(f"Find help at '{HELP_PAGE_URL}'")
                    input("Press enter to continue...")
                break
            case "copy":
                from pyclip import copy
                try:
                    copy(HELP_PAGE_URL)
                except Exception as error:
                    rich_print("[orange1]Cannot send you directly to the webpage. Instead view the url below[/orange1]")
                    rich_print(f"Find help at '{HELP_PAGE_URL}'")
                    input("Press enter to continue...")
                break
            case "display":
                rich_print(f"Find help at '{HELP_PAGE_URL}'")
                input("Press enter to continue...")
                break
            case _:
                rich_print("[red]Invalid input, try again[/red]")
                continue



if __name__ == "__main__":
    scan()
    # help()
    # settings()
    
    