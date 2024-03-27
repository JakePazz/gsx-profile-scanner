def scan():
    import os
    from utils import retrieve_path
    from typing import List
    # Scan the specified profiles folder for GSX profiles using search() and display the results to the user

    # - Get list of filenames
    # - Check that each one is an appropriate file extension and remove it
    # - Get the possible ICOA codes (then IATA codes from names) - length checks
    # - Search for ICAO and IATA codes
    # - Once found, send to seperate df for results
    # - Show to user (Either default df or put into a rich table)
    PROFILE_FOLDER_PATH = retrieve_path()

    profiles: List[str] = os.listdir(PROFILE_FOLDER_PATH)

    for profile in profiles:
        extension = profile.split(".")[-1]
        print(extension)
    
    









def search(target: str) -> int | None:
    # Binary search algorithm, used to search for the target in the data (an airport code within the airports.csv file)
    import pandas as pd
    data = pd.read_csv("./project/airports.csv")
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