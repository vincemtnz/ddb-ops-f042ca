import typer
from datetime import datetime
from random import choice
from rich import print
from typing import Annotated
from config.logger import setup_logger
from models.phone_number_capability import PhoneNumberCapability

def validate_date(value: str):
    try:
        validated_date = datetime.strptime(value, "%Y-%m-%d")
        return validated_date.strftime('%Y-%m-%d')
    except ValueError:
        raise typer.BadParameter("Date must be in YYYY-MM-DD format")


def create_seed_records(
    start_from: int = 0,
    total: int = 0,
    prefix: str = "XXA",
    date: str = datetime.now().strftime('%Y-%m-%d')
):
    records = []
    for i in range(start_from, start_from + total):
        phone_number = f"{prefix.upper()}{str(i).zfill(10 - len(prefix))}"
        record = {
            "phone_number": str(phone_number),
            "channel": "RCS",
            "is_capable": choice([True, False]),
            "last_refreshed_at": date
        }
        records.append(record)

    return records




app = typer.Typer()

@app.command()
def seed(
    total: Annotated[int, typer.Option("--total", help="Number of records to generate")],
    date: Annotated[str, typer.Option("--date", callback=validate_date, help="Date in YYYY-MM-DD format. Defaults to the current date.")] = datetime.now().strftime('%Y-%m-%d'),
    prefix: Annotated[str, typer.Option("--prefix", help="Prefix for the generated numbers (e.g. XXA)")] = "XXA",
    execute: Annotated[bool, typer.Option("--execute", help="Write the values to DynamoDB")] = False
):
    records = create_seed_records(
        total=total,
        date=date,
        prefix=prefix

    )
    print(f"Generated {len(records)} fake records.")
    print(f"First phone number: {records[0].get('phone_number')}.\nLast phone number: {records[-1].get('phone_number')}")

    with PhoneNumberCapability.batch_write(auto_commit=True) as batch:
        items = [
            PhoneNumberCapability(
                r.get("phone_number"),
                r.get("channel"),
                is_capable=r.get("is_capable"),
                last_refreshed_at=r.get("last_refreshed_at")
            )
            for r in records
        ]
        for item in items:
            if execute:
                batch.save(item)
            else:
                print("Dry run. No records saved.")


if __name__ == "__main__":
    setup_logger()
    app()
