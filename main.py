import typer
from rich import print as prnt
from rich.panel import Panel
import pandas as pd

def main():
    """
    This docsctring will be shown when running the --help flag
    """
    
    prnt("[bold red]GSX Pro Profile Scanner[/bold red]")
    prnt("Options:","\n- headers: Show the first 4 rows of the data file", "\n- clean: Clean the data file", "\n- leave: exit the program")
    input = typer.prompt("What would you like to do?")
    if input == "headers":
        airport_data = pd.read_csv("airports.csv")
        airport_data = clean_data(airport_data)
        print(airport_data.head(4))
        main()
    elif input == "clean":
        airport_data = pd.read_csv("airports.csv")
        print("Cleaning data")
        airport_data = clean_data(airport_data)
        print("Data cleaned")
        main()
    elif input == "leave":
        print("Goodbye")
        raise typer.Exit()
       
def clean_data(data):
    return data

typer.run(main)
