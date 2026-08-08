from engine.astrology.version_info import ENGINE_VERSION
from engine.version import ENGINE_VERSION as CANONICAL


def test_engine_version_derives_from_single_source():
    assert ENGINE_VERSION == CANONICAL
