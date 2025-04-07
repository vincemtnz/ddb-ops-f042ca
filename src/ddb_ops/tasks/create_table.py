from ..models.phone_number_capability import PhoneNumberCapability

def run_create_table():
    PhoneNumberCapability().create_table(
        read_capacity_units=100,
        write_capacity_units=100,
        wait=True
    )
