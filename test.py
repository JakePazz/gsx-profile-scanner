import typer
from rich.panel import Panel
import rich
app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello {name}")

@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")

def main():
    rich.print("Hello, [red]World!", "Enter 'hello' or 'goodbye' to see the commands in action!")


app()
