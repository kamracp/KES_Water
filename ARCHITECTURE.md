# KES_Water Architecture

## Purpose

KES_Water is an enterprise water engineering, accounting, and intelligence platform built for industrial plants, utilities, buildings, and water-treatment systems.

## Architectural Style

The backend follows a layered modular architecture:

1. API layer
2. Service layer
3. Repository layer
4. Data model layer
5. PostgreSQL database
6. Engineering domain engines

Engineering domain engines remain independent from HTTP and database concerns.

## Backend Layers

### API Layer

Location: `backend/app/api/`

Responsibilities:

- Define FastAPI routes
- Validate request parameters
- Inject database sessions
- Select response schemas
- Map domain errors to API responses
- Return HTTP status codes

### Service Layer

Location: `backend/app/services/`

Responsibilities:

- Apply business rules
- Validate entity ownership
- Detect duplicate records
- Coordinate repositories
- Invoke engineering domain engines
- Raise application-level HTTP errors

### Repository Layer

Location: `backend/app/repositories/`

Responsibilities:

- Execute SQLAlchemy queries
- Create, update, retrieve, and delete records
- Commit database transactions
- Roll back failed transactions

### Schema Layer

Location: `backend/app/schemas/`

Responsibilities:

- Validate API input
- Define response contracts
- Validate units and operating ranges
- Support Pydantic serialization
- Protect the domain layer from invalid API data

### Model Layer

Location: `backend/app/models/`

Responsibilities:

- Define SQLAlchemy database tables
- Define relationships and constraints
- Define indexes and foreign keys
- Protect database integrity

### Engineering Core

Location: `backend/app/engineering_core/`

Responsibilities:

- Contain engineering formulas
- Define units and assumptions
- Perform deterministic calculations
- Use Decimal-based arithmetic where calculation precision requires it
- Remain independent from HTTP routing
- Remain independent from database sessions
- Support regression and domain testing

## Enterprise Data Hierarchy

- Organization
  - Plant
    - Water Accounting Zone
      - Enterprise engineering calculations
      - Future meters and measurement points
      - Future water streams
      - Future calculation projects
      - Future audit and balance history

## Current Modules

### Organization

Represents the enterprise or customer account.

### Plant

Represents an industrial facility or operational site belonging to an organization.

### Water Accounting Zone

Represents a water-audit, operational, or hydraulic boundary within a plant.

The Water Accounting Zone stores the audit tolerance applied by the Enterprise Water Balance service.

### Enterprise Water Balance V2

Mission: `KESW-S3-M1`

Status: Complete and verified

The module provides:

- Decimal-based domain calculations
- Boundary inflow and outflow accounting
- Net storage-change accounting
- Signed and absolute balance errors
- Balance error and closure percentages
- Unaccounted and over-accounted water
- Internal reuse and gross-demand KPIs
- Configurable Water Accounting Zone audit tolerance
- BALANCED, IMBALANCED, NO_FLOW, and INDETERMINATE statuses

## Enterprise Water Balance Request Flow

1. The API receives and validates the calculation request.
2. Pydantic schemas validate identifiers, numeric values, and units.
3. The service validates Organization, Plant, and Water Accounting Zone ownership.
4. The service retrieves the Water Accounting Zone audit tolerance.
5. The service creates domain-engine inputs.
6. The engineering core performs the deterministic calculation.
7. The service maps the domain result to the response schema.
8. The API returns the calculation response.

The current calculation is stateless. Calculation persistence and audit history are planned for the next mission.

## Water Balance Boundary Model

Boundary inflow:

- External fresh water
- External reclaimed water
- Inter-zone inflow

Boundary outflow:

- Wastewater discharge
- Inter-zone outflow
- Evaporation
- Product incorporation
- Other consumptive use

Storage equation:

- Net storage change equals closing storage minus opening storage

Balance equation:

- Signed balance error equals boundary inflow minus boundary outflow minus net storage change

Internal reuse:

- Excluded from boundary inflow
- Included in gross water demand
- Used to calculate internal reuse percentage

## Current API Structure

Core APIs:

- `/api/v1/health`
- `/api/v1/organizations/`
- `/api/v1/plants/`
- `/api/v1/water-accounting-zones/`

Current engineering API:

- `POST /api/v1/engineering/water-balance/calculate`

Planned engineering APIs:

- `/api/v1/engineering/pumps/`
- `/api/v1/engineering/pipelines/`
- `/api/v1/engineering/tanks/`
- `/api/v1/engineering/friction-loss/`

## Database

Database engine: PostgreSQL

Database name: `kes_water`

Schema migrations are managed through Alembic.

Current migration sequence:

- Organizations
- Plants
- Water Accounting Zones

Current Alembic head:

- `67f3d7e90039`

Enterprise Water Balance V2 uses the existing Water Accounting Zone data and requires no new database migration.

## Engineering Calculator Modernization

Every retained calculator must pass through the following process:

1. Extract the original formula.
2. Review the engineering physics.
3. Define input and output units.
4. Document assumptions and limitations.
5. Refactor into a domain engine.
6. Add Pydantic validation.
7. Add regression tests.
8. Integrate enterprise ownership.
9. Persist calculation inputs and results.
10. Expose a versioned engineering API.

Water Balance V2 has completed steps 1 through 8 and step 10.

Water Balance calculation persistence and audit history remain pending under step 9.

The remaining retained calculators have not yet completed this modernization process.

## Legacy Compatibility

The following legacy Water Balance files remain unchanged:

- `backend/app/engineering_core/water_balance/calculator.py`
- `backend/app/api/routes/water_balance.py`

The legacy route remains dormant and is not registered as the Enterprise Water Balance V2 endpoint.

Legacy formulas must not be removed until their behavior, dependencies, and migration requirements are verified.

## Automated Validation

Enterprise Water Balance V2 validation includes:

- Domain-engine tests
- Schema tests
- Service tests
- API tests
- Ownership-validation tests
- Audit-tolerance tests
- Invalid-input tests
- Status-classification tests
- Live API validation
- Python compile validation

Current result:

- 65 tests passed
- 224 of 224 statements covered
- 100% targeted coverage

## Cross-Cutting Concerns

- Configuration through Pydantic Settings
- PostgreSQL transaction management
- Structured Loguru logging
- CORS configuration
- Central exception handling
- Environment-secret isolation
- OpenAPI documentation
- Alembic schema versioning
- Decimal-based engineering calculations
- Domain-specific validation errors

## Deployment

The backend runs on port `8010`.

The production Docker container:

- Uses Python 3.12
- Runs as a non-root user
- Exposes port 8010
- Includes a health check
- Does not use Uvicorn reload mode

## Design Principles

- Engineering correctness before feature speed
- Explicit units and assumptions
- Clear separation of responsibilities
- Database-backed traceability
- Versioned APIs and calculations
- Domain engines independent from HTTP and database layers
- No duplicate active repositories
- No direct copying of unverified legacy formulas
