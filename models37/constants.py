from datetime import date, datetime

MODEL_RESERVED_ATTRIBUTES = ["models", "events"] + \
                            ["instances", "attributes", "fields", "foreign_keys", "primary_keys"] + \
                            ["d"] + \
                            ["find", "findall"] + \
                            ["on", "emit"]

NATIVE_TYPES_MAP = dict(
    bool=bool,
    int=int,
    float=float,
    str=str,
    date=date,
    datetime=datetime
)

CREATE = "create"
ACCESS = "access"
UPDATE = "update"
DELETE = "delete"
