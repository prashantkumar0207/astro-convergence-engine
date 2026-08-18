"""
Panchanga Element Names (ADR-0055)

Name tables for the four panchanga elements this repository classifies
numerically in engine.astrology.panchanga: tithi, yoga, karana, vara.
Nakshatra names are unchanged and already live in nakshatra_names.py.

These are label tables only; no certification-relevant boundary
arithmetic depends on them. Sourced from the standard classical
Panchanga scheme (the same fixed sequence reproduced identically
across Hindu calendrical references, e.g. the Surya Siddhanta-derived
almanac tradition) - contrast Rahu Kalam/Yamaganda/Gulika, whose
weekday-segment assignment tables genuinely vary by tradition and are
therefore explicitly deferred, not named here (ADR-0055 item 2).
"""

#: 30 tithis. 1-15 is Shukla Paksha (waxing, ending in Purnima, the
#: full moon); 16-30 is Krishna Paksha (waning, ending in Amavasya,
#: the new moon). Names 1-14 repeat identically in both paksha.
_TITHI_BASE_NAMES = (
    "Pratipada",
    "Dwitiya",
    "Tritiya",
    "Chaturthi",
    "Panchami",
    "Shashthi",
    "Saptami",
    "Ashtami",
    "Navami",
    "Dashami",
    "Ekadashi",
    "Dwadashi",
    "Trayodashi",
    "Chaturdashi",
)

PAKSHA_SHUKLA = "Shukla"
PAKSHA_KRISHNA = "Krishna"


def tithi_paksha(number: int) -> str:
    """Which fortnight tithi `number` (1-30) falls in."""

    if not (1 <= number <= 30):
        raise ValueError(f"tithi number out of range 1-30: {number}")
    return PAKSHA_SHUKLA if number <= 15 else PAKSHA_KRISHNA


def tithi_name(number: int) -> str:
    """Name of tithi `number` (1-30), without the paksha qualifier."""

    if not (1 <= number <= 30):
        raise ValueError(f"tithi number out of range 1-30: {number}")
    if number == 15:
        return "Purnima"
    if number == 30:
        return "Amavasya"
    return _TITHI_BASE_NAMES[(number - 1) % 15]


#: 27 yogas, in classification order.
YOGA_NAMES = (
    "Vishkumbha",
    "Priti",
    "Ayushman",
    "Saubhagya",
    "Shobhana",
    "Atiganda",
    "Sukarma",
    "Dhriti",
    "Shula",
    "Ganda",
    "Vriddhi",
    "Dhruva",
    "Vyaghata",
    "Harshana",
    "Vajra",
    "Siddhi",
    "Vyatipata",
    "Variyana",
    "Parigha",
    "Shiva",
    "Siddha",
    "Sadhya",
    "Shubha",
    "Shukla",
    "Brahma",
    "Indra",
    "Vaidhriti",
)


def yoga_name(number: int) -> str:
    if not (1 <= number <= 27):
        raise ValueError(f"yoga number out of range 1-27: {number}")
    return YOGA_NAMES[number - 1]


#: Karana index 1 is the single fixed karana at the start of the lunar
#: month. Indices 2-57 cycle the seven movable karanas eight times
#: (7 x 8 = 56). Indices 58-60 are the three fixed karanas at the end.
KARANA_FIRST_FIXED = "Kimstughna"
KARANA_MOVABLE_NAMES = (
    "Bava",
    "Balava",
    "Kaulava",
    "Taitila",
    "Garija",
    "Vanija",
    "Vishti",
)
KARANA_LAST_FIXED = ("Shakuni", "Chatushpada", "Naga")


def karana_name(number: int) -> str:
    if not (1 <= number <= 60):
        raise ValueError(f"karana number out of range 1-60: {number}")
    if number == 1:
        return KARANA_FIRST_FIXED
    if number >= 58:
        return KARANA_LAST_FIXED[number - 58]
    return KARANA_MOVABLE_NAMES[(number - 2) % 7]


#: Vara (weekday) index 0 = Sunday (Ravivara) .. 6 = Saturday
#: (Shanivara). This weekday-to-name mapping is the universal
#: Panchanga convention (not a regional variant).
VARA_NAMES = (
    "Ravivara",
    "Somavara",
    "Mangalavara",
    "Budhavara",
    "Guruvara",
    "Shukravara",
    "Shanivara",
)


def vara_name(index: int) -> str:
    if not (0 <= index <= 6):
        raise ValueError(f"vara index out of range 0-6: {index}")
    return VARA_NAMES[index]
