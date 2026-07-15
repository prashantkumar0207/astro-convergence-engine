# Knowledge Engine Specification

| Field | Value |
|------|------|
| Status | DRAFT |
| Version | 0.1.0 |
| Owner | Astro Convergence Engine |
| Last Updated | 2026-07-15 |
| Depends On | HLKG_SPEC.md, DOMAIN_REGISTRY_SPEC.md |

---

# 1. Purpose

The Knowledge Engine is responsible for loading, validating, indexing, caching and exposing all structured knowledge used by the Astro Convergence Engine.

Every module interacts with structured knowledge only through this engine.

---

# 2. Responsibilities

The Knowledge Engine SHALL:

- Load knowledge files
- Validate against schemas
- Build registries
- Resolve aliases
- Construct relationship graphs
- Cache loaded knowledge
- Expose read-only APIs

The Knowledge Engine SHALL NOT:

- Perform astrology calculations
- Generate predictions
- Execute inference logic

---

# 3. Inputs

- JSON
- YAML
- Markdown metadata

Located under:

knowledge/
schemas/
examples/

---

# 4. Outputs

Immutable in-memory objects.

Examples:

- Domain
- Question
- Relationship
- Parameter
- Outcome

---

# 5. Components

Loader

Validator

Registry

Relationship Graph

Cache

Public API

---

# 6. Public API

load()

validate()

build_registry()

build_graph()

get_domain()

get_question()

get_relationship()

search()

---

# 7. Design Rules

Knowledge is immutable after loading.

Validation always occurs before registration.

Every identifier must be globally unique.

No module accesses knowledge files directly.

Knowledge Engine is the single source of truth.

---

# 8. Future Modules

loader.py

validator.py

registry.py

graph.py

cache.py

models.py

exceptions.py