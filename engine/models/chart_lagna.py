from dataclasses import dataclass


@dataclass(frozen=True)
class ChartLagna:
    longitude: float
    sign: int
    degree: float
    nakshatra: int
    #: Nakshatra pada (1-4), canonical name per audit A-6.
    nakshatra_pada: int

    @property
    def sign_zero_based(self) -> int:
        """
        The 0-based index of :attr:`sign`.

        :attr:`sign` is 1-based and CERTIFIED; this accessor is
        additive (ADR-0012, Decision SC-B) and changes no
        stored value.
        """

        return self.sign - 1

    @property
    def sign_object(self):
        """:attr:`sign` as an explicit Sign (ADR-0012)."""

        from engine.astrology.sign import Sign

        return Sign.from_one_based(self.sign)