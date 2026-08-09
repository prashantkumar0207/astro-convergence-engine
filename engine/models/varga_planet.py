from dataclasses import dataclass


@dataclass(frozen=True)
class VargaPosition:
    """
    Authoritative varga placement of a point (Phase A generic model).

    The classification (sign, division_number, fraction) is the
    canonical output; no expanded D-space longitude is carried,
    because longitude projection is a per-varga convention owned by
    certified modules (ADR refinement).

    Attributes
    ----------
    source_longitude
        The sidereal D1 longitude that was classified, in degrees.
    sign
        0-based sign in the divisional chart (matching the certified
        D9/D10 convention).
    division_number
        1-based division within the source sign (generic name for
        what D9 calls navamsa_number and D10 calls segment).
    fraction
        Position within the division, in [0, 1).
    """

    source_longitude: float
    sign: int
    division_number: int
    fraction: float

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


@dataclass(frozen=True)
class VargaPlanet:
    """A named planet's varga placement."""

    name: str
    source_longitude: float
    sign: int
    division_number: int
    fraction: float

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
