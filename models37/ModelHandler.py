from .queries import Query, KeyQuery, InheritQuery
from .events import EventManager


class ModelHandler:
    Model: type
    models: KeyQuery = KeyQuery("__name__")
    events: EventManager = EventManager()

    instances: KeyQuery
    attributes: InheritQuery
    fields: KeyQuery
    foreign_keys: KeyQuery
    primary_keys: KeyQuery

    def __init__(self, model):
        self.model = model
        ModelHandler.models.add(model)

        self.instances = KeyQuery("uid")

        attributes = Query(safe=True)

        for mro in reversed(model.__mro__):
            if mro is not model:
                if issubclass(mro, self.Model):
                    for attribute in mro.h.attributes:
                        older = attributes.where(name=attribute.name).first
                        if older:
                            attributes.replace(older, attribute)
                        else:
                            attributes.append(attribute)

        self.attributes = InheritQuery("name", attributes)

        self.fields = self.attributes.keeptype("Field").safe()
        self.foreign_keys = self.attributes.keeptype("ForeignKey").safe()
        self.primary_keys = self.fields.where(pk=True).safe()
