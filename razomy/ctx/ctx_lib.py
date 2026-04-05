import typing
from razomy.python.id import id_lib

CtxId = typing.NewType('ctx_id', str)


class IdCtx:
    ctx_id: CtxId


def create_id(prefix: str):
    return CtxId(f'{prefix} {id_lib.create_id_short()}')


class Ctx(IdCtx):
    def get[T](self, k: str) -> T:
        return getattr(self, k)

    def set(self, k: str, v):
        return setattr(self, k, v)

    def has(self, k):
        return hasattr(self, k)

    def set_if_default(self, k: str, v):
        if not self.has(k):
            self.set(k, v)

    def get_or_default(self, k: str, d):
        if self.has(k):
            return self.get(k)
        else:
            return d

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def items(self):
        return self.__dict__.items()


class Contextable[T]:
    def __init__(self, ctx: T):
        self.ctx = ctx


def create_from_dict(obj: dict):
    ctx = Ctx()
    for k, v in obj.items():
        ctx[k] = v
    return ctx
