
class Command:
    def __init__(self, text: str, prefix: str = '/'):
        self.text = text
        self.prefix = prefix

    @property
    def command(self):
        return self.prefix + self.text