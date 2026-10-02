# BhuStack

**One Parcel. One Identity. Complete Land Intelligence.**

BhuStack is a hackathon MVP that demonstrates a parcel-centric workflow: GIS parcel → ULPIN → FastAPI → PostGIS → Unified Parcel Profile.

> **Synthetic-data notice:** Every parcel, owner, record, tax, dispute, registration, and permission is synthetic demonstration data. The BHU map context is an approximate showcase only; BhuStack is not connected to government or BHU land-record systems.

## Prerequisites

- Python **3.12 preferred** (the bootstrap discovers a stable compatible interpreter and does not select prerelease Python)
- Node.js **18+** (npm included)
- Docker Desktop (Windows) or Docker Engine (Linux), with Docker Compose

PostgreSQL, PostGIS, `psql`, and `pg_config` are not required on the host. PostGIS runs in Docker.

## Quick start: Linux and Windows

Linux:

```bash
git clone <repository-url>
cd bhustack
python3 scripts/init.py
python3 scripts/start.py
```

Windows:

```powershell
git clone <repository-url>
cd bhustack
python scripts/init.py
python scripts/start.py
```

Initialization discovers Python 3.12 when available, creates `backend/.venv`, installs dependencies, starts PostGIS, applies the schema, loads the canonical seed only into an empty database, runs administrative ingestion, verifies the complete dataset, runs API smoke testing, and builds the frontend.

Open `http://localhost:5173`. API docs: `http://localhost:8000/docs`; health: `http://localhost:8000/api/v1/health`.

## Project commands

```bash
python scripts/bhustack.py doctor
python scripts/bhustack.py init
python scripts/bhustack.py start
python scripts/bhustack.py status
python scripts/bhustack.py test
python scripts/bhustack.py stop
python scripts/bhustack.py db-init
python scripts/bhustack.py db-reset --yes
```

Thin wrappers delegate to the same CLI: `./start.sh` / `./stop.sh` on Linux, and `start.bat` / `stop.bat` or `start.ps1` / `stop.ps1` on Windows. The scripts do not require a manually activated Python virtual environment.

### Fresh-machine setup

```bash
cd bhustack
python3 scripts/bhustack.py doctor
python3 scripts/bhustack.py init
./start.sh
```

On Windows PowerShell:

```powershell
cd bhustack
python .\scripts\bhustack.py doctor
python .\scripts\bhustack.py init
.\start.ps1
```

On Windows CMD:

```cmd
cd bhustack
python scripts\bhustack.py doctor
python scripts\bhustack.py init
start.bat
```

`db-reset --yes` is the only bootstrap reset command. It is destructive: it removes the Docker PostGIS volume and recreates the synthetic database. Normal `init`, `start`, and `db-init` preserve existing data and complete missing administrative initialization.

## Dataset and persistence

The intended application dataset contains **32 parcels**:

- 30 canonical `IND-DEMO-000001` through `IND-DEMO-000030` records from `database/seed.sql`.
- 2 administrative hierarchy demo records, `1234-5678-9012` and `9876-5432-1098`, from `scripts/ingest_administrative_data.py`.

The ingestion script also owns `administrative_regions` and the eight department records for those two parcels. It is idempotent and is run after schema and seed initialization. Docker volume data persists across `stop` and normal initialization; `db-reset --yes` is required to remove it.

Local development and the one-command bootstrap use the PostGIS container at `localhost:5433`. An externally managed PostgreSQL/PostGIS database can be used by changing `DATABASE_URL` in `backend/.env` for application runs, but the Docker-backed bootstrap verification and administrative ingestion flow are intended for the local container.

Clean database reset:

```bash
python3 scripts/bhustack.py db-reset --yes
```

## Architecture and workflow

```text
React + Leaflet → FastAPI (/api/v1) → PostgreSQL + PostGIS
                         ↑
       Synthetic Government API → DemoStateAdapter
```

The frontend never connects directly to PostgreSQL. The existing Satellite View queries FastAPI, which reads parcel and administrative geometry from PostgreSQL/PostGIS.

## Structure

```text
backend/       FastAPI app, requirements, smoke test
frontend/      React/Vite UI and package lockfile
database/      authoritative schema.sql, seed.sql, queries.sql, sample GeoJSON
scripts/       cross-platform init/start/stop/status/test CLI
docs/          user, architecture, API, database, and demo references
postman/       importable API collection
```

## Troubleshooting

- Docker daemon unavailable: start Docker Desktop/Engine and retry.
- Node.js missing: install Node 18+ and rerun `python scripts/init.py`.
- Dependency download failure: check internet/DNS; initialization identifies npm/PyPI failures.
- Port conflict: use `python scripts/stop.py` for BhuStack; resolve unrelated port users separately.

See [docs/architecture.md](docs/architecture.md), [docs/api.md](docs/api.md), [docs/database.md](docs/database.md), and [docs/demo-script.md](docs/demo-script.md).
