import os
import sys
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute
from dotenv import load_dotenv

# Load environment variables from .env file, if present.
# We're mainly using
load_dotenv()

TABLE_NAME=os.environ.get("TABLE_NAME")


class PhoneNumberCapability(Model):
    class Meta: # pyright: ignore [reportIncompatibleVariableOverride]
        table_name = TABLE_NAME

    phone_number = UnicodeAttribute(hash_key=True)
    channel = UnicodeAttribute(range_key=True)
    is_capable = BooleanAttribute(default=True)
    last_refreshed_at = UnicodeAttribute()

if not TABLE_NAME:
    sys.exit("TABLE_NAME environment variable not set")
