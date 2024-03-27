# External imports
import typer
from rich import print as prnt
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
import pandas as pd
import json
from os import path

# Internal imports
import actions as actn
from setup import setup
import utils

# TODO: Add option to mass install profiles from a specified folder (future feature)
# TODO: Add caching to remember past airports, especially ones that the system cannot detect
# TODO: Add function to open GSX Folder

def main():
    boot()

    commands_table = Table("Command", "Trigger", "Description", style="bold yellow")
    commands_table.add_row("Scan Folder","scan", "Scan the specified profiles folder for GSX profiles")
    commands_table.add_row("Settings","settings", "View and edit the settings for this program")
    commands_table.add_row("Help","help", "View the help menu")
    commands_table.add_row("Exit","exit", "Exit the program")

    prnt(
        Panel(Markdown("# GSX Pro Profile Scanner"), title="Welcome", style="bold green"),
        Panel(commands_table, title="Commands", style="bold yellow", title_align="left"),
        Panel(Markdown(
"""
1. Use the 'commands' box to view all available commands
2. To run a command, type the trigger word in the input box
"""), title="Instructions", style="bold red", title_align="left")
)
    
    input = typer.prompt("Action")

    if input == "scan":
        actn.scan()
        main()
    elif input == "settings":
        main()
    elif input == "help":
        main()
    elif input == "exit":
        print("Goodbye")
        raise typer.Exit()

def boot():
    # Check if setup is required
    # TODO: Add error checking for this initial check incase the file or configs folder does not exist (likely during initial load)

    if not path.exists("./configs"):
        prnt(Panel("[bright_yellow]Invalid installation found (no configs folder), launching setup[/bright_yellow]", title="Critical Error", style="bold orange1", title_align="left"))
        setup()
    
    if not path.exists("./data"):
        prnt(Panel("[bright_yellow]Invalid installation found (no data folder), launching setup[/bright_yellow]", title="Critical Error", style="bold orange1", title_align="left"))
        setup()

    if not path.exists("./logs"):
        prnt(Panel("[bright_yellow]Invalid installation found (no logs folder), launching setup[/bright_yellow]", title="Critical Error", style="bold orange1", title_align="left"))
        setup()

    with open("./configs/program_config.json", "r") as file:
        config = json.load(file)
        if config["successfull_configuration"] != "true":
            prnt(Panel("[]"))
            setup()

typer.run(main)
