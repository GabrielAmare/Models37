from ..constants import MODEL_RESERVED_ATTRIBUTES, NATIVE_TYPES_STRING
from ..errors import ForeignKeyConfigError
from ..ModelHandler import ModelHandler
from .RPY import RPY


class ForeignKey:
    name: str
    type: str
    optional: bool
    multiple: bool

    @classmethod
    def rpy(cls, rpy: str, **config):
        """
            Create a field from a rpy string (and additional config)
        :param rpy: the rpy string
        :param config: dict containing the other parameters
        :return: Field
        """
        return cls(**RPY.rpy_to_cfg(rpy), **config)

    def __init__(self, name, type_, optional: bool = False, multiple: bool = False, key: str = ""):
        def foreign_key_config_error(reason, solve=""):
            return ForeignKeyConfigError(model='*', field=name, reason=reason, solve=solve)

        if name in MODEL_RESERVED_ATTRIBUTES:
            raise foreign_key_config_error(
                reason='name=' + repr(name) + ' is not allowed (reserved attribute for Model class)',
                solve='use names that are not in (' + ', '.join(map(repr, MODEL_RESERVED_ATTRIBUTES)) + ')'
            )

        if not key:
            raise foreign_key_config_error(reason='key must be defined')

        if type_ in NATIVE_TYPES_STRING:
            raise foreign_key_config_error(
                reason='type=' + repr(
                    type_) + ' is not allowed (native type needs can\'t be set as a foreign key type)',
                solve='use a model name as type, so it will link to this model instances'
            )

        self.name = name
        self.type = type_
        self.optional = optional
        self.multiple = multiple

        self.key = key

    def __call__(self, model):
        model.h.attributes.add(self)
        return model

    def getter(self, target):
        model = ModelHandler.models.get(self.type)

        q = model.h.instances.where(**{self.key: target})

        if self.multiple:
            return q
        else:
            return q.first
