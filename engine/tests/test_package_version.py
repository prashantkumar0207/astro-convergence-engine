from engine.astrology.__version__ import __version__
from engine.version import ENGINE_VERSION


def test_package_version_derives_from_single_source():
    assert __version__ == ENGINE_VERSION
