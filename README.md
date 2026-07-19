# KES_Water

Enterprise Water Engineering, Accounting, and Intelligence Platform by Kamra Engineering Solutions.

## Product Vision

KES_Water is the single canonical SaaS platform for industrial water engineering, water accounting, hydraulic calculations, treatment systems, compliance, and future AI-driven water intelligence.

The platform consolidates the engineering calculator history of Kamra Water OS with the enterprise architecture of KES_Water.

## Canonical Repository

https://github.com/kamracp/KES_Water.git

Only this repository is actively maintained for the KES water platform.

## Current Status

Completed foundation:

- FastAPI
- PostgreSQL
- SQLAlchemy 2.x
- Alembic
- Pydantic v2
- Loguru
- CORS
- Versioned API under `/api/v1`
- Swagger and OpenAPI
- Repository pattern
- Service layer

Completed enterprise modules:

- Organization CRUD
- Plant CRUD
- Water Accounting Zone CRUD
- Enterprise Water Balance V2

Current Water Balance validation:

- 65 automated tests passed
- 224 of 224 statements covered
- 100% targeted coverage
- Python compile validation passed
- Live API calculation passed

## Retained Enterprise Data

- Organization ID: 2
- Organization Code: KES
- Organization Name: Kamra Engineering Solutions
- Plant ID: 1
- Plant Code: MOH-01
- Plant Name: KES Mohali Water Engineering Plant
- Water Accounting Zone ID: 1
- Zone Code: MOH-WAZ-01
- Zone Name: KES Mohali Main Water Accounting Zone
- Zone Audit Tolerance: 5%

## Water Accounting Zone

The Water Accounting Zone module supports:

- Water audit boundaries
- Inflow and outflow accounting
- Water mass balance
- Consumption and loss assessment
- Baseline consumption
- Metering coverage
- Audit tolerance
- Hierarchical plant water zones
- Future ISO 46001-aligned workflows

Current Alembic migration head: `67f3d7e90039`

## Enterprise Water Balance V2

Mission `KESW-S3-M1` delivered a Decimal-based enterprise Water Balance engine.

Registered endpoint:

- `POST /api/v1/engineering/water-balance/calculate`

Boundary inflow includes:

- External fresh water
- External reclaimed water
- Inter-zone inflow

Boundary outflow includes:

- Wastewater discharge
- Inter-zone outflow
- Evaporation
- Product incorporation
- Other consumptive use

Net storage change is calculated as closing storage minus opening storage.

Signed balance error is calculated as boundary inflow minus boundary outflow minus net storage change.

Internal reuse is excluded from boundary inflow and is used for gross demand and circularity KPIs.

Supported statuses:

- BALANCED
- IMBALANCED
- NO_FLOW
- INDETERMINATE

The service validates Organization, Plant, and Water Accounting Zone ownership and applies the configured Water Accounting Zone audit tolerance.

## Engineering Calculators

Modernized enterprise calculator:

- Water Balance V2

Preserved legacy calculators:

- Water Balance
- Pump Selection
- Pipeline Sizing
- Tank Design
- Pump Head
- Friction Loss

The legacy Water Balance calculator and dormant legacy route remain unchanged for traceability.

The remaining calculators will be reviewed, validated, unit-tested, refactored into domain engines, integrated with Organization, Plant, and Water Accounting Zone, and exposed under `/api/v1/engineering/`.

## Technology Stack

Backend:

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy 2.x
- Alembic
- Pydantic v2
- Loguru
- Uvicorn

Development testing:

- pytest
- pytest-cov

Planned frontend:

- React 19
- TypeScript
- Vite
- Tailwind CSS
- React Router
- React Query
- Axios
- React Hook Form

## Local Development

Project root: `/home/chander/projects/KES_Water`

Backend directory:

`/home/chander/projects/KES_Water/backend`

Start the backend:

`../.venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8010`

API documentation:

http://127.0.0.1:8010/docs

Install development dependencies from the backend directory:

`../.venv/bin/pip install -r requirements-dev.txt`

Run the Enterprise Water Balance test suite:

`../.venv/bin/python -m pytest tests/engineering_core/water_balance/test_engine.py tests/schemas/test_water_balance.py tests/services/test_water_balance_service.py tests/api/test_engineering_water_balance.py -q`

## Core API Modules

- `/api/v1/health`
- `/api/v1/organizations/`
- `/api/v1/plants/`
- `/api/v1/water-accounting-zones/`
- `POST /api/v1/engineering/water-balance/calculate`

## Security

- Local `.env` files must not be committed.
- Virtual environments, logs, caches, and compiled files are excluded from Git.
- `.env.example` must contain placeholders only.
- Production credentials must never be committed.

## Development Principle

Every engineering module must be technically reviewable, unit-aware, assumption-aware, testable, and traceable to its calculation inputs and results.