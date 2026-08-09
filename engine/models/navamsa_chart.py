from dataclasses import dataclass
from engine.models.navamsa_planet import NavamsaPlanet

@dataclass(frozen=True)
class NavamsaChart:
    ascendant: float
    ascendant_sign: int
    planets: dict[str, NavamsaPlanet]

    @property
    def ascendant_sign_one_based(self) -> int:
        """
        The 1-based number of :attr:`ascendant_sign`.

        :attr:`ascendant_sign` is 0-based and CERTIFIED; this accessor is
        additive (ADR-0012, Decision SC-B) and changes no
        stored value.
        """

        return self.ascendant_sign + 1

    @property
    def ascendant_sign_object(self):
        """:attr:`ascendant_sign` as an explicit Sign (ADR-0012)."""

        # Deferred import: engine.astrology's package import registers
        # production vargas, which import this module; a module-level
        # import here would create a cycle.
        from engine.astrology.sign import Sign

        return Sign.from_zero_based(self.ascendant_sign)
