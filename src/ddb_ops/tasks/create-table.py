import typer
from rich import print
from ..config.logger import setup_logger
from ..models.phone_number_capability import PhoneNumberCapability

def create_table():
    PhoneNumberCapability().create_table(
        read_capacity_units=100,
        write_capacity_units=100,
        wait=True
    )

app = typer.Typer()

@app.command()
def run():
    print("Creating table...")
    create_table()


if __name__ == "__main__":
    setup_logger()
    app()
