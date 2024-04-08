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
    # TODO: Comment things for future me
    
    PROFILE_FOLDER_PATH: str = retrieve_path()

    profiles: List[str] = os.listdir(PROFILE_FOLDER_PATH)

    profile_files: List[Dict["filename": str, "valid": bool, "extension": str, "invalid_reason": str, "airport_index": int, "ident-found": str]] = [] # Filename, Reason, Extension

    for profile in profiles:
        extension: str = profile.split(".")[-1]
        extensions: List[str] = retrieve_config("scan_config","recognised_profile_extensions")
        if extension not in extensions:
            profile_files.append({"filename": profile.split(".")[0], "valid": False,"extension": extension, "invalid_reason": "invalid_extension"})
        else:
            profile_files.append({"filename": profile.split(".")[0], "valid": True, "extension": extension})
    

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
                # This is where a overrides.json can be added to

    for file_index, file in enumerate(profile_files):
        for comparison_index, comparison_file in enumerate(profile_files):
            if (file["valid"] == True) and (comparison_file["valid"]) == True and (file_index != comparison_index):
                if file["airport_index"] == comparison_file["airport_index"]:
                    comparison_file["valid"] = False
                    comparison_file["invalid_reason"] = "duplicate"


    with open("./data/temp_results.json", "w") as temp_file:
        temp_file.write(dumps(profile_files))

    
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
            invalid_data.append(tuple(profile["filename"], profile["extension"], profile["invalid_reason"]))

    for row in table_data:
        scan_results_table.add_row(*row)

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
    """
- Ask user which config they want to see and change
- Display available configs and current state; load from the object (get input rules based off if it is an array or not)
- Ask and get what setting user wants to change
- Apply change
- Store in configs_audit.txt
    """

    # TODO: Instead allow user to redo setup - but maybe allow them to keep some settings and stop any possible overrides

    # with open("./configs/program_config.json", "r") as program_config_file:
    #     program_config = json.load(program_config_file)
        

    # with open("./configs/scan_config.json", "r") as scan_config_file:
    #     scan_config = json.load(scan_config_file)

    # from rich import print as rich_print
    # from rich.table import Table
    # from rich import box

    # from os import listdir
    # from typing import List
    # from typer import prompt
    # import json

    # rich_print("[bold green]Settings[/bold green]")

    # rich_print("Enter one of the below [green]available configs[/green] using it's name")

    # available_configs: List[str] = listdir("./configs")
    # for index, config in enumerate(available_configs):
    #     available_configs[index] = config.split(".")[0].split("_", maxsplit=1)[0]
    #     rich_print(f"- {available_configs[index]}")
    
    # while True:
    #     settings_file_decision: str = prompt("Action").lower().strip()
    #     if settings_file_decision not in available_configs:
    #         rich_print("[red]Invalid input, try again[/red]")
    #         continue
    #     else:
    #         break


    # with open(f"./configs/{settings_file_decision}_config.json", "r") as config_file:
    #     config = json.load(config_file)
    
    # options_table = Table("Setting","Current Value", box=box.HEAVY_EDGE, expand=True, style="dodger_blue2")

    # for setting in config:
    #     options_table.add_row(str(setting), str(config[setting]))
    
    # rich_print(options_table)

    # rich_print("Enter either the [green]Setting[/green] that you would like to change or [red]'exit'[/red] to return to the menu")
    # while True:
    #     selected_setting = prompt("Setting")
    #     if selected_setting not in config and selected_setting != "exit":
    #         rich_print("[red]Invalid input, try again[/red]")
    #         continue
    #     else:
    #         break
    
    # print(config[selected_setting])

def program_settings_configure():
    pass

def scan_settings_configure():
    pass

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
    # scan()
    # help()
    settings()
    