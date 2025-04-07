from rich import print
from ..models.phone_number_capability import PhoneNumberCapability

def delete_numbers(
    prefix: str,
    execute: bool = False
):
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
