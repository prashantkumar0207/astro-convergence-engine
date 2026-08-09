"""
SIGN_CONVENTION_V1 gates (ADR-CONVENTION-001).

Gate 2: Sign type correctness, exhaustive and adversarial.
Gate 3: declaration coverage, enforced by walking the live object
        graph of real charts. A new sign-typed field with no
        declaration FAILS here, which is the purpose of the phase.
Gate 4: cross-layer agreement between the two certified conventions.
"""

import dataclasses
import importlib
import pkgutil

import pytest

import engine.models as models_package
from engine.astrology.chart_factory import build_master_chart
from engine.astrology.dashamsa_chart import dashamsa_chart, dashamsa_sign
from engine.astrology.divisional_chart import divisional_chart
from engine.astrology.navamsa_chart import navamsa_chart, navamsa_sign
from engine.astrology.sign import SIGN_COUNT, Sign, SignConventionError
from engine.astrology.sign_names import SIGN_NAMES
from engine.astrology.sign_conventions import (
    NOT_AN_INDEX,
    ONE_BASED,
    SIGN_FIELD_CONVENTIONS,
    SIGN_FUNCTION_CONVENTIONS,
    ZERO_BASED,
    declared,
    is_index,
)
from engine.astrology.signs import zodiac_sign
from engine.astrology.varga_classifier import classify
from engine.astrology.varga_d3 import D3_PARASHARA
from engine.calculations.calculations import calculate
from engine.kp.chain import kp_chain
from engine.kp.chart import kp_chart
from engine.models.birth_data import BirthData
from engine.parashari.drishti import aspected_signs, parashari_drishti

BIRTH = BirthData(1985, 12, 21, 14, 40, 0.0, 25.6, 85.1333, "Asia/Kolkata")


# ------------------------------------------------------------ Gate 2

def test_sign_round_trips_exhaustively():
    for index in range(SIGN_COUNT):
        sign = Sign.from_zero_based(index)
        assert sign.zero_based == index
        assert sign.one_based == index + 1
        assert sign.name == SIGN_NAMES[index + 1]
        assert Sign.from_one_based(index + 1) == sign


def test_sign_rejects_out_of_range_and_wrong_types():
    for bad in (-1, SIGN_COUNT, 99, -100):
        with pytest.raises(SignConventionError):
            Sign.from_zero_based(bad)
    for bad in (0, SIGN_COUNT + 1, -1):
        with pytest.raises(SignConventionError):
            Sign.from_one_based(bad)
    for bad in ("4", 4.0, None, True, [4]):
        with pytest.raises(SignConventionError):
            Sign.from_zero_based(bad)
        with pytest.raises(SignConventionError):
            Sign.from_one_based(bad)


def test_sign_is_inert_and_immutable():
    sign = Sign.from_zero_based(3)
    # No implicit integer conversion and no arithmetic: a silent
    # off-by-one is the failure this type exists to prevent.
    for attribute in ("__int__", "__index__", "__add__", "__sub__", "__iadd__"):
        assert not hasattr(sign, attribute), attribute
    with pytest.raises(Exception):
        sign.zero_based = 5
    assert Sign.from_zero_based(0) < Sign.from_zero_based(11)
    assert len({Sign.from_one_based(1), Sign.from_zero_based(0)}) == 1


# ------------------------------------------------------------ Gate 3

def _chart_roots():
    snapshot = calculate(BIRTH).snapshot
    roots = [
        build_master_chart(snapshot),
        navamsa_chart(snapshot),
        dashamsa_chart(snapshot),
        kp_chart(BIRTH),
        parashari_drishti(BIRTH),
    ]
    roots += [divisional_chart(snapshot, division) for division in (2, 3, 7, 12, 30)]
    return roots


def _walk(roots):
    """Every dataclass instance reachable from the chart roots."""

    seen = set()
    found = []
    stack = list(roots)
    while stack:
        obj = stack.pop()
        if id(obj) in seen:
            continue
        seen.add(id(obj))
        if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
            found.append(obj)
            for field in dataclasses.fields(obj):
                stack.append(getattr(obj, field.name))
        elif isinstance(obj, dict):
            stack.extend(obj.keys())
            stack.extend(obj.values())
        elif isinstance(obj, (list, tuple, set, frozenset)):
            stack.extend(obj)
    return found


def _sign_typed_fields():
    """Discover sign-typed fields on every public model dataclass."""

    discovered = []
    for module_info in pkgutil.iter_modules(models_package.__path__):
        module = importlib.import_module(f"engine.models.{module_info.name}")
        for obj in vars(module).values():
            if not (dataclasses.is_dataclass(obj) and isinstance(obj, type)):
                continue
            if obj.__module__ != module.__name__:
                continue
            for field in dataclasses.fields(obj):
                lowered = field.name.lower()
                is_sign_named = "sign" in lowered or "rashi" in lowered
                is_sign_class_number = "sign" in obj.__name__.lower() and lowered == "number"
                if is_sign_named or is_sign_class_number:
                    discovered.append((obj.__name__, field.name))
    return sorted(set(discovered))


def test_every_sign_typed_field_is_declared():
    undeclared = [
        f"{model}.{field}"
        for model, field in _sign_typed_fields()
        if declared(model, field) is None
    ]
    assert undeclared == [], (
        "undeclared sign-typed fields; add them to "
        "engine.astrology.sign_conventions.SIGN_FIELD_CONVENTIONS with the "
        f"convention their live values exhibit: {undeclared}"
    )


def test_no_stale_declarations():
    live = {f"{model}.{field}" for model, field in _sign_typed_fields()}
    stale = sorted(set(SIGN_FIELD_CONVENTIONS) - live)
    assert stale == [], f"declarations for fields that no longer exist: {stale}"


def test_declarations_match_live_values_and_accessors():
    instances = _walk(_chart_roots())
    assert instances, "object graph walk found nothing"
    checked = 0
    for instance in instances:
        model = type(instance).__name__
        for field in dataclasses.fields(instance):
            declaration = declared(model, field.name)
            if declaration is None:
                continue
            convention, _shape, accessor = declaration
            if not is_index(convention):
                continue
            value = getattr(instance, field.name)
            values = []
            if isinstance(value, int):
                values = [value]
            elif isinstance(value, dict):
                values = [v for v in value.values() if isinstance(v, int)] or \
                         [k for k in value.keys() if isinstance(k, int)]
            elif isinstance(value, (tuple, list)):
                values = [v for v in value if isinstance(v, int)]
            for observed in values:
                if convention == ZERO_BASED:
                    assert 0 <= observed <= 11, (model, field.name, observed)
                else:
                    assert 1 <= observed <= 12, (model, field.name, observed)
                checked += 1
            # The additive accessor must agree exactly with the raw
            # certified value under its declared convention.
            if accessor and isinstance(value, int):
                sign_object = getattr(instance, f"{accessor}_object")
                if convention == ZERO_BASED:
                    assert sign_object.zero_based == value
                    assert getattr(instance, f"{accessor}_one_based") == value + 1
                else:
                    assert sign_object.one_based == value
                    assert getattr(instance, f"{accessor}_zero_based") == value - 1
                assert sign_object.name == SIGN_NAMES[sign_object.one_based]
    assert checked > 100, f"expected a broad sample, checked {checked}"


def test_declared_conventions_are_only_the_two_certified_ones():
    for key, (convention, _shape, _accessor) in SIGN_FIELD_CONVENTIONS.items():
        assert convention in (ZERO_BASED, ONE_BASED, NOT_AN_INDEX), key


# ------------------------------------------------------------ Gate 4

def test_function_conventions_hold_over_dense_longitudes():
    step = 360.0 / 997
    for i in range(997):
        longitude = i * step + 0.0007  # off exact boundaries by design
        one_based = [
            zodiac_sign(longitude),
            kp_chain(longitude).sign_number,
        ] + list(aspected_signs("Sun", zodiac_sign(longitude)))
        zero_based = [
            navamsa_sign(longitude),
            dashamsa_sign(longitude),
            classify(longitude, D3_PARASHARA).d_sign,
        ]
        for value in one_based:
            assert 1 <= value <= 12, (longitude, value)
            assert Sign.from_one_based(value).zero_based == value - 1
        for value in zero_based:
            assert 0 <= value <= 11, (longitude, value)
            assert Sign.from_zero_based(value).one_based == value + 1


def test_rashi_level_layers_agree_on_the_same_sign():
    # D1 and the KP chain are both rashi-level and must name the same
    # sign for the same longitude, off exact boundaries (the KP layer
    # carries no boundary tolerance by certified design).
    step = 360.0 / 997
    for i in range(997):
        longitude = i * step + 0.0007
        d1 = Sign.from_one_based(zodiac_sign(longitude))
        kp = Sign.from_one_based(kp_chain(longitude).sign_number)
        assert d1 == kp, longitude
        assert d1.name == kp.name


def test_conversion_is_exactly_one_step_in_both_directions():
    for index in range(SIGN_COUNT):
        assert Sign.from_zero_based(index).one_based - 1 == index
        assert Sign.from_one_based(index + 1).zero_based + 1 == index + 1


def test_function_convention_registry_covers_the_sign_producers():
    assert set(SIGN_FUNCTION_CONVENTIONS.values()) == {ZERO_BASED, ONE_BASED}
    assert len(SIGN_FUNCTION_CONVENTIONS) == 6
