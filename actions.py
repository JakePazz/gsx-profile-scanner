def scan():
    import os
    from utils import retrieve_path, retrieve_config
    from typing import List, Dict
    from json import dumps
    
    PROFILE_FOLDER_PATH: str = retrieve_path()

    profiles: List[str] = os.listdir(PROFILE_FOLDER_PATH)

    profile_files: List[Dict["filename": str, "valid": bool, "extension": str, "invalid_reason": str, "airport_index": int, "ident-found": str]] = [] # Filename, Reason, Extension

    for profile in profiles:
        extension: str = profile.split(".")[-1]
        extensions: List[str] = retrieve_config("program_config","recognised_profile_extensions")
        if extension not in extensions:
            profile_files.append({"filename": profile.split(".")[0], "valid": False,"extension": extension, "invalid_reason": "invalid_extension"})
        else:
            profile_files.append({"filename": profile.split(".")[0], "valid": True, "extension": extension})
    

    for file in profile_files:
        if file["valid"] == True:
            for split_type in retrieve_config("scan_config", "recognised_profile_name_split_types"): # TODO: Add to config
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

    for file_index, file in enumerate(profile_files):
        for comparison_index, comparison_file in enumerate(profile_files):
            if (file["valid"] == True) and (comparison_file["valid"]) == True and (file_index != comparison_index):
                if file["airport_index"] == comparison_file["airport_index"]:
                    comparison_file["valid"] = False
                    comparison_file["invalid_reason"] = "duplicate"


    with open("./data/temp_results.json", "w") as temp_file:
        temp_file.write(dumps(profile_files))


"""
DONE - check through each valid_files and split by - and if successful move on, then split by _ MAKE IT A FUNCTION
DONE - Check each section of each file and see if it is len(4) then search for it in data
DONE - If found add index to dictionary as an airport_index
DONE - Check for duplicates by comparing airport_indexs and if found store this and output to user (add valid = False attribute with reason being duplicate and then display at end)
- Output to user (inc. any invalid_files and any unidentified or duplicate files)
- Allow user to update data for a file manually (including found airport files incase it was misidentified) and then save this in a json file in ./data to be scanned before outputting any other time for any matches to then replace existing info with what is in the file


"""


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
    
    pass

def help():
    # Display some help information to the user - how to use the program, what commands are available, etc.

    pass



if __name__ == "__main__":
    scan()