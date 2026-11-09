"""The seeded event-class vocabulary (ADR-0113 s2 C1; ADR-0115 s3; H1 s3).

Event class is a controlled vocabulary, never free text. The seed is exactly the 47 rows of
knowledge/hlkg/domains/career/CAREER_EVENT_REGISTRY.md s3, in registry order, each with its group
and its registered origin. Further classes are admitted only by a governed change to that registry;
scripts/check_event_identifiers.py fails when this table and the registry disagree.

Recording a row's origin decides nothing: the registry stays DRAFT, and its open items stay open.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

#: The registered EV-CAR family (docs/NAMING_STANDARD.md s2): domain-local, three digits.
CLASS_PATTERN = re.compile(r"EV-CAR-\d{3}")
#: The domain the EV-CAR family is local to.
CLASS_DOMAIN = "career"
REGISTRY_PATH = "knowledge/hlkg/domains/career/CAREER_EVENT_REGISTRY.md"


class ClassOrigin(Enum):
    """The registry's own origin column, carried as recorded."""

    MODEL = "MODEL"
    PROPOSED_ADDITION = "PROPOSED-ADDITION"


MODEL = ClassOrigin.MODEL
PROPOSED_ADDITION = ClassOrigin.PROPOSED_ADDITION


@dataclass(frozen=True, slots=True)
class EventClass:
    """One registered event class: identifier, name, group and origin, as the registry states them."""

    class_id: str
    name: str
    group: str
    origin: ClassOrigin


SEED = (
    EventClass('EV-CAR-001', 'first_employment', 'entry', MODEL),
    EventClass('EV-CAR-002', 'workforce_reentry', 'entry', MODEL),
    EventClass('EV-CAR-043', 'employment_obtained', 'entry', PROPOSED_ADDITION),
    EventClass('EV-CAR-044', 'offer_received', 'entry', PROPOSED_ADDITION),
    EventClass('EV-CAR-003', 'promotion', 'progression', MODEL),
    EventClass('EV-CAR-004', 'grade_rise', 'progression', MODEL),
    EventClass('EV-CAR-005', 'scope_expansion', 'progression', MODEL),
    EventClass('EV-CAR-006', 'leadership_appointment', 'progression', MODEL),
    EventClass('EV-CAR-007', 'pay_raise', 'progression', MODEL),
    EventClass('EV-CAR-008', 'role_change', 'lateral', MODEL),
    EventClass('EV-CAR-009', 'employer_change', 'lateral', MODEL),
    EventClass('EV-CAR-010', 'transfer', 'lateral', MODEL),
    EventClass('EV-CAR-011', 'secondment', 'lateral', MODEL),
    EventClass('EV-CAR-012', 'foreign_posting', 'lateral', MODEL),
    EventClass('EV-CAR-013', 'posting_return', 'lateral', MODEL),
    EventClass('EV-CAR-014', 'profession_change', 'reorientation', MODEL),
    EventClass('EV-CAR-015', 'industry_change', 'reorientation', MODEL),
    EventClass('EV-CAR-016', 'employment_mode_switch', 'reorientation', MODEL),
    EventClass('EV-CAR-045', 'second_career_start', 'reorientation', PROPOSED_ADDITION),
    EventClass('EV-CAR-017', 'resignation', 'separation', MODEL),
    EventClass('EV-CAR-018', 'termination', 'separation', MODEL),
    EventClass('EV-CAR-019', 'layoff', 'separation', MODEL),
    EventClass('EV-CAR-020', 'contract_end', 'separation', MODEL),
    EventClass('EV-CAR-021', 'business_start', 'venture', MODEL),
    EventClass('EV-CAR-022', 'business_expansion', 'venture', MODEL),
    EventClass('EV-CAR-023', 'business_pivot', 'venture', MODEL),
    EventClass('EV-CAR-024', 'venture_partnership_formation', 'venture', MODEL),
    EventClass('EV-CAR-025', 'venture_partnership_dissolution', 'venture', MODEL),
    EventClass('EV-CAR-026', 'business_closure', 'venture', MODEL),
    EventClass('EV-CAR-027', 'business_sale', 'venture', MODEL),
    EventClass('EV-CAR-028', 'career_break_start', 'interruption', MODEL),
    EventClass('EV-CAR-029', 'career_break_end', 'interruption', MODEL),
    EventClass('EV-CAR-030', 'sabbatical', 'interruption', MODEL),
    EventClass('EV-CAR-031', 'suspension', 'interruption', MODEL),
    EventClass('EV-CAR-032', 'award', 'recognition', MODEL),
    EventClass('EV-CAR-033', 'milestone', 'recognition', MODEL),
    EventClass('EV-CAR-034', 'appraisal_outcome', 'recognition', MODEL),
    EventClass('EV-CAR-035', 'professional_honour', 'recognition', MODEL),
    EventClass('EV-CAR-036', 'demotion', 'adversity', MODEL),
    EventClass('EV-CAR-037', 'disciplinary_action', 'adversity', MODEL),
    EventClass('EV-CAR-038', 'stagnation_onset', 'adversity', MODEL),
    EventClass('EV-CAR-046', 'workplace_conflict_onset', 'adversity', PROPOSED_ADDITION),
    EventClass('EV-CAR-047', 'workplace_conflict_resolution', 'adversity', PROPOSED_ADDITION),
    EventClass('EV-CAR-039', 'retirement', 'exit', MODEL),
    EventClass('EV-CAR-040', 'early_exit', 'exit', MODEL),
    EventClass('EV-CAR-041', 'career_end', 'exit', MODEL),
    EventClass('EV-CAR-042', 'postretirement_engagement', 'exit', MODEL),
)

#: Lookup by identifier. Built once; the seed is fixed at import.
CLASSES = {entry.class_id: entry for entry in SEED}


def registered(class_id: str) -> bool:
    """Whether `class_id` names a registered event class."""

    return isinstance(class_id, str) and class_id in CLASSES
