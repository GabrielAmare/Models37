from .KeyQuery import KeyQuery
from .Query import Query


class InheritQuery(KeyQuery):
    def __init__(self, key: str, query: Query = None):
        data = query.list() if query else []
        super().__init__(key=key, data=data, safe=True)
        self.base_index = len(data)

    def add(self, new):
        old = self.get(getattr(new, self.key))
        if old is None:
            self.insert(self.base_index, new)
        else:
            self.replace(old, new)
