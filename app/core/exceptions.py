class CoreValidationError(Exception):
    def __init__(self, field, msg) -> None:
        self.field = field
        self.msg = msg

    def to_dict(self):
        return {self.field: self.msg}
