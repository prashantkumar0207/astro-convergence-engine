from dataclasses import dataclass


@dataclass(frozen=True)
class ChartNavamsa:
    """
    D9 summary embedded in a D1 planet.

    navamsa_number is the 1-9 division within the sign (canonical
    terminology; audit A-6). The 1-4 nakshatra pada lives on
    ChartPlanet.nakshatra_pada, never here.
    """

    navamsa_number: int
    sign: int

    @property
    def sign_one_based(self) -> int:
        """
        The 1-based number of :attr:`sign`.

        :attr:`sign` is 0-based and CERTIFIED; this accessor is
        additive (ADR-CONVENTION-001, Decision SC-B) and changes no
        stored value.
        """

        return self.sign + 1

    @property
    def sign_object(self):
        """:attr:`sign` as an explicit Sign (ADR-CONVENTION-001)."""

        # Deferred import: engine.astrology's package import registers
        # production vargas, which import this module; a module-level
        # import here would create a cycle.
        from engine.astrology.sign import Sign

        return Sign.from_zero_based(self.sign)
