from .Model import Model
from .queries import *
from .attributes import *
from .constants import *
from .errors import *

from .ModelHandler import ModelHandler

Field.rpy(
    rpy="!uid[int] -u -s",
    default=lambda model, **_: model.h.instances.getattr("uid").max(default=0) + 1,
    pk=True
)(Model)


def database_to_rpy(color=False):
    if color:
        BOLD = "\033[1m"
        BLUE = "\u001b[34m"
        GREEN = "\u001b[32m"
        CLR = "\033[0m"
    else:
        BOLD = ""
        BLUE = ""
        GREEN = ""
        CLR = ""

    def model_to_rpy(model):

        def field_to_rpy(field):
            card = RPY.to_card[(field.optional, field.multiple)]

            u = f" {RPY.symbol_unique}" if field.unique else ""
            p = f" {RPY.symbol_private}" if field.private else ""
            s = f" {RPY.symbol_static}" if field.static else ""

            return card + GREEN + field.name + CLR + "[" + \
                   ("" if field.type in ("bool", "int", "float", "str", "date", "datetime") else BLUE + BOLD) + \
                   field.type + CLR + "]" + u + p + s

        return BOLD + BLUE + model.__name__ + CLR + ":\n" + "\n".join(
            "\t" + field_to_rpy(a) for a in model.h.attributes
        )

    return "\n\n".join(model_to_rpy(model) for model in ModelHandler.models) + "\n"
