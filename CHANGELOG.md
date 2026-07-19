# Changelog

All notable changes to KES_Water are documented in this file.

The project follows semantic versioning for application releases and Alembic revision identifiers for database schema changes.

## [Unreleased]

### Planned

- Water Balance engineering domain review
- Physics and unit validation for retained calculators
- Engineering calculation project persistence
- Versioned engineering APIs
- Automated regression tests
- Authentication and authorization
- React enterprise frontend
- Docker deployment validation

## [1.0.0] - 2026-07-19

### Added

- Enterprise FastAPI application foundation
- PostgreSQL database integration
- SQLAlchemy 2.x models and session management
- Alembic database migrations
- Pydantic v2 request and response schemas
- Pydantic Settings configuration
- Loguru application logging
- CORS configuration
- Versioned API router under `/api/v1`
- Swagger and OpenAPI documentation
- Repository and service layers
- Central exception handling
- Production-oriented non-root Dockerfile
- Safe `.gitignore`
- Placeholder-only `.env.example`

### Organization Module

- Organization model
- Organization schemas
- Organization repository
- Organization service
- Organization API
- Full CRUD validation
- Organizations database migration

### Plant Module

- Plant model
- Plant schemas
- Plant repository
- Plant service
- Plant API
- Organization ownership validation
- Full CRUD validation
- Plants database migration

### Water Accounting Zone Module

- Water Accounting Zone model
- Water Accounting Zone schemas
- Water Accounting Zone repository
- Water Accounting Zone service
- Water Accounting Zone API
- Organization and Plant ownership validation
- Parent-zone validation
- Duplicate zone-code protection
- Baseline date and consumption constraints
- Metering coverage constraints
- Audit tolerance constraints
- Full CRUD validation
- Filter validation
- Water Accounting Zones database migration
- Retained main zone `MOH-WAZ-01`

### Consolidation

- Established `kamracp/KES_Water` as the canonical repository
- Retained legacy Kamra Water OS Git history
- Retained Water Balance calculator
- Retained Pump Selection calculator
- Retained Pipeline Sizing calculator
- Retained Tank Design calculator
- Retained Pump Head calculator
- Retained Friction Loss calculator
- Retained enterprise backup pending final verification and archival decision

### Database Revisions

- `c1444267cc45` — Create Organizations table
- `d2e92f26bce6` — Create Plants table
- `67f3d7e90039` — Create Water Accounting Zones table

### Verified Retained Records

- Organization ID `2` — Kamra Engineering Solutions
- Plant ID `1` — KES Mohali Water Engineering Plant
- Water Accounting Zone ID `1` — KES Mohali Main Water Accounting Zone

### Security

- Excluded local environment files from Git
- Excluded virtual environments from Git
- Excluded logs and Python caches from Git
- Confirmed `.env.example` remains trackable