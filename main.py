import typer
from rich import print as prnt
from rich.panel import Panel
import pandas as pd

def main(name: str = "", age: int = 0, lastname: str = "", headers: bool = False):
    """
    This docsctring will be shown when running the --help flag
    """
    print(f"Hello {name}, who is {age} years old!")
    
    prnt(Panel("Hello, [red]World!"))
    if lastname:
        print(f"Also, your last name is {lastname}")
    elif name:
        print(f"Also, you have no last name, {name}")
    elif headers:
        airport_data = pd.read_csv("airports.csv")
        print(airport_data.head(4))




if __name__ == "__main__":
    typer.run(main)
