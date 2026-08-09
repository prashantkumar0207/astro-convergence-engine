from dataclasses import dataclass
from engine.models.chart_navamsa import ChartNavamsa


@dataclass(frozen=True)
class ChartPlanet:

    name: str

    longitude: float

    sign: int

    degree: float

    house: int

    nakshatra: int

    #: Nakshatra pada (1-4). Canonical name per audit A-6;
    #: the 1-9 navamsa division is `navamsa.navamsa_number`.
    nakshatra_pada: int

    navamsa: ChartNavamsa | None = None

    latitude: float = 0.0

    speed: float = 0.0

    distance: float = 0.0

    retrograde: bool = False

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