from typer import run

def main():
    # External imports
    import typer
    from rich import print as rich_print
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.table import Table
    
    # Internal imports
    import actions as actn
    import utils

    boot()

    # Display menu and accept user input for command choice and execute
    while True:
        utils.print_line()

        commands_table = Table("Command", "Trigger", "Description", style="bold yellow")
        commands_table.add_row("Scan Folder","scan", "Scan the specified profiles folder for GSX profiles")
        commands_table.add_row("Search Airport", "search", "Search for a specific airport in the specified profiles folder")
        commands_table.add_row("Open Folder", "open", "Open the GSX Pro Profiles folder in file explorer")
        commands_table.add_row("Settings","settings", "View and edit the settings for this program")
        commands_table.add_row("Data File Upload", "upload", "Upload a new data file to the program")
        commands_table.add_row("Open Program Folder", "directory", "Open the folder containing this program's files")
        commands_table.add_row("Help","help", "View the help menu")
        commands_table.add_row("Exit","exit", "Exit the program")

        rich_print(
            Panel(Markdown("# GSX Pro Profile Scanner"), title="Welcome", style="bold green"),
            Panel(commands_table, title="Commands", style="bold yellow", title_align="left"),
            Panel(Markdown(
    """
    1. Use the 'commands' box to view all available commands
    2. To run a command, type the trigger word in the input box
    3. Once presented with the 'Action Complete!' message press enter to return here and select a new action
    4. Start again or type 'exit' as shown above to quit the program
    """), title="Instructions", style="bold red", title_align="left")
    )
        
        continue_decision: str = typer.prompt("Action")
        match continue_decision:
            case "scan":
                actn.scan()
                main()
            case "search":
                actn.search()
                main()
            case "open":
                actn.open_profile_folder()
                main()
            case "settings":
                actn.settings()
                main()
            case "upload":
                actn.file_upload()
                main()
            case "directory":
                actn.open_program_directory()
                main()
            case "help":
                actn.help()
                main()
            case "exit":
                rich_print("[red]Goodbye![/red]")
                raise typer.Exit()
            case _:
                print("AAA")
                utils.action_complete_prompt(skip_confirmation=True)

def boot() -> None:
    # Check if setup is required by confirming folders and successful_configuration == True
    import json
    from os import path
    from rich import print as rich_print
    from rich.panel import Panel
    from setup import setup
    if not path.exists("./configs"):
        rich_print(Panel("[bright_yellow]Invalid installation found (no configs folder), launching setup[/bright_yellow]", title="Critical Error", style="bold orange1", title_align="left"))
        setup()
    
    if not path.exists("./data"):
        rich_print(Panel("[bright_yellow]Invalid installation found (no data folder), launching setup[/bright_yellow]", title="Critical Error", style="bold orange1", title_align="left"))
        setup()

    if not path.exists("./logs"):
        rich_print(Panel("[bright_yellow]Invalid installation found (no logs folder), launching setup[/bright_yellow]", title="Critical Error", style="bold orange1", title_align="left"))
        setup()

    if path.exists("./configs/program_config.json"):
        with open("./configs/program_config.json", "r") as file:
            config: dict = json.load(file)
            if config["successful_configuration"] != True:
                rich_print(Panel("[]"))
                setup()
    else:
        rich_print(Panel("[bright_yellow]Invalid installation found (no program_config), launching setup[/bright_yellow]", title="Critical Error", style="bold orange1", title_align="left"))
        setup()

run(main)