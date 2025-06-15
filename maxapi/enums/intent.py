from enum import Enum

class Intent(str, Enum):
    DEFAULT = 'default'
    POSITIVE = 'positive'
    NEGATIVE = 'negative'