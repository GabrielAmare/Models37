from datetime import date, datetime

MODEL_RESERVED_ATTRIBUTES = ["h", "d"] + ["find", "findall"]
NATIVE_TYPES_STRING = ("bool", "int", "float", "str", "date", "datetime")
NATIVE_TYPES = (bool, int, float, str, date, datetime)

CREATE = "create"
ACCESS = "access"
UPDATE = "update"
DELETE = "delete"
