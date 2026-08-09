"""
Parashari school layer.

Isolated per the school-separation rule: separate modules per school,
never one conflated engine. Consumes only certified shared facts
(sidereal positions, whole-sign houses) computed under the
PARASHARI_LAHIRI profile. Nothing here is imported by the KP, dasha,
varga, or transit layers.

Current scope: PARASHARI_DRISHTI_V1 (graha drishti, full aspects).
"""
