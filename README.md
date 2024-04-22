# GSX Profile Scanner

This is a small CLI (command line interface) app intended to help users of [GSX Pro](https://www.fsdreamteam.com/products_gsxpro.html) for MSFS 2020, providing features to make life easier when trying to see what profiles you have.

## Features Explained
As you will see when you load the app, there is some basic instructions and a table containing all available commands. Below is the same table for reference.

| Command          | Trigger  | Description                                                    |
| ---------------- | -------- | -------------------------------------------------------------- |
| Scan Folder      | scan     | Scan the specified profiles folder for GSX Profiles            |
| Search Airport   | search   | Search for a specific airport in the specified profiles folder |
| Open Folder      | open     | Open the GSX Pro Profiles folder in file explorer              |
| Settings         | settings | View and edit the settings for this program                    |
| Data File Upload | upload   | Upload a new data file to the program                          |
| Help             | help     | View the help menu                                             |
| Exit             | exit     | Exit the program                                               |

## Installation

1. Download the latest release from this page (on the right side of your screen)
2. And more that I need to add once I am certain on the process...

# Potential Improvements

Below are some features/changes I am considering adding at some point (maybe never)

#### Refactoring

Not a new feature, but there is certainly areas of improvement in the app that I can leverage to improve performance/speed (eg: improve search function to not rely on folder_scan())

#### Mass profile install
Allows the user to specify a target folder, that will have all files/folders (.zip, .rar, .ini, .py etc.) and automatically find the valid profile files and copy them to the specified profiles folder

#### Scan Filtering
Allow the user to only see data that meets a criteria specified before the scan is started (region, airport size etc.); may require more data from [ourairports.com](https://ourairports.com/)

## Packages in use

- Pandas
- Rich
- Typer
- Typing
- pyclip
- shutil
- requests
- json
- datetime
- webbrowser
- os
