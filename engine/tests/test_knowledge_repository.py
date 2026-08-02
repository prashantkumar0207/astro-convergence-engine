from engine.knowledge.repository import KnowledgeRepository


def test_repository_loads_planets():
    planets = KnowledgeRepository.planets()
    assert isinstance(planets, dict)
    assert "schema_version" in planets
    assert "metadata" in planets
    assert "planets" in planets


def test_repository_loads_signs():
    signs = KnowledgeRepository.signs()
    assert isinstance(signs, dict)
    assert "schema_version" in signs
    assert "metadata" in signs
    assert "signs" in signs


def test_repository_loads_houses():
    houses = KnowledgeRepository.houses()
    assert isinstance(houses, dict)
    assert "schema_version" in houses
    assert "metadata" in houses
    assert "houses" in houses


def test_repository_loads_dignities():
    dignities = KnowledgeRepository.dignities()
    assert isinstance(dignities, dict)
    assert "schema_version" in dignities
    assert "metadata" in dignities
    assert "dignities" in dignities


def test_repository_loads_relationships():
    relationships = KnowledgeRepository.natural_relationships()
    assert isinstance(relationships, dict)
    assert "schema_version" in relationships
    assert "metadata" in relationships
    assert "relationships" in relationships


def test_repository_loads_nakshatras():
    nakshatras = KnowledgeRepository.nakshatras()
    assert isinstance(nakshatras, dict)
    assert "schema_version" in nakshatras
    assert "metadata" in nakshatras
    assert "nakshatras" in nakshatras