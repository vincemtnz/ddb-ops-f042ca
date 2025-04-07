import typer
from rich import print
from typing import Annotated
from ..config.logger import setup_logger
from ..models.phone_number_capability import PhoneNumberCapability

app = typer.Typer()

@app.command()
def delete_numbers(
    prefix: Annotated[str, typer.Option("--prefix", help="Prefix for the generated numbers (e.g. XXA)")],
    execute: Annotated[bool, typer.Option("--execute", help="Write the values to DynamoDB")] = False
):
    print(f"Scanning for records with prefix={prefix}")
    with PhoneNumberCapability.batch_write(auto_commit=True) as batch:
        items = PhoneNumberCapability.scan(
            filter_condition=PhoneNumberCapability.phone_number.startswith(prefix),
        )
        for item in items:
            if execute:
                print(f"Deleting item: {item.phone_number}")
                batch.delete(item)
            else:
                print(f"Would delete item: {item.phone_number}")

if __name__ == "__main__":
    setup_logger()
    app()
