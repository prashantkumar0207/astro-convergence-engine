"""
Explicit sign value type (SIGN_CONVENTION_V1, ADR-CONVENTION-001).

The repository carries two sign-index conventions by history, both
certified and both locked: every VARGA sign output is 0-based
(including the certified D9 and D10 production modules), while every
RASHI-level sign output is 1-based (D1 chart fields, KP chains,
Parashari drishti). Neither can be renumbered without reopening
certified behavior, so this module does not renumber anything.

Instead it gives the project one explicit carrier so no sign value
crosses a layer boundary without its convention attached, which is
the prerequisite the architecture notes record for the convergence
layer.

Design constraints (Decision SC-A, approved 2026-08-09): the type is
INERT. It has named constructors, named accessors, equality, and
ordering, and deliberately NO arithmetic and NO implicit integer
conversion, because a silent off-by-one is exactly the failure this
type exists to prevent. Sign stepping stays in the layers that own
their classical rules.
"""

from dataclasses import dataclass

from engine.astrology.sign_names import SIGN_NAMES

#: Number of zodiac signs.
SIGN_COUNT = 12


class SignConventionError(ValueError):
    """Raised when a sign index is out of range for its convention."""


@dataclass(frozen=True, slots=True, order=True)
class Sign:
    """
    One zodiac sign, carrying its convention explicitly.

    Construct only through :meth:`from_zero_based` or
    :meth:`from_one_based`; read through :attr:`zero_based`,
    :attr:`one_based`, or :attr:`name`. There is intentionally no
    arithmetic and no ``__int__``.
    """

    zero_based: int

    @classmethod
    def from_zero_based(cls, index) -> "Sign":
        """Build from a 0-based index (Aries = 0 ... Pisces = 11)."""

        if isinstance(index, bool) or not isinstance(index, int):
            raise SignConventionError(
                f"zero-based sign index must be an int, got {type(index).__name__}"
            )
        if not 0 <= index <= SIGN_COUNT - 1:
            raise SignConventionError(
                f"zero-based sign index must be 0..11, got {index}"
            )
        return cls(zero_based=index)

    @classmethod
    def from_one_based(cls, number) -> "Sign":
        """Build from a 1-based number (Aries = 1 ... Pisces = 12)."""

        if isinstance(number, bool) or not isinstance(number, int):
            raise SignConventionError(
                f"one-based sign number must be an int, got {type(number).__name__}"
            )
        if not 1 <= number <= SIGN_COUNT:
            raise SignConventionError(
                f"one-based sign number must be 1..12, got {number}"
            )
        return cls(zero_based=number - 1)

    @property
    def one_based(self) -> int:
        """The 1-based sign number (Aries = 1 ... Pisces = 12)."""

        return self.zero_based + 1

    @property
    def name(self) -> str:
        """Canonical sign name from the project's single naming authority."""

        return SIGN_NAMES[self.one_based]

    def __str__(self) -> str:
        return self.name
