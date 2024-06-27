class ArgumentException(Exception):
    def __init__(self, _argument, *args):
        super().__init__(ArgumentException.__name__, _argument, *args)


class NotFoundException(Exception):
    def __init__(self, *args):
        super().__init__(NotFoundException.__name__, *args)


class UnknownTypeException(Exception):
    def __init__(self, _type, *args):
        super().__init__(UnknownTypeException.__name__, _type, *args)
