from dataclasses import dataclass


@dataclass(frozen=True)
class NavamsaPlanet:
    """
    A planet in the D9 chart.

    navamsa_number is the 1-9 division within the source sign
    (canonical terminology per audit A-6; formerly named `pada`).
    """

    name: str
    longitude: float
    sign: int
    degree: float
    navamsa_number: int

    @property
    def sign_one_based(self) -> int:
        """
        The 1-based number of :attr:`sign`.

        :attr:`sign` is 0-based and CERTIFIED; this accessor is
        additive (ADR-0012, Decision SC-B) and changes no
        stored value.
        """

        return self.sign + 1

    @property
    def sign_object(self):
        """:attr:`sign` as an explicit Sign (ADR-0012)."""

        # Deferred import: engine.astrology's package import registers
        # production vargas, which import this module; a module-level
        # import here would create a cycle.
        from engine.astrology.sign import Sign

        return Sign.from_zero_based(self.sign)
