class State:
    def __init__(self):
        self.name = None

    def __set_name__(self, owner, attr_name):
        self.name = f'{owner.__name__}:{attr_name}'

    def __str__(self):
        return self.name


class StatesGroup:
    @classmethod
    def states(cls) -> list[str]:
        return [str(getattr(cls, attr)) for attr in dir(cls)
                if isinstance(getattr(cls, attr), State)]