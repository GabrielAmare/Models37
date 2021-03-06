from .constants import MODEL_RESERVED_ATTRIBUTES, CREATE, UPDATE, DELETE
from .errors import ModelOverwriteError, PrimaryKeyError
from .queries import Query, KeyQuery, InheritQuery
from .events import EventManager


class Model:
    """
        The following attributes are set at different levels of use,
            - some are associated with the Model class only [A]
            - some are associated with the Model subclasses [M]
            - some are associated with the Model subclasses instances [I]

        [A] models : Contains the list of all the runtime registered Model subclasses
        [A] events : Register for the events -> callback

        [M] instances : List of all the runtime created/loaded instances
        [M] attributes : List of all the attributes associated with a given model
        [M] fields : Subset of the 'attributes' with only the instances of Field
        [M] foreign_keys : Subset of the 'attributes' with only the instances of ForeignKey

        [I] d : dict of the data about the instance

    """
    models: KeyQuery = KeyQuery("__name__")
    events: EventManager = EventManager()

    instances: KeyQuery
    attributes: InheritQuery = InheritQuery("name", Query(safe=True))
    fields: KeyQuery
    foreign_keys: KeyQuery
    primary_keys: KeyQuery

    d: dict

    def __init_subclass__(cls, **kwargs):
        if cls.__name__ == "Model":
            raise ModelOverwriteError(
                model=cls.__name__,
                reason="You can't overwrite <model> !"
            )

        Model.models.add(cls)
        cls.instances = KeyQuery("uid")

        attributes = Query(safe=True)

        for mro in reversed(cls.__mro__):
            if mro is not cls:
                if issubclass(mro, Model):
                    for attribute in mro.attributes:
                        older = attributes.where(name=attribute.name).first
                        if older:
                            attributes.replace(older, attribute)
                        else:
                            attributes.append(attribute)

        cls.attributes = InheritQuery("name", attributes)

        cls.fields = cls.attributes.keeptype("Field").safe()
        cls.foreign_keys = cls.attributes.keeptype("ForeignKey").safe()
        cls.primary_keys = cls.fields.where(pk=True).safe()

    def on(self, action: str, name=None, callback=None):
        model = self.__class__
        uid = str(self.uid)

        event = model.__name__ + '/' + uid + '/' + action

        if name:
            event += '/' + name

        Model.events.on(event, callback)

    def emit(self, action: str, field=None, **cfg):
        model = self.__class__
        try:
            uid = str(self.uid)
        except AttributeError:
            uid = "?"

        event = model.__name__ + '/' + uid + '/' + action
        config = dict(model=model, target=self, **cfg)

        if field:
            event += '/' + field.name
            config["field"] = field

        Model.events.emit(event, **config)

    def __init__(self, **data):
        """
            If the instance already exists (which we check by the existence of the attribute 'd'),
            it will be updated, else it will be created
        """
        for field in self.fields:
            field.parse(action=CREATE, model=self.__class__, target=self, data=data)
        for field in self.fields:
            field.check(action=CREATE, model=self.__class__, target=self, data=data)

        self.d = data
        self.instances.add(self)
        self.emit(CREATE, data=data)

    def __update__(self, **data):
        for field in self.fields:
            field.parse(action=UPDATE, model=self.__class__, target=self, data=data)
        for field in self.fields:
            field.check(action=UPDATE, model=self.__class__, target=self, data=data)

        self.d.update(data)

        self.emit(UPDATE, data=data)

    def __del__(self):
        self.emit(DELETE)
        try:
            self.instances.remove(self)
        except ValueError as e:
            pass

    def __repr__(self):
        return f"{self.__class__.__name__}(" + \
               ", ".join(
                   f"{key}={repr(val)}"
                   for key, val in self.d.items()
                   if self.fields.get(key).show
               ) + \
               ")"

    def __setattr__(self, key, val):
        if key.startswith("__") and key.endswith("__") or key in MODEL_RESERVED_ATTRIBUTES:
            return super().__setattr__(key, val)

        field = self.fields.get(key)
        if field:
            data = {key: val}
            field.parse(action=UPDATE, model=self.__class__, target=self, data=data)
            field.check(action=UPDATE, model=self.__class__, target=self, data=data)
            self.d[key] = data[key]

            self.emit(UPDATE, field, value=val)

        return super().__setattr__(key, val)

    def __getattr__(self, key):
        if key.startswith("__") and key.endswith("__") or key in MODEL_RESERVED_ATTRIBUTES:
            return super().__getattribute__(key)

        attribute = self.attributes.get(key)
        if attribute:
            return attribute.getter(self)

        return super().__getattribute__(key)

    @classmethod
    def __cast__(cls, item):
        if isinstance(item, cls):
            return item

        for primary_key in cls.primary_keys:
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
        return cls.instances.where(**cfg)
