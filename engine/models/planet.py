from enum import Enum


class Planet(Enum):
    SUN = "Sun"
    MOON = "Moon"
    MARS = "Mars"
    MERCURY = "Mercury"
    JUPITER = "Jupiter"
    VENUS = "Venus"
    SATURN = "Saturn"
    RAHU = "Rahu"
    KETU = "Ketu"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def ordered(cls) -> tuple["Planet", ...]:
        return (
            cls.SUN,
            cls.MOON,
            cls.MARS,
            cls.MERCURY,
            cls.JUPITER,
            cls.VENUS,
            cls.SATURN,
            cls.RAHU,
            cls.KETU,
        )