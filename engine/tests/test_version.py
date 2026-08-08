from engine.astrology.version import VERSION
from engine.version import ENGINE_VERSION


def test_version_derives_from_single_source():
    assert VERSION == ENGINE_VERSION
