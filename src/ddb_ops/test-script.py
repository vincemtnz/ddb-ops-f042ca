from datetime import datetime
from typing import Annotated
from collections.abc import Iterable
from random import choice

import typer
from rich import print

from ddb_ops.config.logger import setup_logger
from ddb_ops.models.phone_number_capability import PhoneNumberCapability
from ddb_ops.types import CapabilityCode

app = typer.Typer()

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")

def validate_date(value: str):
    try:
        validated_date = datetime.strptime(value, "%Y-%m-%d")
        return validated_date.strftime("%Y-%m-%d")
    except ValueError:
        raise typer.BadParameter("Date must be in YYYY-MM-DD format")


def create_seed_records(
    start_from: int = 0,
    total: int = 0,
    prefix: str = "XXA",
    date: str = CURRENT_DATE,
) -> Iterable[PhoneNumberCapability]:
    for i in range(start_from, start_from + total):
        phone_number = f"{prefix.upper()}{str(i).zfill(10 - len(prefix))}"
        yield PhoneNumberCapability(
            phone_number=str(phone_number),
            channel="RCS",
            capability_status=choice(
                [CapabilityCode.ENABLED, CapabilityCode.UNREACHABLE]
            ),
            last_refreshed_at=date

        )

def run_seed(total: int, date: str, prefix: str, execute: bool):
    records = list(create_seed_records(total=total, date=date, prefix=prefix))
    print(f"Generated {len(records)} fake records.")
    print(
        f"First phone number: {records[0].get('phone_number')}.\nLast phone number: {records[-1].get('phone_number')}"
    )

    with PhoneNumberCapability.batch_write(auto_commit=True) as batch:
        for record in records:
            if execute:
                batch.save(record)
            else:
                print("Dry run. No records saved.")


@app.command()
def seed(
    total: Annotated[
        int, typer.Option("--total", help="Number of records to generate")
    ],
    date: Annotated[
        str,
        typer.Option(
            "--date",
            callback=validate_date,
            help="Date in YYYY-MM-DD format. Defaults to the current date.",
        ),
    ] = CURRENT_DATE,
    prefix: Annotated[
        str,
        typer.Option("--prefix", help="Prefix for the generated numbers (e.g. XXA)"),
    ] = "XXA",
    execute: Annotated[
        bool, typer.Option("--execute", help="Write the values to DynamoDB")
    ] = False,
):
    run_seed(total=total, date=date, prefix=prefix, execute=execute)


if __name__ == "__main__":
    setup_logger()
    app()
