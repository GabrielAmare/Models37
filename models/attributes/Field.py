from ..constants import MODEL_RESERVED_ATTRIBUTES, NATIVE_TYPES_STRING, NATIVE_TYPES, CREATE, UPDATE, ACCESS
from ..errors import PrimaryKeyError, FieldCheckError, FieldConfigError, FieldFindError
from .DataList import DataList
from .RPY import RPY
from .Parse import Parse


class Field:
    name: str
    type: str
    optional: bool
    multiple: bool

    unique: bool
    private: bool
    static: bool

    @classmethod
    def rpy(cls, rpy: str, **config):
        """
            Create a field from a rpy string (and additional config)
        :param rpy: the rpy string
        :param config: dict containing the other parameters
        :return: Field
        """
        return cls(**RPY.rpy_to_cfg(rpy), **config)

    def __init__(self, name, type_,
                 optional: bool = False, multiple: bool = False,
                 unique: bool = False, private: bool = False, static: bool = False,
                 default=None, values=None, show=True, pk=False
                 ):
        def field_config_error(reason, solve):
            return FieldConfigError(model='*', field=name, reason=reason, solve=solve)

        if name in MODEL_RESERVED_ATTRIBUTES:
            raise field_config_error(
                reason='name=' + repr(name) + ' is not allowed (reserved attribute for Model class)',
                solve='use names that are not in (' + ', '.join(map(repr, MODEL_RESERVED_ATTRIBUTES)) + ')'
            )

        if pk and not unique:
            raise field_config_error(
                reason='pk=True is not allowed when static=False',
                solve='Set static=True or pk=False when creating the field'
            )

        if static and multiple:
            raise field_config_error(
                reason='static=True is not allowed when multiple=True',
                solve='Set static=False or multiple=False when creating the field'
            )

        if default is not None and not hasattr(default, '__call__') and not default.__class__ in NATIVE_TYPES:
            raise field_config_error(
                reason='default: ' + default.__class__.__name__ + ' is not allowed',
                solve='Use a default value which type is in (' + ', '.join(NATIVE_TYPES_STRING) + ')'
            )

        self.name = name
        self.type = type_
        self.optional = optional
        self.multiple = multiple

        self.static = static
        self.private = private
        self.unique = unique

        self.default = default
        self.values = values

        self.show = show
        self.pk = pk

    def __call__(self, model):
        model.h.attributes.add(self)
        return model

    def data_type(self, model):
        if self.type in NATIVE_TYPES_STRING:
            return eval(self.type)
        else:
            return model.h.models.get(self.type)

    def check(self, action, model, target, data):
        def field_check_error(reason, solve=""):
            return FieldCheckError(
                model=model.__name__,
                field=self.name,
                reason=reason,
                solve=solve
            )

        data_type = self.data_type(model)

        if action == CREATE:
            if self.name in data:
                value = data[self.name]
            else:
                raise field_check_error(
                    reason='missing key in data',
                    solve='add ' + self.name + ' = ... in data'
                )
        elif action == UPDATE:
            if self.name in data:
                value = data[self.name]
            else:
                return
        else:
            raise Exception('Invalid action !')

        if self.multiple:
            if not isinstance(value, list):
                raise field_check_error(
                    reason='<field> must be a list !'
                )

            if not (self.optional or len(value)):
                raise field_check_error(
                    reason='<field> must have at least one element !'
                )

            if not all(isinstance(item, data_type) for item in value):
                raise field_check_error(
                    reason='<field> items must all be typed as ' + self.type
                )
        else:
            if not (self.optional or value is not None):
                raise field_check_error(
                    reason='<field> value must not be None !'
                )

            if not (value is None or isinstance(value, data_type)):
                raise field_check_error(
                    reason='<field>: ' + value.__class__.__name__ + ' is an invalid type',
                    solve='set <field>: ' + self.type
                )

        if self.unique:
            if value in model.h.instances.filter(lambda i: i is target).getattr(self.name):
                raise field_check_error(
                    reason='<field> = ' + repr(value) + ' already exists in the column',
                    solve='use a value which is not already used for <field>'
                )

        if self.values:
            if value not in self.values:
                raise field_check_error(
                    reason='<field> = ' + repr(value) + ' is not in the list of accepted values',
                    solve='set <field> to one of those ' + repr(self.values)
                )

    def parse(self, action, model, target, data):
        data_type = self.data_type(model)

        if action == CREATE:
            value = data.get(self.name)
        elif action == UPDATE:
            if self.name in data:
                value = data[self.name]
            else:
                return
        elif action == ACCESS:
            assert isinstance(target, model)

            value = getattr(target, self.name)

            if not self.private:
                data[self.name] = value

            return
        else:
            raise Exception(f"Invalid action !")

        if value is None and self.default is not None:
            if hasattr(self.default, '__call__'):
                value = self.default(model=model, target=target)
            else:
                value = self.default

        if self.multiple:
            if value is None:
                value = []

            if not isinstance(value, (list, DataList)):
                value = [value]

            if isinstance(value, list):
                value = [Parse.to(item, data_type) for item in value]

                if target:
                    value = DataList(self, target, value)
        else:
            value = Parse.to(value, data_type)

        data[self.name] = value

    def find(self, model, item):
        if not self.pk:
            raise FieldFindError(
                model=model.__name__,
                field=self.name,
                reason="<field> is not a primary key",
                solve="Set parameter pk=True when creating <field>"
            )

        data_type = self.data_type(model)

        if isinstance(item, dict) and self.name in item:
            item = item[self.name]

        item = Parse.to(item, data_type)

        if isinstance(item, data_type):
            target = model.h.instances.where(**{self.name: item}).first
            if target:
                return target

        raise PrimaryKeyError(
            model=model.__name__,
            field=self.name,
            reason='<method> with data=' + repr(item) + ' not found !'
        )

    def getter(self, target):
        return target.d[self.name]
