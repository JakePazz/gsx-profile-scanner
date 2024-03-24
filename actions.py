def scan():
    # Scan the specified profiles folder for GSX profiles using search() and display the results to the user

    
    pass

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