from ..errors import FieldAppendError, FieldRemoveError, FieldReplaceError


class DataList:
    def __init__(self, field, target, values):
        self.model = target.__class__
        self.field = field
        self.target = target
        self.values = values

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        return iter(self.values)

    def __repr__(self):
        return repr(self.values)

    def __str__(self):
        return str(self.values)

    def __eq__(self, other):
        return isinstance(other, DataList) and self.values == other.values

    def append(self, item):
        if not isinstance(item, self.field.dtype):
            raise FieldAppendError(
                model=self.model.__name__,
                field=self.field.name,
                reason=f"<field> items should all be typed as {self.field.type}"
            )

        self.values.append(item)

    def remove(self, item):
        if not self.field.optional and len(self.values) == 1:
            raise FieldRemoveError(
                model=self.model.__name__,
                field=self.field.name,
                reason=f"<field> must contain at least one element (can't remove the last one)"
            )

        if item not in self.values:
            raise FieldRemoveError(
                model=self.model.__name__,
                field=self.field.name,
                reason=f"<field> doesn't contain {item} (can't remove it)"
            )

        self.values.remove(item)

    def replace(self, old, new):
        if old not in self.values:
            raise FieldReplaceError(
                model=self.model.__name__,
                field=self.field.name,
                reason=f"<field> doesn't contain {old} (can't replace it)"
            )

        index = self.values.index(old)
        self.values[index] = new
