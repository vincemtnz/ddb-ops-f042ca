from collections.abc import Iterable
from datetime import datetime
from random import choice

import typer
from rich import print

from ddb_ops.models.phone_number_capability import PhoneNumberCapability
from ddb_ops.types import CapabilityCode

app = typer.Typer()

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")

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
