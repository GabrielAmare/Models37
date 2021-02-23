from .constants import MODEL_RESERVED_ATTRIBUTES, CREATE, UPDATE, DELETE
from .errors import ModelOverwriteError, PrimaryKeyError
from .queries import Query
from .ModelHandler import ModelHandler


class Model:
    h: ModelHandler
    d: dict

    def __init_subclass__(cls, **kwargs):
        if cls.__name__ == "Model":
            raise ModelOverwriteError(
                model=cls.__name__,
                reason="You can't overwrite <model> !"
            )

        cls.h = ModelHandler(cls)

    def __emit__(self, action: str, field=None, **cfg):
        model = self.__class__
        event = model.__name__ + '/' + str(self.uid) + '/' + action
        config = dict(model=model, target=self, **cfg)

        if field:
            event += '/' + field
            config["field"] = field

        self.h.events.emit(event, **config)

    def __init__(self, **data):
        """
            If the instance already exists (which we check by the existence of the attribute 'd'),
            it will be updated, else it will be created
        """
        for field in self.h.fields:
            field.parse(action=CREATE, model=self.__class__, target=self, data=data)
        for field in self.h.fields:
            field.check(action=CREATE, model=self.__class__, target=self, data=data)

        self.d = data
        self.h.instances.add(self)

        self.__emit__(CREATE, data=data)

    def __update__(self, **data):
        for field in self.h.fields:
            field.parse(action=UPDATE, model=self.__class__, target=self, data=data)
        for field in self.h.fields:
            field.check(action=UPDATE, model=self.__class__, target=self, data=data)

        self.d.update(data)

        self.__emit__(UPDATE, data=data)

    def __del__(self):
        self.__emit__(DELETE)

        self.h.instances.remove(self)

    def __repr__(self):
        return f"{self.__class__.__name__}(" + \
               ", ".join(
                   f"{key}={repr(val)}"
                   for key, val in self.d.items()
                   if self.h.fields.get(key).show
               ) + \
               ")"

    def __setattr__(self, key, val):
        if key.startswith("__") and key.endswith("__") or key in MODEL_RESERVED_ATTRIBUTES:
            return super().__setattr__(key, val)

        field = self.h.fields.get(key)
        if field:
            data = {key: val}
            field.parse(action=UPDATE, model=self.__class__, target=self, data=data)
            field.check(action=UPDATE, model=self.__class__, target=self, data=data)
            self.d[key] = data[key]

            self.__emit__(UPDATE, field, value=val)

        return super().__setattr__(key, val)

    def __getattr__(self, key):
        if key.startswith("__") and key.endswith("__") or key in MODEL_RESERVED_ATTRIBUTES:
            return super().__getattribute__(key)

        attribute = self.h.attributes.get(key)
        if attribute:
            return attribute.getter(self)

        return super().__getattribute__(key)

    @classmethod
    def __cast__(cls, item):
        if isinstance(item, cls):
            return item

        for primary_key in cls.h.primary_keys:
            try:
                return primary_key.find(cls, item)
            except PrimaryKeyError:
                continue

        return item

    @classmethod
    def find(cls, **cfg):
        for found in cls.findall(**cfg):
            return found

    @classmethod
    def findall(cls, **cfg) -> Query:
        return cls.h.instances.where(**cfg)


ModelHandler.Model = Model
Model.h = ModelHandler(Model)
