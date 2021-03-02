from datetime import date, datetime

MODEL_RESERVED_ATTRIBUTES = ["h", "d"] + ["find", "findall"] + ["on", "emit"]

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
