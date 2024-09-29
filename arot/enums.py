from enum import Enum


class Label(Enum):
    هایفو = 1
    ژل = 2
    لاغری = 3
    ناخن = 4
    مزو = 5

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace('_', ' ')) for key in cls]
