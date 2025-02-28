import typer
from rich import print
from typing import Annotated
from config.logger import setup_logger
from models.phone_number_capability import PhoneNumberCapability

app = typer.Typer()

def generate_pks(prefix: str, total: int):
    for i in range(total):
        yield f"{prefix.upper()}{str(i).zfill(10 - len(prefix))}"


@app.command()
def batch_get(
    prefix: Annotated[str, typer.Option("--prefix", help="Prefix for the generated numbers (e.g. XXA)")] = "XXA",
    total: Annotated[int, typer.Option("--total", help="Total number of records to read")] = 10,
    execute: Annotated[bool, typer.Option("--execute", help="Write the values to DynamoDB")] = False
):
    item_keys = [(pk, "RCS") for pk in generate_pks(prefix, total)]
    item_keys.extend([(pk, "RCS") for pk in generate_pks("YYA", total)])

    if execute:
        for item in PhoneNumberCapability.batch_get(item_keys):
            print(item)
    else:
        print(item_keys)
        print("Dry run.")


@app.command()
def query(
    prefix: Annotated[str, typer.Option("--prefix", help="Prefix for the generated numbers (e.g. XXA)")] = "XXA",
    total: Annotated[int, typer.Option("--total", help="Total number of records to read")] = 10,
    execute: Annotated[bool, typer.Option("--execute", help="Write the values to DynamoDB")] = False
):
    print(f"Reading {total} records.")
    if execute:
        for pk in generate_pks(prefix, total):
            for item in PhoneNumberCapability.query(pk, PhoneNumberCapability.channel == "RCS"):
                print(item.phone_number, item.channel, item.is_capable)
    else:
        print("Dry run.")

if __name__ == "__main__":
    setup_logger()
    app()
