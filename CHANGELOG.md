# Changelog

All notable changes to KES_Water are documented in this file.

The project follows semantic versioning for application releases and Alembic revision identifiers for database schema changes.

## [Unreleased]

### Added

- Enterprise Water Balance V2 under mission `KESW-S3-M1`
- Decimal-based Water Balance engineering domain engine
- Enterprise Water Balance request and response schemas
- Water Accounting Zone-aware calculation service
- Versioned engineering calculation endpoint:
  `POST /api/v1/engineering/water-balance/calculate`
- Configurable Water Accounting Zone audit tolerance
- Signed and absolute balance-error calculations
- Balance error and closure percentages
- Unaccounted and over-accounted water calculations
- Gross water demand and internal reuse percentage
- BALANCED, IMBALANCED, NO_FLOW, and INDETERMINATE statuses
- Domain validation for Boolean, invalid, non-finite, and negative inputs
- Audit-tolerance range validation
- Water Balance engine tests
- Water Balance schema tests
- Water Balance service tests
- Water Balance API tests
- Development dependencies in `backend/requirements-dev.txt`

### Changed

- Registered the Enterprise Water Balance API in the versioned API router
- Classified internal reuse as a circularity KPI instead of boundary inflow
- Applied Water Accounting Zone audit tolerance through the service layer
- Updated project status for Enterprise Water Balance V2 completion

### Preserved

- Legacy Water Balance calculator remains unchanged
- Legacy dormant Water Balance route remains unchanged
- Enterprise backup remains retained and must not be deleted

### Validated

- Live API request returned HTTP 200
- Boundary inflow verified at 120 m3
- Boundary outflow verified at 100 m3
- Net storage change verified at 20 m3
- Signed balance error verified at 0 m3
- Balance closure verified at 100%
- Internal reuse verified at 25%
- Applied audit tolerance verified at 5%
- BALANCED status verified
- Engine tests: 27 passed
- Schema tests: 18 passed
- Service tests: 13 passed
- API tests: 7 passed
- Combined automated result: 65 passed
- Coverage result: 224 of 224 statements, 100%
- Python compile validation passed
- Git whitespace validation passed

### Planned

- Water Balance calculation persistence and audit trail
- Calculation history and filtering APIs
- Physics and unit validation for remaining retained calculators
- Engineering calculation project persistence
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