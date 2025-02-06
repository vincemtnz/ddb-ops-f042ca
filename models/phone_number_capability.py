from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute
from os import environ
from dotenv import load_dotenv

# Load environment variables from .env file, if present.
# We're mainly using
load_dotenv()

class PhoneNumberCapability(Model):
    class Meta: # pyright: ignore [reportIncompatibleVariableOverride]
        table_name = environ.get("TABLE_NAME")

    phone_number = UnicodeAttribute(hash_key=True)
    channel = UnicodeAttribute(range_key=True)
    is_capable = BooleanAttribute(default=True)
    last_refreshed_at = UnicodeAttribute()
