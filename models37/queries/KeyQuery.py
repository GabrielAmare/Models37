from .Query import Query


class KeyQuery(Query):
    def __init__(self, key: str, data=None, safe=True):
        if data is None:
            data = []
        super().__init__(data=data, safe=safe)
        self.key = key

    def get(self, val):
        return self.where(**{self.key: val}).first

    def add(self, new):
        old = self.get(getattr(new, self.key))
        if old is None:
            self.append(new)
        else:
            self.replace(old, new)

    def copy(self, safe: bool = None):
        return KeyQuery(key=self.key, data=self.data, safe=self._safe if safe is None else safe)
