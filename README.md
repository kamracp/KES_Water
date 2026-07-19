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

## Retained Engineering Calculators

The following legacy calculators are preserved:

- Water Balance
- Pump Selection
- Pipeline Sizing
- Tank Design
- Pump Head
- Friction Loss

Each calculator will be reviewed, validated, unit-tested, refactored into a domain engine, integrated with Organization, Plant, and Water Accounting Zone, and exposed under `/api/v1/engineering/`.

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

Start the backend:

`cd /home/chander/projects/KES_Water/backend`

`../.venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8010`

API documentation:

http://127.0.0.1:8010/docs

## Core API Modules

- `/api/v1/health`
- `/api/v1/organizations/`
- `/api/v1/plants/`
- `/api/v1/water-accounting-zones/`

## Security

- Local `.env` files must not be committed.
- Virtual environments, logs, caches, and compiled files are excluded from Git.
- `.env.example` must contain placeholders only.
- Production credentials must never be committed.

## Development Principle

Every engineering module must be technically reviewable, unit-aware, assumption-aware, testable, and traceable to its calculation inputs and results.