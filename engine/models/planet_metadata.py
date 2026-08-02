from dataclasses import dataclass
from typing import Tuple

from .planet import Planet


@dataclass(frozen=True)
class PlanetMetadata:
    planet: Planet

    english_name: str
    sanskrit_name: str
    unicode_symbol: str

    category: str

    gender: str
    nature: str
    element: str
    guna: str
    caste: str
    direction: str
    weekday: str

    karakas: Tuple[str, ...]