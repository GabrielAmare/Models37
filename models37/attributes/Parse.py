from datetime import date, datetime
import re


class Parse:
    """
        Class to cast the data to a desired type given a possible wrong typed value
    """
    regex_int = re.compile(r"^-?[0-9]+$")
    regex_float = re.compile(r"^-?([0-9]+\.[0-9]*|\.[0-9]+)$")
    regex_int_float = re.compile(r"^-?[0-9]+\.0*$")
    regex_date = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
    regex_datetime = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]{6})?$")

    @classmethod
    def to_bool(cls, value) -> bool:
        type_ = type(value)

        if type_ is bool:
            return value

        if type_ in (int, float):
            return bool(value)

        if type_ is str:
            if value == "True":
                return True
            if value == "False":
                return False

        raise TypeError

    @classmethod
    def to_int(cls, value) -> int:
        type_ = type(value)

        if type_ is int:
            return value

        if type_ in (bool, float):
            return int(value)

        if type_ is str:
            if cls.regex_int.match(value):
                return int(value)

            if cls.regex_int_float.match(value):
                return int(float(value))

        raise TypeError

    @classmethod
    def to_float(cls, value) -> float:
        type_ = type(value)

        if type_ is float:
            return value

        if type_ in (bool, int):
            return float(value)

        if type_ is str:
            if value == "inf":
                return float("inf")
            if value == "-inf":
                return float("-inf")
            if cls.regex_float.match(value):
                return float(value)
            if cls.regex_int.match(value):
                return float(int(value))

        raise TypeError

    @staticmethod
    def to_str(value) -> str:
        type_ = type(value)

        if type_ is str:
            return value

        if type_ in (bool, int, float):
            return str(value)

        if type_ in (date, datetime):
            return value.isoformat()

        raise TypeError

    @classmethod
    def to_date(cls, value) -> date:
        type_ = type(value)

        if type_ is date:
            return value

        if type_ is datetime:
            # WARNING : this operation leads to a data loss when (hours, minutes, seconds or milliseconds)
            return value.date()

        if type_ is str:
            if cls.regex_date.match(value):
                return date.fromisoformat(value)

            if cls.regex_datetime.match(value):
                return datetime.fromisoformat(value).date()

        raise TypeError

    @classmethod
    def to_datetime(cls, value) -> datetime:
        type_ = type(value)

        if type_ is datetime:
            return value

        if type_ is date:
            # WARNING : this operation assumes that a date datetime equivalent is the start of the day
            return datetime(value.year, value.month, value.day)

        if type_ is str:
            if cls.regex_datetime.match(value):
                return datetime.fromisoformat(value)

            if cls.regex_date.match(value):
                value_ = date.fromisoformat(value)
                return datetime(value_.year, value_.month, value_.day)

        raise TypeError

    @classmethod
    def to(cls, value, type_):
        try:
            if type_ is bool:
                return cls.to_bool(value)
            elif type_ is int:
                return cls.to_int(value)
            elif type_ is float:
                return cls.to_float(value)
            elif type_ is str:
                return cls.to_str(value)
            elif type_ is date:
                return cls.to_date(value)
            elif type_ is datetime:
                return cls.to_datetime(value)
            elif hasattr(type_, "__cast__"):
                return type_.__cast__(value)
            else:
                raise TypeError
        except TypeError:
            return value
