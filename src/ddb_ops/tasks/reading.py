from rich import print
from ..models.phone_number_capability import PhoneNumberCapability

def generate_pks(prefix: str, total: int):
    for i in range(total):
        yield f"{prefix.upper()}{str(i).zfill(10 - len(prefix))}"


def run_batch_get(
    prefix: str = "XXA",
    total: int = 10,
    execute: bool = False
):
    item_keys = [(pk, "RCS") for pk in generate_pks(prefix, total)]
    item_keys.extend([(pk, "RCS") for pk in generate_pks("YYA", total)])

    if execute:
        for item in PhoneNumberCapability.batch_get(item_keys):
            print(item)
    else:
        print(item_keys)
        print("Dry run.")


def run_query(
    prefix: str = "XXA",
    total: int = 10,
    execute: bool = False
):
    print(f"Reading {total} records.")
    if execute:
        for pk in generate_pks(prefix, total):
            for item in PhoneNumberCapability.query(pk, PhoneNumberCapability.channel == "RCS"):
                print(item.phone_number, item.channel, item.is_capable)
    else:
        print("Dry run.")
