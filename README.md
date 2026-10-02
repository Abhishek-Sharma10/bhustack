# BhuStack

## Integrated GIS-based Digital Public Infrastructure for Land Governance

BhuStack is a GIS-based land governance platform designed to provide a unified digital interface for accessing, visualizing, and managing land-related information.

The platform combines GIS parcel visualization, land records, ownership information, registration details, administrative boundaries, service requests, and interoperability capabilities into a single application.

---

## Project Overview

Land-related information is often distributed across different records, departments, and systems. BhuStack provides a unified interface where a user can search for a land parcel using its ULPIN and access the associated information through a single platform.

The system provides:

- GIS-based parcel visualization
- ULPIN-based parcel search
- Parcel profile and land information
- Ownership and RoR information
- Registration information
- Land-use information
- Tax and restriction information
- Dispute information
- Building permission information
- Service request management
- Administrative boundary visualization
- GIS explorer
- Interoperability demonstration
- Application tracking
- Administrative dashboard

The current project uses synthetic/demo data for demonstration purposes.

---

## Main Features

### 1. GIS Parcel Explorer

The GIS Explorer provides an interactive map for visualizing land parcels and administrative boundaries.

Features include:

- Satellite map visualization
- Parcel boundaries
- Parcel selection
- ULPIN search
- Parcel highlighting
- Parcel information panel
- Administrative boundary layers
- State-level mapping
- Map controls and layer management

Parcel geometry is handled through the project's GIS/PostGIS architecture.

---

### 2. Unified Parcel Profile

A parcel can be identified using its ULPIN.

The parcel profile provides information such as:

- ULPIN
- Parcel location
- Ownership
- Record of Rights
- Land use
- Registration
- Tax information
- Restrictions
- Disputes
- Building permissions

---

### 3. Service Requests

BhuStack provides a service-request interface for land-related citizen services.

The application supports the demonstration of submitting and tracking requests related to land records and associated services.

---

### 4. Application Tracking

Users can track the status of submitted applications and service requests.

The project includes status handling for the application workflow.

---

### 5. Administrative Dashboard

The administrative dashboard provides an interface for viewing and managing application/service information.

---

### 6. Interoperability Demo

The Interoperability Demo demonstrates how land-related information can be exposed and consumed through a unified platform.

The backend API acts as the integration layer between the frontend GIS application and the underlying land database.

---

## Technology Stack

### Frontend

- React
- Vite
- JavaScript
- Tailwind CSS
- Leaflet
- GeoJSON

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn
- psycopg2

### Database

- PostgreSQL
- PostGIS

### Infrastructure

- Docker
- Docker Compose

### Development / Testing

- Git
- GitHub
- Postman

---

## System Architecture

```text
                    BhuStack Frontend
                           |
                           |
                    React + Vite
                           |
                           |
                    REST API / JSON
                           |
                           v
                    FastAPI Backend
                           |
             +-------------+-------------+
             |                           |
             v                           v
       Parcel Services             Request Services
             |                           |
             +-------------+-------------+
                           |
                           v
                    PostgreSQL
                           |
                         PostGIS
                           |
             +-------------+-------------+
             |                           |
             v                           v
       Parcel Geometry          Administrative Data

```
## Project Structure

---
bhustack/
│
├── backend/
│   ├── app/
│   │   ├── adapters/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── utils/
│   │
│   ├── tests/
│   ├── .env.example
│   └── requirements.txt
│
├── database/
│   ├── sample_data/
│   │   ├── bihar_admin.json
│   │   ├── campus_parcels.geojson
│   │   └── indian_states.geojson
│   │
│   ├── generate_seed.py
│   ├── queries.sql
│   ├── schema.sql
│   └── seed.sql
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── map/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── types/
│   │   └── utils/
│   │
│   ├── .env.example
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── postman/
│   └── BhuStack.postman_collection.json
│
├── scripts/
│   ├── bhustack.py
│   ├── ingest_administrative_data.py
│   ├── init.py
│   ├── start.py
│   └── stop.py
│
├── docker-compose.yml
├── index.html
├── satellite_parcel_view.html
│
├── start.sh
├── start.ps1
├── start.bat
│
├── stop.sh
├── stop.ps1
├── stop.bat
│
├── .gitignore
└── README.md

---

## Database
BhuStack uses PostgreSQL with the PostGIS extension for spatial data.

The main database definition is maintained in:
---
database/schema.sql
---

Demo data is maintained in:
---
database/seed.sql
---

Additional sample GIS/administrative data is available under:
---
database/sample_data/
---

Current sample data includes:

Synthetic campus parcel data
Indian state boundary data
Bihar administrative data

The database is intended for demonstration and development purposes.

## Demo Data

The project contains synthetic parcel records using ULPIN-style identifiers such as:
---
IND-DEMO-000001
IND-DEMO-000002
IND-DEMO-000003
...
IND-DEMO-000030
---

Additional administrative/demo records are also present in the current database.

The data should be treated as synthetic demonstration data and not as official government land records.

## Environment Configuration

Environment-specific configuration should be stored in .env files.

Do not commit actual .env files to GitHub.

Example configuration files are provided as:
---
backend/.env.example
frontend/.env.example
---

Create the appropriate .env file locally based on these examples.

## Prerequisites

The project requires:

Git
Python 3.x
Node.js and npm
Docker Desktop / Docker Engine
Docker Compose

PostgreSQL/PostGIS is provided through Docker.

## Quick Start
### Linux

From the project root:
---
./start.sh
---

The startup system is designed to handle the required local services and project startup.

To stop the project:
---
./stop.sh
---

### Windows

Use:
---
start.bat
---

To stop:
---
stop.bat
---

PowerShell scripts are also available:
---
.\start.ps1
---

and:
---
.\stop.ps1
---

If PowerShell execution policy prevents running the script, the batch file can be used instead.

## Manual Development Setup
### Backend

Create a virtual environment:

---
cd backend
python -m venv .venv
---

Activate it on Linux:
---
source .venv/bin/activate
---

Windows:
---
.venv\Scripts\Activate.ps1
---

Install dependencies:
---
pip install -r requirements.txt
---

### Frontend

From the frontend directory:
---
cd frontend
npm install
---

Run the development server:
---
npm run dev
---

### Database

Start PostGIS using Docker Compose:
---
docker compose up -d postgis
---

The project uses PostgreSQL/PostGIS for the spatial database.

Database schema and demo data are provided in:
---
database/schema.sql
database/seed.sql
---

### API

The backend is implemented using FastAPI.

The backend provides APIs for:

 - Health checks
 - Parcel retrieval
 - Parcel information
 - Service requests
 - Application tracking
 - GIS/GeoJSON data
 - Administrative information

The exact API implementation is available under:
---
backend/app/api/
backend/app/services/
---

When the backend is running, FastAPI's interactive documentation can be accessed through its standard /docs endpoint.

### Postman

A Postman collection is included for API testing:
---
postman/BhuStack.postman_collection.json
---

Import this collection into Postman after starting the backend.

### GIS Data

The project uses GeoJSON and PostGIS for spatial information.

Current sample GIS data includes:
---
database/sample_data/campus_parcels.geojson
database/sample_data/indian_states.geojson
database/sample_data/bihar_admin.json
---

Administrative data can be processed through:
---
scripts/ingest_administrative_data.py
---

## Cross-Platform Support

The project contains startup and shutdown scripts for Linux and Windows.

 - Linux
---
start.sh
stop.sh
---

 - Windows Batch
---
start.bat
stop.bat
---

 - Windows PowerShell
---
start.ps1
stop.ps1
---

The Python-based project CLI is located at:
---
scripts/bhustack.py
---

Supporting commands are provided through:
---
scripts/init.py
scripts/start.py
scripts/stop.py
---

## Docker

The PostgreSQL/PostGIS service is defined in:
---
docker-compose.yml
---

Start the database:
---
docker compose up -d postgis
---

Check running containers:
---
docker ps
---

Stop the database:
---
docker compose stop postgis
---

The Docker database volume is local to the machine and is not stored in GitHub.

## Important Repository Rules

The following local/generated files must not be committed:
---
.env
.venv/
node_modules/
dist/
logs/
.run/
__pycache__/
---

These are already covered by .gitignore.

The following project sources should remain version controlled:
---
database/schema.sql
database/seed.sql
database/sample_data/
backend/
frontend/src/
frontend/package.json
frontend/package-lock.json
scripts/
docker-compose.yml
---

## Project Status
Current implementation includes:
---
React/Vite frontend
FastAPI backend
PostgreSQL/PostGIS database
Synthetic land parcel data
GIS parcel visualization
Administrative GIS data
ULPIN-based parcel search
Parcel profile
Service requests
Application tracking
Administrative dashboard
Interoperability demonstration
Docker-based database
Cross-platform startup scripts
---

The project is intended as a prototype/demo implementation of an integrated digital land-governance platform.

## Data Disclaimer

BhuStack's current parcel and land-record data is synthetic/demo data created for development, testing, and hackathon demonstration.

It should not be treated as official land ownership, registration, cadastral, tax, or government data.
