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

## Backend Layers

### API Layer

Location: `backend/app/api/`

Responsibilities:

- Define FastAPI routes
- Validate request parameters
- Inject database sessions
- Select response schemas
- Return HTTP status codes

### Service Layer

Location: `backend/app/services/`

Responsibilities:

- Apply business rules
- Validate entity ownership
- Detect duplicate records
- Coordinate repositories
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
- Remain independent from HTTP routing
- Support regression testing

## Enterprise Data Hierarchy

- Organization
  - Plant
    - Water Accounting Zone
      - Future meters and measurement points
      - Future water streams
      - Future calculation projects
      - Future audit and balance results

## Current Modules

### Organization

Represents the enterprise or customer account.

### Plant

Represents an industrial facility or operational site belonging to an organization.

### Water Accounting Zone

Represents a water-audit, operational, or hydraulic boundary within a plant.

## Current API Structure

- `/api/v1/health`
- `/api/v1/organizations/`
- `/api/v1/plants/`
- `/api/v1/water-accounting-zones/`

Future engineering APIs will use:

- `/api/v1/engineering/water-balance/`
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

## Cross-Cutting Concerns

- Configuration through Pydantic Settings
- PostgreSQL transaction management
- Structured Loguru logging
- CORS configuration
- Central exception handling
- Environment-secret isolation
- OpenAPI documentation
- Alembic schema versioning

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
- No duplicate active repositories
- No direct copying of unverified legacy formulas