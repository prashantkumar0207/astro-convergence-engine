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
- Publication only (ADR-0130, narrowly superseding ADR-0120 D1 and AC11): a rule not marked synthetic is published
  only if its citation names an authorized source of its own school, listed in a sourced snapshot, with a locator
  naming chapter, verse and page. It is published for citation and never projected into evidence: rule_version()
  refuses it, so no evidence can name it before INTERPRETATION is entered. The pinned snapshot lists no source, so
  every rule it publishes is a synthetic fixture rule.

Nothing here evaluates a condition, applies a rule, reads a chart, scores or divides.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from engine.evidence.entity import DataClass, RecordProvenance
from engine.evidence.evidence import Domain, Polarity, ProducingSystem, RuleSpec, RuleVersion
from engine.evidence.evidence_identifiers import RUL_LAST, RuleId

#: A snapshot of rules alone. Its name is also the provenance schema of every projection rule_version() makes, so
#: it never changes: stored rule versions keep matching their publication (ADR-0124; ADR-0127).
SNAPSHOT_SCHEMA = "ace-rule-snapshot-v1"
#: A snapshot that also lists its authorized sources and independent verifications (ADR-0130).
SOURCED_SNAPSHOT_SCHEMA = "ace-rule-snapshot-v2"
#: What an independent verifier reviews before a genuine rule's claims may be marked independently checked.
VERIFIED_ASPECTS = ("statement", "locator", "condition", "domain", "polarity")
#: A genuine rule's locator, in its edition: "chapter 24, verse 109, page 325" or "chapter 24, verses 109-110, page 325".
LOCATOR_PATTERN = re.compile(r"chapter [1-9][0-9]*, verses? [1-9][0-9]*(-[1-9][0-9]*)?, pages? [1-9][0-9]*(-[1-9][0-9]*)?")
_SHA256 = re.compile(r"[0-9a-f]{64}")
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
        if not isinstance(self.synthetic, bool):
            raise RegistryError("a rule is marked synthetic, true or false; a genuine rule is published only from an "
                                "authorized source (ADR-0130)")
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


@dataclass(frozen=True, slots=True)
class AuthorizedSource:
    """A source genuine rules may cite: one edition of one work, for one school, with its witness and rights basis."""

    id: str
    school: ProducingSystem
    work: str
    edition: str
    language: str
    witness_url: str
    witness_sha256: str
    rights_basis: str

    def __post_init__(self):
        for name in ("id", "work", "edition", "language", "witness_url", "rights_basis"):
            _text(f"source {name}", self.__getattribute__(name))
        if not isinstance(self.school, ProducingSystem):
            raise RegistryError("an authorized source names its school")
        if not isinstance(self.witness_sha256, str) or _SHA256.fullmatch(self.witness_sha256) is None:
            raise RegistryError("an authorized source pins its witness by SHA-256")


@dataclass(frozen=True, slots=True)
class Verification:
    """An independent verifier's review of one genuine rule version and variant (H5 s4; ADR-0130)."""

    rule: RuleId
    version: int
    variant: str
    verifier: str
    transcription_sha256: str
    reviewed: tuple

    def __post_init__(self):
        if not isinstance(self.rule, RuleId) or isinstance(self.version, bool) or not isinstance(self.version, int):
            raise RegistryError("a verification names a rule version")
        _text("verification variant", self.variant)
        _text("verifier", self.verifier)
        if not isinstance(self.transcription_sha256, str) or _SHA256.fullmatch(self.transcription_sha256) is None:
            raise RegistryError("a verification pins the verifier's transcription by SHA-256")
        if self.reviewed != VERIFIED_ASPECTS:
            raise RegistryError(f"a verification reviews exactly {list(VERIFIED_ASPECTS)}")


def statement_digest(statement: str) -> str:
    """The SHA-256 of a statement after the declared normalisation: Unicode NFC, whitespace collapsed."""

    return hashlib.sha256(unicodedata.normalize("NFC", " ".join(statement.split())).encode("utf-8")).hexdigest()


def source_from_record(data) -> AuthorizedSource:
    data = _exact("an authorized source", data, ("id", "school", "work", "edition", "language", "witness_url",
                                                 "witness_sha256", "rights_basis"))
    try:
        school = ProducingSystem(data["school"])
    except ValueError as exc:
        raise RegistryError(f"an authorized source names an unknown school: {exc}") from exc
    return AuthorizedSource(id=data["id"], school=school, work=data["work"], edition=data["edition"],
                            language=data["language"], witness_url=data["witness_url"],
                            witness_sha256=data["witness_sha256"], rights_basis=data["rights_basis"])


def verification_from_record(data) -> Verification:
    data = _exact("a verification", data, ("rule", "version", "variant", "verifier", "transcription_sha256", "reviewed"))
    number = data["rule"]
    if isinstance(number, bool) or not isinstance(number, int) or not 1 <= number <= RUL_LAST:
        raise RegistryError(f"a verification names an issued rule number: {number!r}")
    if not isinstance(data["reviewed"], list):
        raise RegistryError("a verification lists what it reviewed")
    return Verification(rule=RuleId.from_number(number), version=data["version"], variant=data["variant"],
                        verifier=data["verifier"], transcription_sha256=data["transcription_sha256"],
                        reviewed=tuple(data["reviewed"]))


def _require_authorized(data: dict, sources: tuple) -> None:
    """A rule not marked synthetic is published only if it cites an authorized source of its own school, at a locator
    naming chapter, verse and page. Checked before the rule is built, so an unauthorized one is refused for this."""

    if data["synthetic"] is not False:
        return
    citation = data["citation"]
    source = citation["source"] if isinstance(citation, dict) and "source" in citation else None
    listed = [item for item in sources if item.id == source]
    if not listed or listed[0].school.value != data["school"]:
        raise RegistryError("the registry publishes synthetic rules only, unless a rule cites an authorized source of "
                            "its own school (ADR-0120 D1, AC11; ADR-0130)")
    locator = citation["locator"] if "locator" in citation else None
    if not isinstance(locator, str) or LOCATOR_PATTERN.fullmatch(locator) is None:
        raise RegistryError(f"a genuine rule's locator names chapter, verse and page in its edition: {locator!r} "
                            f"(ADR-0130)")


def rule_from_record(data, sources: tuple = ()) -> RegistryRule:
    """Rebuild a published rule, refusing any key the schema does not define (no free text, no code). A rule not
    marked synthetic needs an authorized source among `sources`; with none, only synthetic rules are accepted."""

    data = _exact("a rule record", data, RECORD_FIELDS)
    _require_authorized(data, sources)
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

    def __init__(self, rules: tuple, snapshot_sha256: str, sources: tuple = (), verifications: tuple = ()):
        self._rules = {(item.rule, item.version, item.variant): item for item in rules}
        self.snapshot_sha256 = snapshot_sha256
        self._sources = tuple(sources)
        self._verifications = tuple(verifications)

    def sources(self) -> tuple:
        return self._sources

    def verifications(self) -> tuple:
        return self._verifications

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
        """The evidence store's view of one published synthetic rule: what it must match exactly to register it. A genuine
        rule is published for citation only and is never projected, so no evidence can name it (ADR-0130). Every path
        into evidence, registration and every evidence read alike, goes through here and fails closed."""

        item = self.lookup(rule, version, variant)
        if item.synthetic is not True:
            raise RegistryError(f"{rule} version {version} variant {variant!r} is a genuine rule: published for citation "
                                f"and never projected into evidence until INTERPRETATION is entered (ADR-0130)")
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
    sourced = isinstance(data, dict) and "sources" in data
    data = _exact("the snapshot", data, ("schema", "rules", "sources", "verifications") if sourced else ("schema", "rules"))
    if data["schema"] != (SOURCED_SNAPSHOT_SCHEMA if sourced else SNAPSHOT_SCHEMA) or \
            not isinstance(data["rules"], list) or not data["rules"]:
        raise RegistryError("not a rule snapshot of this schema")
    sources, verifications = (), ()
    if sourced:
        if not isinstance(data["sources"], list) or not isinstance(data["verifications"], list):
            raise RegistryError("a sourced snapshot lists its sources and verifications")
        sources = tuple(source_from_record(record) for record in data["sources"])
        verifications = tuple(verification_from_record(record) for record in data["verifications"])
        if len({item.id for item in sources}) != len(sources):
            raise RegistryError("an authorized source is listed once")
    rules = tuple(rule_from_record(record, sources) for record in data["rules"])
    _require_verified(rules, verifications)
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
    return RuleRegistry(rules, pinned_sha256, sources, verifications)


def _require_verified(rules: tuple, verifications: tuple) -> None:
    """A genuine rule's claim marked independently checked needs a verification of that exact version and variant,
    whose transcription matches the published statement; a verification names a published genuine rule (H5 s4)."""

    genuine = {(item.rule, item.version, item.variant): item for item in rules if item.synthetic is not True}
    checked = {}
    for entry in verifications:
        identity = (entry.rule, entry.version, entry.variant)
        if identity not in genuine or identity in checked:
            raise RegistryError(f"{entry.rule} v{entry.version} {entry.variant!r}: a verification names one published "
                                f"genuine rule, once")
        checked[identity] = entry
    for identity, item in genuine.items():
        certification = item.certification
        claims = (certification.transcription_fidelity, certification.source_attribution,
                  certification.applicability_conditions)
        if ClaimState.INDEPENDENTLY_CHECKED not in claims:
            continue
        if identity not in checked:
            raise RegistryError(f"{item.rule} v{item.version} {item.variant!r} is marked independently checked with no "
                                f"independent verification (H5 s4; ADR-0130)")
        if checked[identity].transcription_sha256 != statement_digest(item.statement):
            raise RegistryError(f"{item.rule} v{item.version} {item.variant!r}: the independent transcription does not "
                                f"match the published statement (ADR-0130)")


_PINNED: list = []


def pinned() -> RuleRegistry:
    """The registry the evidence store uses: the snapshot under engine/, verified against the pin in this module."""

    if not _PINNED:
        _PINNED.append(load_registry(DATA_DIR, PINNED_SNAPSHOT_SHA256))
    return _PINNED[0]


__all__ = ["CONDITION_SCHEMA", "Citation", "ClaimState", "CertificationLevel", "Condition", "RegistryError",
           "RegistryRule", "RuleRegistry", "content_hash", "content_record", "canonical", "load_registry", "pinned",
           "read_history", "rule_from_record", "PINNED_SNAPSHOT_SHA256", "DATA_DIR", "AuthorizedSource", "Verification",
           "LOCATOR_PATTERN", "SOURCED_SNAPSHOT_SCHEMA", "VERIFIED_ASPECTS", "source_from_record", "statement_digest",
           "verification_from_record"]
