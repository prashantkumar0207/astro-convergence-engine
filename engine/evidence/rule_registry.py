"""The interpretation rule registry: the H5 specification's rule record, read only from a pinned snapshot (ADR-0120).

- Rules are data (ADR-0112 D-3), inside engine/ (D-2), reached only through an immutable snapshot
  whose SHA-256 is pinned in this module (D-1). Loading checks the manifest, the pin, the bytes and
  the schema, and every mismatch fails closed. Nothing reads top-level knowledge/ (ADR-0030 clause 1).
- RUL identity (ADR-0121): the governed authoring process, scripts/author_rule_registry.py, is the
  only RUL issuer, recorded in a persistent, append-only allocation history. A snapshot publishes
  issued identities; it never allocates. Every published rule is checked against that history.
- The record (H5 s2): RUL identity and version; school, never inferred; a checkable citation; the
  statement in the source's terms, kept apart from the machine-applicable condition, which is data
  under a declared schema and never code; activation conditions; effect, polarity and domain; named
  variants, selected explicitly, with no default (ADR-0120 D4); and a certification level whose four
  claims are separate (H5 s4).
- Synthetic only (ADR-0120 D1): every published rule is a synthetic fixture rule.

Nothing here evaluates a condition, applies a rule, reads a chart, scores or divides.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from engine.evidence.entity import DataClass, RecordProvenance
from engine.evidence.evidence import Domain, Polarity, ProducingSystem, RuleSpec, RuleVersion
from engine.evidence.evidence_identifiers import RUL_LAST, RuleId

SNAPSHOT_SCHEMA = "ace-rule-snapshot-v1"
MANIFEST_SCHEMA = "ace-rule-snapshot-manifest-v1"
HISTORY_SCHEMA = "ace-rul-allocation-history-v1"
DATA_DIR = Path(__file__).resolve().parent / "rule_registry_data"
MANIFEST_NAME = "MANIFEST.json"
HISTORY_NAME = "allocation_history.json"
#: The pinned snapshot (ADR-0112 D-1). Changing the snapshot requires changing this pin, in a reviewed commit.
PINNED_SNAPSHOT_SHA256 = "ea8d185ff0786e1c2d68b8010b45b9721367e8e55efca49a4c1a4b8402643d0d"

PLANETS = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu")
#: The declared condition schema: each kind, and the type of each parameter. A condition is data, never code.
CONDITION_SCHEMA = {
    "planet_in_house": {"planet": "planet", "house": "house"},
    "planet_in_sign": {"planet": "planet", "sign": "sign"},
    "house_lord_in_house": {"lord_of": "house", "house": "house"},
    "cusp_sublord_signifies": {"cusp": "house", "houses": "houses"},
}
RECORD_FIELDS = ("rule", "key", "version", "variant", "school", "citation", "statement", "condition",
                 "activation_conditions", "effect", "polarity", "domain", "known_variants", "certification",
                 "declared_strength", "synthetic", "content_hash")


class RegistryError(ValueError):
    """The pinned registry cannot be trusted, or a request is not for a registered rule."""


class ClaimState(Enum):
    """One H5 s4 claim's state. Each of the four claims is recorded on its own; none implies another."""

    NOT_ASSESSED = "not_assessed"
    DECLARED_BY_AUTHOR = "declared_by_author"
    INDEPENDENTLY_CHECKED = "independently_checked"


def _text(name: str, value) -> None:
    if not isinstance(value, str) or not value.strip():
        raise RegistryError(f"{name} must be non-empty text")


@dataclass(frozen=True, slots=True)
class Citation:
    """A source cited precisely enough to be checked by someone who owns the text (H5 s2; ADR-0120 AC10)."""

    source: str
    locator: str

    def __post_init__(self):
        _text("citation source", self.source)
        _text("citation locator", self.locator)


@dataclass(frozen=True, slots=True)
class Condition:
    """A machine-applicable condition: a declared kind and its typed parameters. Data only; nothing evaluates it."""

    kind: str
    parameters: tuple

    def __post_init__(self):
        if self.kind not in CONDITION_SCHEMA:
            raise RegistryError(f"condition kind {self.kind!r} is not in the declared schema")
        if not isinstance(self.parameters, tuple) or not all(
                isinstance(pair, tuple) and len(pair) == 2 for pair in self.parameters):
            raise RegistryError("condition parameters are (name, value) pairs")
        names = [name for name, _value in self.parameters]
        if sorted(names) != sorted(CONDITION_SCHEMA[self.kind]) or len(set(names)) != len(names):
            raise RegistryError(f"a {self.kind} condition takes exactly {sorted(CONDITION_SCHEMA[self.kind])}")
        for name, value in self.parameters:
            _typed(f"{self.kind}.{name}", CONDITION_SCHEMA[self.kind][name], value)


def _typed(name: str, kind: str, value) -> None:
    number = lambda item: not isinstance(item, bool) and isinstance(item, int) and 1 <= item <= 12
    if kind == "planet" and value not in PLANETS:
        raise RegistryError(f"{name} must name one of {PLANETS}")
    if kind in ("house", "sign") and not number(value):
        raise RegistryError(f"{name} must be a number from 1 to 12")
    if kind == "houses" and not (isinstance(value, tuple) and value and all(number(item) for item in value)
                                 and len(set(value)) == len(value)):
        raise RegistryError(f"{name} must be distinct numbers from 1 to 12")


@dataclass(frozen=True, slots=True)
class CertificationLevel:
    """H5 s4's four claims, kept apart. Measured performance is absent in WP-E5 (ADR-0120 AC3)."""

    transcription_fidelity: ClaimState
    source_attribution: ClaimState
    applicability_conditions: ClaimState
    measured_performance: None

    def __post_init__(self):
        for name in ("transcription_fidelity", "source_attribution", "applicability_conditions"):
            if not isinstance(self.__getattribute__(name), ClaimState):
                raise RegistryError(f"{name} is a ClaimState")
        if self.measured_performance is not None:
            raise RegistryError("measured performance is absent in WP-E5: nothing here measures a rule")


@dataclass(frozen=True, slots=True)
class RegistryRule:
    """One published rule version under one named variant."""

    rule: RuleId
    key: str
    version: int
    variant: str
    school: ProducingSystem
    citation: Citation
    statement: str
    condition: Condition
    activation_conditions: tuple
    effect: str
    polarity: Polarity
    domain: Domain
    known_variants: tuple
    certification: CertificationLevel
    declared_strength: str
    synthetic: bool
    content_hash: str

    def __post_init__(self):
        if not isinstance(self.rule, RuleId):
            raise RegistryError("a rule is identified by its RUL identifier")
        _text("key", self.key)
        if isinstance(self.version, bool) or not isinstance(self.version, int) or self.version < 1:
            raise RegistryError("a rule version is an integer from 1")
        _text("variant", self.variant)
        if not isinstance(self.school, ProducingSystem):
            raise RegistryError("a rule's school is a ProducingSystem, stated, never inferred")
        if not isinstance(self.citation, Citation):
            raise RegistryError("every rule carries a citation (ADR-0120 AC10)")
        _text("statement", self.statement)
        if not isinstance(self.condition, Condition):
            raise RegistryError("a rule's machine-applicable condition is a Condition")
        if not isinstance(self.activation_conditions, tuple) or \
                not all(isinstance(item, Condition) for item in self.activation_conditions):
            raise RegistryError("activation conditions are a tuple of Conditions")
        _text("effect", self.effect)
        if not isinstance(self.polarity, Polarity) or not isinstance(self.domain, Domain):
            raise RegistryError("a rule states its polarity and domain")
        if not isinstance(self.known_variants, tuple) or not self.known_variants or \
                self.variant not in self.known_variants or len(set(self.known_variants)) != len(self.known_variants):
            raise RegistryError("known variants are named, distinct, and include this record's variant")
        if not isinstance(self.certification, CertificationLevel):
            raise RegistryError("a rule carries its certification level")
        _text("declared_strength", self.declared_strength)
        if self.synthetic is not True:
            raise RegistryError("WP-E5 publishes synthetic rules only; real population needs its own authorization "
                                "(ADR-0120 D1, AC11)")
        if self.content_hash != content_hash(self):
            raise RegistryError(f"{self.rule} v{self.version} {self.variant}: the content hash does not match the "
                                f"published content")


def _condition_record(condition: Condition) -> dict:
    return {"kind": condition.kind,
            "parameters": {name: (list(value) if isinstance(value, tuple) else value)
                           for name, value in condition.parameters}}


def _condition_from(data) -> Condition:
    data = _exact("condition", data, ("kind", "parameters"))
    if not isinstance(data["parameters"], dict):
        raise RegistryError("condition parameters are an object")
    return Condition(kind=data["kind"], parameters=tuple(sorted(
        (name, tuple(value) if isinstance(value, list) else value) for name, value in data["parameters"].items())))


def content_record(rule) -> dict:
    """The published content of a rule version: every field except its content hash, in canonical form."""

    certification = rule.certification
    identity: RuleId = rule.rule
    return {"rule": identity.number, "key": rule.key, "version": rule.version, "variant": rule.variant,
            "school": rule.school.value, "citation": {"source": rule.citation.source, "locator": rule.citation.locator},
            "statement": rule.statement, "condition": _condition_record(rule.condition),
            "activation_conditions": [_condition_record(item) for item in rule.activation_conditions],
            "effect": rule.effect, "polarity": rule.polarity.value, "domain": rule.domain.value,
            "known_variants": list(rule.known_variants),
            "certification": {"transcription_fidelity": certification.transcription_fidelity.value,
                              "source_attribution": certification.source_attribution.value,
                              "applicability_conditions": certification.applicability_conditions.value,
                              "measured_performance": None},
            "declared_strength": rule.declared_strength, "synthetic": rule.synthetic}


def canonical(data) -> bytes:
    return (json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode("ascii")


def content_hash(rule) -> str:
    return hashlib.sha256(canonical(content_record(rule))).hexdigest()


def _exact(name: str, data, expected) -> dict:
    if not isinstance(data, dict) or set(data) != set(expected):
        extra = sorted(set(data) - set(expected)) if isinstance(data, dict) else data
        raise RegistryError(f"{name} carries only its schema's fields; refused: {extra}")
    return data


def rule_from_record(data) -> RegistryRule:
    """Rebuild a published rule, refusing any key the schema does not define (no free text, no code)."""

    data = _exact("a rule record", data, RECORD_FIELDS)
    citation = _exact("citation", data["citation"], ("source", "locator"))
    certification = _exact("certification", data["certification"],
                           ("transcription_fidelity", "source_attribution", "applicability_conditions",
                            "measured_performance"))
    number = data["rule"]
    if isinstance(number, bool) or not isinstance(number, int) or not 1 <= number <= RUL_LAST:
        raise RegistryError(f"a published rule number must be an issued integer: {number!r}")
    if not isinstance(data["activation_conditions"], list) or not isinstance(data["known_variants"], list):
        raise RegistryError("activation conditions and known variants are lists")
    try:
        school, polarity, domain = (ProducingSystem(data["school"]), Polarity(data["polarity"]),
                                    Domain(data["domain"]))
        states = [ClaimState(certification[name]) for name in
                  ("transcription_fidelity", "source_attribution", "applicability_conditions")]
    except ValueError as exc:
        raise RegistryError(f"a rule record names an unknown value: {exc}") from exc
    return RegistryRule(
        rule=RuleId.from_number(number), key=data["key"], version=data["version"], variant=data["variant"],
        school=school, citation=Citation(source=citation["source"], locator=citation["locator"]),
        statement=data["statement"], condition=_condition_from(data["condition"]),
        activation_conditions=tuple(_condition_from(item) for item in data["activation_conditions"]),
        effect=data["effect"], polarity=polarity, domain=domain, known_variants=tuple(data["known_variants"]),
        certification=CertificationLevel(transcription_fidelity=states[0], source_attribution=states[1],
                                         applicability_conditions=states[2],
                                         measured_performance=certification["measured_performance"]),
        declared_strength=data["declared_strength"], synthetic=data["synthetic"], content_hash=data["content_hash"])


def read_history(path: Path) -> dict:
    """The RUL allocation history: number -> (key, school). Contiguous from 1, unique, never reused (ADR-0121)."""

    try:
        data = json.loads(path.read_bytes())
    except (OSError, ValueError) as exc:
        raise RegistryError(f"the RUL allocation history cannot be read: {exc}") from exc
    data = _exact("the allocation history", data, ("schema", "allocations"))
    if data["schema"] != HISTORY_SCHEMA or not isinstance(data["allocations"], list):
        raise RegistryError("not an allocation history of this schema")
    bound, keys = {}, set()
    for position, entry in enumerate(data["allocations"], 1):
        entry = _exact("an allocation", entry, ("number", "key", "school"))
        if entry["number"] != position:
            raise RegistryError(f"allocation {position} records number {entry['number']}; numbers are issued once, "
                                f"in order, from 1, and never reused")
        if entry["key"] in keys:
            raise RegistryError(f"rule key {entry['key']!r} was issued twice")
        try:
            school = ProducingSystem(entry["school"])
        except ValueError as exc:
            raise RegistryError(f"allocation {position} names an unknown school") from exc
        keys.add(entry["key"])
        bound[position] = (entry["key"], school)
    return bound


class RuleRegistry:
    """The published rules of one verified snapshot. Construct only through load_registry or pinned()."""

    def __init__(self, rules: tuple, snapshot_sha256: str):
        self._rules = {(item.rule, item.version, item.variant): item for item in rules}
        self.snapshot_sha256 = snapshot_sha256

    def lookup(self, rule: RuleId, version: int, variant: str) -> RegistryRule:
        """The published rule for this exact identity, version and explicit variant; anything else is refused."""

        if not isinstance(rule, RuleId) or not isinstance(variant, str):
            raise RegistryError("a lookup names a RUL identifier, a version and an explicit variant")
        if (rule, version, variant) not in self._rules:
            raise RegistryError(f"{rule} version {version} variant {variant!r} is not registered")
        return self._rules[(rule, version, variant)]

    def rules(self) -> tuple:
        return tuple(self._rules[identity] for identity in sorted(self._rules))

    def versions(self, rule: RuleId) -> tuple:
        found = sorted({version for identity, version, _variant in self._rules if identity == rule})
        if not found:
            raise RegistryError(f"{rule} is not registered")
        return tuple(found)

    def variants(self, rule: RuleId, version: int) -> tuple:
        found = sorted(variant for identity, number, variant in self._rules if (identity, number) == (rule, version))
        if not found:
            raise RegistryError(f"{rule} version {version} is not registered")
        return tuple(found)

    def by_key(self, key: str) -> RuleId:
        found = {item.rule for item in self._rules.values() if item.key == key}
        if len(found) != 1:
            raise RegistryError(f"rule key {key!r} is not registered")
        return found.pop()

    def rule_version(self, rule: RuleId, version: int, variant: str) -> RuleVersion:
        """The evidence store's view of one published rule: what it must match exactly to register it."""

        item = self.lookup(rule, version, variant)
        return RuleVersion(rule=item.rule, version=item.version, spec=RuleSpec(
            school=item.school, content_hash=item.content_hash, knowledge_snapshot_hash=self.snapshot_sha256,
            declared_strength=item.declared_strength, variant=item.variant,
            provenance=RecordProvenance(source="the pinned rule registry", method="published snapshot",
                                        schema_version=SNAPSHOT_SCHEMA),
            data_class=DataClass.SYNTHETIC))


def load_registry(directory: Path, pinned_sha256: str) -> RuleRegistry:
    """Load and verify a snapshot. A missing file, a changed byte, a changed pin, a schema violation, an identity
    the history never issued, or a rebinding each fails closed (ADR-0120 AC5; ADR-0121)."""

    try:
        manifest = json.loads((directory / MANIFEST_NAME).read_bytes())
    except (OSError, ValueError) as exc:
        raise RegistryError(f"the snapshot manifest cannot be read: {exc}") from exc
    manifest = _exact("the manifest", manifest, ("schema", "snapshot", "sha256"))
    if manifest["schema"] != MANIFEST_SCHEMA or not isinstance(manifest["snapshot"], str) or \
            "/" in manifest["snapshot"] or "\\" in manifest["snapshot"]:
        raise RegistryError("not a snapshot manifest of this schema")
    if manifest["sha256"] != pinned_sha256:
        raise RegistryError("the manifest's snapshot hash differs from the pinned hash; refusing to load")
    try:
        raw = (directory / manifest["snapshot"]).read_bytes()
    except OSError as exc:
        raise RegistryError(f"the pinned snapshot cannot be read: {exc}") from exc
    if hashlib.sha256(raw).hexdigest() != pinned_sha256:
        raise RegistryError("the snapshot's bytes do not match the pinned hash; refusing to load")
    try:
        data = json.loads(raw)
    except ValueError as exc:
        raise RegistryError(f"the snapshot is not valid JSON: {exc}") from exc
    data = _exact("the snapshot", data, ("schema", "rules"))
    if data["schema"] != SNAPSHOT_SCHEMA or not isinstance(data["rules"], list) or not data["rules"]:
        raise RegistryError("not a rule snapshot of this schema")
    rules = tuple(rule_from_record(record) for record in data["rules"])
    issued = read_history(directory / HISTORY_NAME)
    identities = set()
    for item in rules:
        rule_id: RuleId = item.rule
        if rule_id.number not in issued:
            raise RegistryError(f"{item.rule} was never issued by the authoring process; a snapshot never allocates")
        binding = issued[rule_id.number]
        if binding != (item.key, item.school):
            raise RegistryError(f"{item.rule} is bound to {binding[0]!r} ({binding[1].value}) in the allocation "
                                f"history; the snapshot rebinds it to {item.key!r} ({item.school.value})")
        identity = (item.rule, item.version, item.variant)
        if identity in identities:
            raise RegistryError(f"{item.rule} version {item.version} variant {item.variant!r} is published twice")
        identities.add(identity)
    for rule in {item.rule for item in rules}:
        versions = sorted({item.version for item in rules if item.rule == rule})
        if versions != list(range(1, len(versions) + 1)):
            raise RegistryError(f"{rule}'s published versions are not 1..n: {versions}")
    return RuleRegistry(rules, pinned_sha256)


_PINNED: list = []


def pinned() -> RuleRegistry:
    """The registry the evidence store uses: the snapshot under engine/, verified against the pin in this module."""

    if not _PINNED:
        _PINNED.append(load_registry(DATA_DIR, PINNED_SNAPSHOT_SHA256))
    return _PINNED[0]


__all__ = ["CONDITION_SCHEMA", "Citation", "ClaimState", "CertificationLevel", "Condition", "RegistryError",
           "RegistryRule", "RuleRegistry", "content_hash", "content_record", "canonical", "load_registry", "pinned",
           "read_history", "rule_from_record", "PINNED_SNAPSHOT_SHA256", "DATA_DIR"]
