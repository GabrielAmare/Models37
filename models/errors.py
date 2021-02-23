class FWError(Exception):
    header: str = ""

    def __init__(self, reason: str = "", solve: str = ""):
        self.reason = reason
        self.solve = solve

    def parse(self, s: str) -> str:
        return s

    def __str__(self):
        m = self.parse(self.header)

        reason = self.parse(self.reason)
        solve = self.parse(self.solve)

        if reason:
            m += "\n\t[REASON] " + reason
        if solve:
            m += "\n\t [SOLVE] " + solve
        return m


class ModelError(FWError):
    header = '<model>'

    def __init__(self, model, reason: str = "", solve: str = ""):
        super().__init__(reason, solve)
        self.model = model

    def parse(self, s: str) -> str:
        return s.replace('<model>', self.model)


class ModelFieldError(ModelError):
    header = '<field>'

    def __init__(self, model, field: str, reason="", solve=""):
        super().__init__(model, reason, solve)
        self.field = field

    def parse(self, s: str) -> str:
        return ModelError.parse(self, s.replace('<field>', '<model>.' + self.field))


class ModelFieldMethodError(ModelFieldError):
    header = '<method>'

    def __init__(self, model, field: str, method, reason="", solve=""):
        super().__init__(model, field, reason, solve)
        self.method = method

    def parse(self, s):
        return super().parse(s.replace('<method>', '<field>.' + self.method + "(...)"))


class ModelOverwriteError(ModelError):
    pass


class FieldConfigError(ModelFieldError):
    pass


class ForeignKeyConfigError(ModelFieldError):
    pass


class FieldCheckError(ModelFieldMethodError):
    def __init__(self, model: str, field: str, reason: str = "", solve: str = ""):
        super().__init__(model, field, "check", reason, solve)


class PrimaryKeyError(ModelFieldMethodError):
    def __init__(self, model: str, field: str, reason: str = "", solve: str = ""):
        super().__init__(model, field, "find", reason, solve)


class FieldAppendError(ModelFieldMethodError):
    def __init__(self, model: str, field: str, reason: str = "", solve: str = ""):
        super().__init__(model, field, "append", reason, solve)


class FieldRemoveError(ModelFieldMethodError):
    def __init__(self, model: str, field: str, reason: str = "", solve: str = ""):
        super().__init__(model, field, "remove", reason, solve)


class FieldReplaceError(ModelFieldMethodError):
    def __init__(self, model: str, field: str, reason: str = "", solve: str = ""):
        super().__init__(model, field, "replace", reason, solve)


class FieldFindError(ModelFieldMethodError):
    def __init__(self, model: str, field: str, reason: str = "", solve: str = ""):
        super().__init__(model, field, "find", reason, solve)
