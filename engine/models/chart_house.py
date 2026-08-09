from dataclasses import dataclass


@dataclass(frozen=True)
class ChartHouse:
    number: int
    cusp: float
    sign: int
    degree: float

    @property
    def sign_zero_based(self) -> int:
        """
        The 0-based index of :attr:`sign`.

        :attr:`sign` is 1-based and CERTIFIED; this accessor is
        additive (ADR-CONVENTION-001, Decision SC-B) and changes no
        stored value.
        """

        return self.sign - 1

    @property
    def sign_object(self):
        """:attr:`sign` as an explicit Sign (ADR-CONVENTION-001)."""

        from engine.astrology.sign import Sign

        return Sign.from_one_based(self.sign)