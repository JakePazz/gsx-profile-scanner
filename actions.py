def scan():
    from typing import List, Dict
    from rich.table import Table
    from rich import box
    from rich import print as rich_print
    from rich.progress import track
    import pandas as pd
    from typer import prompt
    import json

    from utils import retrieve_config, print_line, yes_or_no, log, action_complete_prompt
    
    print_line()
    # Loop through each filename and check it has a valid extension
    profile_files: List[Dict[
        "filename": str,
        "valid": bool,
        "extension": str,
        "invalid_reason": str,
        "airport_index": int,
        "ident-type": str
        ]] = folder_scan()

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

    for profile in track(profile_files, description="Table Creation"):
        if profile["valid"] == True:
            airport_info = data.iloc[profile["airport_index"]]
            current_airport: List = []
            for preference in display_preference:
                current_airport.append(str(airport_info[preference]))
            table_data.append(tuple(current_airport))
        else:
            invalid_data.append((profile["filename"], profile["extension"], profile["invalid_reason"]))

    for row in table_data:
        scan_results_table.add_row(*row)

    rich_print("[bold green]Scan Complete![/bold green]")

    print_line()
    rich_print(scan_results_table)
    print_line()

    # Display invalid data, and offer option to add overrides
    if invalid_data != []:
        erroneous_results_table = Table("ID", "Filename", "Extension", "Invalid Reason", box=box.HEAVY_EDGE, expand=True, style="gold1")

        for index, row in enumerate(invalid_data):
            erroneous_results_table.add_row(str(index), *row)
        

        rich_print("[orange1]Invalid data was found within the profiles folder, would you like to view this data?[/orange1]")
        if yes_or_no():
            log("info", "User chose to view invalid data")
            rich_print(erroneous_results_table)
            print_line()
            rich_print("[orange1]Would you like to manually enter the airport code for any of these profiles?[/orange1]")
            if yes_or_no():
                log("info", "User chose to manually enter airport codes for invalid data")

                print_line()
                rich_print("[cornflower_blue]Step 1)[/cornflower_blue] Enter the ID of the profile you would like to update")
                while True:
                    try:
                        id_input = str(prompt("ID"))
                        if id_input not in [str(index) for index in range(len(invalid_data))]:
                            rich_print("[red]Invalid input, try again[/red]")
                            continue
                        else:
                            break
                    except Exception as error:
                        rich_print("[red]Invalid input, try again[/red]")
                        log("warn", f"User inputted an invalid ID for the profile to update with error: {error}")
                        continue

                print_line()
                rich_print("[cornflower_blue]Step 2)[/cornflower_blue] Enter type of identifer (icao or iata)")
                while True:
                    try:
                        ident_type = str(prompt("Type")).lower().strip()
                        if ident_type not in ["icao","iata"]:
                            rich_print("[red]Invalid input, try again[/red]")
                            log("warn", f"User inputted an invalid ident type for the profile to update")
                            continue
                        else:
                            break
                    except Exception as error:
                        rich_print("[red]Invalid input, try again[/red]")
                        log("warn", f"User inputted an invalid ident type for the profile to update with error: {error}")
                        continue

                print_line()
                rich_print("[cornflower_blue]Step 3)[/cornflower_blue] Enter the airport code")
                while True:
                    try:
                        airport_code = prompt("Code").upper().strip()
                        if ((len(airport_code) == 4 and ident_type == "icao")
                            or (len(airport_code) == 3 and ident_type == "iata")):
                            if ident_type == "icao":
                                ident_type = "ident"
                            else:
                                ident_type = "iata_code"
                            if index_search(airport_code, ident_type) == None:
                                rich_print("[red]Airport code could not be found within dataset, try again[/red]")
                                rich_print("[orange1]Note: If this error is persistent, this airport code may not be present in the dataset in use[/orange1]")
                                continue
                            else:
                                break
                        else:
                            rich_print("[red]Invalid input, try again[/red]")
                            continue
                    except Exception as error:
                        rich_print("[red]Invalid input, try again[/red]")
                        continue
                

                print_line()
                rich_print("Confirm the changes by entering [green]'confirm'[/green] or [red]'cancel'[/red] to stop the changes")
                rich_print("[gold1]Note: This will automatically override any existing overrides for this filename and extension/filetype[/gold1]")
                while True:
                    try:
                        confirm_decision = prompt("Action").lower().strip()
                        if confirm_decision not in ["confirm","cancel"]:
                            rich_print("[red]Invalid input, try again[/red]")
                            continue
                        else:
                            break
                    except Exception as error:
                        rich_print("[red]Invalid input, try again[/red]")
                        log("warn", "User inputted an invalid action for the profile update")
                        continue
                if confirm_decision == "confirm":
                    log("info", f"User confirmed the changes to the profile with ID {id_input} with new ident type of {ident_type} and code of {airport_code}")
                    
                    try:
                        with open("./data/overrides.json", "r") as overrides_file:
                            overrides = json.load(overrides_file)
                    except FileNotFoundError:
                        log("warn", "No overrides.json file found, program will create a new one")
                        overrides = {"override_idents": []}

                    for override in overrides["override_idents"]:
                        if override["filename"] == invalid_data[int(id_input)][0] and override["extension"] == invalid_data[int(id_input)][1]:
                            overrides["override_idents"].remove(override)
                    
                    overrides["override_idents"].append({"filename": invalid_data[int(id_input)][0], "ident_value": airport_code, "ident_type": ident_type, "extension": invalid_data[int(id_input)][1]})

                    try:
                        with open("./data/overrides.json", "w") as overrides_file:
                            overrides_file.write(json.dumps(overrides))
                            log("info", "Successfully wrote new overrides to file")
                    except Exception as error:
                        log("warn", f"Failed to write new overrides to file with error: {error}")
                        rich_print("[red]Failed to write new overrides to file, action cancelled[/red]")            
    
    action_complete_prompt()

def folder_scan() -> object:
    from rich.progress import track
    from typing import List, Dict
    from os import listdir

    from utils import retrieve_config, retrieve_path

    # Retrieve the path to the profiles folder
    PROFILE_FOLDER_PATH: str = retrieve_path()

    # Retrieve all filenames within the folder
    profiles: List[str] = listdir(PROFILE_FOLDER_PATH)
    
    profile_files: List[Dict[
        "filename": str,
        "valid": bool,
        "extension": str,
        "invalid_reason": str,
        "airport_index": int,
        "ident-type": str
        ]] = []

    for profile in track(profiles, description="Extension Check"):
        extension: str = profile.split(".")[-1]
        extensions: List[str] = retrieve_config("scan_config","recognised_profile_extensions")
        if extension not in extensions:
            profile_files.append({"filename": profile.split(".")[0], "valid": False,"extension": extension, "invalid_reason": "invalid_extension"})
        else:
            profile_files.append({"filename": profile.split(".")[0], "valid": True, "extension": extension})
    
    # Go through each valid file and find a valid airport_index (index is in airports.csv)
    for file in track(profile_files, description="Ident Search"):
        if file["valid"] == True:
            for split_type in retrieve_config("scan_config", "recognised_profile_name_split_types"):
                filename_parts: List[str] = file["filename"].split(split_type)
                for part in filename_parts:
                    if len(part) == 4:
                        icao_search_result: int | None = index_search(part.upper(), "ident")
                        if icao_search_result != None:
                            file["airport_index"] = icao_search_result
                            file["ident-found"] = "icao"
                            break
                    elif len(part) == 3:
                        iata_search_result: int | None = index_search(part.upper(), "iata_code")
                        if iata_search_result != None:
                            file["airport_index"] = iata_search_result
                            file["ident-found"] = "iata"
                            break
                if "airport_index" in file.keys():
                    break
            if "airport_index" not in file.keys():
                override = check_overrides(file["filename"])
                if override != None:
                    if override["extension"] == file["extension"]:
                        file["airport_index"] = index_search(override["ident_value"], override["ident_type"])
                        if file["airport_index"] != None:
                            file["ident-found"] = override["ident_type"]
                            file["valid"] = True
                            file["invalid_reason"] = None
                        else:
                            file["valid"] = False
                            file["invalid_reason"] = "override_invalid"
                else:
                    file["valid"] = False
                    file["invalid_reason"] = "no_code_found"

    return profile_files

def check_overrides(filename) -> object | None:
    # Check if there are any overrides for a specific filename
    import json
    from utils import log

    try:
        with open("./data/overrides.json", "r") as overrides_file:
            overrides = json.load(overrides_file)
    except FileNotFoundError:
        log("error", "No overrides.json file found, overrides will be ignored")
    
    try:
        for override in overrides["override_idents"]:
            if override["filename"] == filename:
                return override
    except KeyError:
        log("error", "No overrides found in the overrides.json file, but a a file was found")
    
    return None

def search() -> None:
    # Search for a specific airport code within the data
    # target: str, type: str = "ident"
    from rich import print as rich_print
    from rich.progress import track
    from utils import print_line, action_complete_prompt
    from typing import List, Dict
    from pandas import read_csv
    from typer import prompt
    
    print_line()
    rich_print("[bold green]Search[/bold green]")
    
    # Get icao or iata decision
    rich_print("Would you like to search by [green]icao[/green] or [green]iata[/green] code?")#
    while True:
        search_type = prompt("Type").lower().strip()
        if search_type not in ["icao","iata"]:
            rich_print("[red]Invalid input, try again[/red]")
            continue
        else:
            if search_type == "icao":
                search_type = "ident"
            break

    print_line()

    # Get the target code
    rich_print("Enter the airport code you would like to search for")
    while True:
        search_target = prompt("Code").upper().strip()
        if (len(search_target) == 4 and search_type == "ident") or (len(search_target) == 3 and search_type == "iata"):
            break
        else:
            rich_print("[red]Invalid input, try again[/red]")
            continue
    
    print_line()
    profile_files: List[Dict[
        "filename": str,
        "valid": bool,
        "extension": str,
        "invalid_reason": str,
        "airport_index": int,
        "ident-type": str
        ]] = folder_scan()

    success: bool = False

    data = read_csv("./data/airports.csv")
    # Display the search result
    for file in track(profile_files, description="Presence Search"):
        if file["valid"] == True:
            if data.iloc[file["airport_index"]][search_type] == search_target:
                found_airport = file
    
    rich_print("[bold green]Search Complete[/bold green]")
    print_line()
    
    if found_airport is not None:
        rich_print(f"[green]Found[/green] a match for the airport code '{search_target}' in the file '{found_airport['filename']}' with extension '{found_airport['extension']}' at index '{found_airport['airport_index']}'")
    else:
        rich_print(f"[red]No[/red] match found for the airport code '{search_target}'")
    
    action_complete_prompt()

def file_upload() -> None:
    # Allow user to update data for a file manually
    from rich import print as rich_print
    from os import scandir, path
    from utils import print_line, log, print_folder_tree, action_complete_prompt
    from typing import List
    from typer import prompt
    from shutil import copyfile

    print_line()
    print_folder_tree(folder_path="./data")
    

    data_filenames: List[str] = []
    with scandir("./data") as profiles_folder:
        for file in profiles_folder:
            data_filenames.append(file.name)

    rich_print("Select a data file to replace by entering it's [green]name[/green] (inc. extension), or type [red]'exit'[/red] to return to the menu")
    while True:
        selected_filename = prompt("Action")
        if selected_filename in data_filenames or selected_filename.lower() == "exit":
            break
        else:
            rich_print("[red]Invalid input, try again[/red]")
            continue
    print_line()
    
    if selected_filename != "exit":
        rich_print("Enter the path of the new data file to replace the existing one")
        rich_print("Note: The file [bold]MUST[/bold] be in the same format and type as the existing file")
        while True:
            new_data_path = prompt("Path")
            if not path.isfile(new_data_path):
                rich_print("[red]Invalid path, try again[/red]")
                log("warn", "User inputted an invalid path for the data file upload")
                continue
            elif new_data_path.split(".")[-1] != selected_filename.split(".")[-1]:
                rich_print("[red]Invalid file type, try again[/red]")
                log("warn", "User inputted a file with an invalid file type for the data file upload")
                continue
            else:
                break
        
        rich_print("Confirm the changes by entering [green]'confirm'[/green] or [red]'cancel'[/red] to stop the changes")
        while True:
            confirm_decision = prompt("Action").lower().strip()
            if confirm_decision not in ["confirm","cancel"]:
                rich_print("[red]Invalid input, try again[/red]")
                log("warn", "User inputted an invalid action for the data file update confirmation")
                continue
            else:
                break
        
        if confirm_decision == "confirm":
            log("info", f"User confirmed the changes to the data file {selected_filename} with new file at path {new_data_path}")
            try:
                copyfile(new_data_path, f"./data/{selected_filename}")
                log("info", "Successfully copied new data file to data folder")
            except Exception as error:
                log("warn", f"Failed to copy new data file to data folder with error: {error}")
                rich_print("[red]Failed to copy new data file to data folder, action cancelled[/red]")
    
    action_complete_prompt()
    
def index_search(target: str, type: str = "ident") -> int | None:
    # Binary search algorithm, used to search for the target in the data (an airport code within the airports.csv file) with the specified type (icao or iata)
    import pandas as pd
    data = pd.read_csv("./data/airports.csv")
    
    target = target.upper().strip()

    if type == "icao":
        type = "ident"
    elif type == "iata":
        type = "iata_code"
    
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

    from utils import display_data, log, print_line, action_complete_prompt



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
    # Note: Some hardcoded custom validation/alternative methods of input for certain settings are in use
    if selected_setting_key != "exit":
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
            
    action_complete_prompt()

def setting_datatype(setting):
    # Return the datatype, list_item_datatype (if applicable) of a setting value
    datatype: str = type(setting).__name__
    list_datatype: str = None

    # If datatype is a string, return tuple with second value being the datatype of the list values
    if datatype == "list":
        list_datatype = type(setting[0]).__name__

    return datatype, list_datatype

def open_profile_folder() -> None:
    """Open the GSX Profile folder using stored path"""
    from os import startfile
    from rich import print as rich_print
    from typer import Exit
    from utils import retrieve_path, log, action_complete_prompt

    # Open GSX profiles folder in file explorer
    try:
        startfile(retrieve_path())
    except Exception as error:
        rich_print("[red]Error while trying to open GSX Profile Folder[/red]")
        log("error", f"Could not open GSX Profile folder (open_profile_folder()) with error: {error}")
        raise Exit()

    action_complete_prompt()
    
def help():
    from utils import print_line
    from rich import print as rich_print
    from typer import prompt
    from webbrowser import open
    from pyclip import copy

    print_line()
    rich_print("[bold green]Help[/bold green]")
    rich_print("Help can be found on an external website.\nTo access it you can: go 'direct' to the webpage, 'copy' to clipboard, 'display' url")

    while True:
        HELP_PAGE_URL = "https://github.com/JakePazz/gsx-profile-scanner" # TODO: Change to actual help website link
        help_decision = prompt("Action").lower().strip()

        match help_decision:
            case "direct":
                try:
                    open(HELP_PAGE_URL, autoraise=2)
                except Exception as error:
                    rich_print("[orange1]Cannot send you directly to the webpage. Instead view the url below[/orange1]")
                    rich_print(f"Find help at '{HELP_PAGE_URL}'")
                    input("Press enter to continue...")
                break
            case "copy":
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
    
    action_complete_prompt()

def open_program_directory():
    from os import startfile
    from rich import print as rich_print
    from utils import log
    from typer import Exit
    from pathlib import Path

    current_path = Path().resolve()

    try:
        startfile(current_path)
    except Exception as error:
        rich_print("[red]Error while trying to open GSX Profile Folder[/red]")
        log("error", f"Could not open GSX Profile folder (open_profile_folder()) with error: {error}")
        raise Exit()

if __name__ == "__main__":
    directory()