-- BhuStack schema
-- Database: bhustack
-- One parcel → one ULPIN → linked governance datasets
-- All data in this prototype is SYNTHETIC.

CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS parcels (
    id              SERIAL PRIMARY KEY,
    ulpin           VARCHAR(32) NOT NULL UNIQUE,
    survey_number   VARCHAR(32) NOT NULL,
    parcel_number   VARCHAR(32) NOT NULL UNIQUE,
    area            NUMERIC(12, 2) NOT NULL CHECK (area > 0),
    state           VARCHAR(64) NOT NULL DEFAULT 'Demo State',
    district        VARCHAR(64) NOT NULL DEFAULT 'Demo District',
    block           VARCHAR(64),
    village         VARCHAR(64) NOT NULL DEFAULT 'Demo Campus',
    land_type       VARCHAR(64),
    source_type     VARCHAR(32) NOT NULL DEFAULT 'SYNTHETIC'
                    CHECK (source_type IN ('SYNTHETIC', 'GOVERNMENT_API', 'OPEN_DATA')),
    geometry        geometry(Polygon, 4326) NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT parcels_ulpin_format CHECK (ulpin ~ '^IND-DEMO-[0-9]{6}$'),
    CONSTRAINT parcels_geometry_valid CHECK (ST_IsValid(geometry))
);

CREATE INDEX IF NOT EXISTS idx_parcels_ulpin ON parcels (ulpin);
CREATE INDEX IF NOT EXISTS idx_parcels_survey ON parcels (survey_number);
CREATE INDEX IF NOT EXISTS idx_parcels_parcel_number ON parcels (parcel_number);
CREATE INDEX IF NOT EXISTS idx_parcels_village ON parcels (village);
CREATE INDEX IF NOT EXISTS idx_parcels_district ON parcels (district);
CREATE INDEX IF NOT EXISTS idx_parcels_geometry ON parcels USING GIST (geometry);

CREATE TABLE IF NOT EXISTS ownership (
    id              SERIAL PRIMARY KEY,
    ulpin           VARCHAR(32) NOT NULL UNIQUE REFERENCES parcels(ulpin) ON DELETE CASCADE,
    owner_name      VARCHAR(128) NOT NULL,
    status          VARCHAR(32) NOT NULL DEFAULT 'Verified',
    owner_type      VARCHAR(64) NOT NULL DEFAULT 'Institution',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ror (
    id              SERIAL PRIMARY KEY,
    ulpin           VARCHAR(32) NOT NULL UNIQUE REFERENCES parcels(ulpin) ON DELETE CASCADE,
    status          VARCHAR(32) NOT NULL,
    khata_number    VARCHAR(64),
    remarks         TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS registrations (
    id                  SERIAL PRIMARY KEY,
    ulpin               VARCHAR(32) NOT NULL UNIQUE REFERENCES parcels(ulpin) ON DELETE CASCADE,
    status              VARCHAR(32) NOT NULL,
    registration_date   DATE,
    document_number     VARCHAR(64),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS land_use (
    id              SERIAL PRIMARY KEY,
    ulpin           VARCHAR(32) NOT NULL UNIQUE REFERENCES parcels(ulpin) ON DELETE CASCADE,
    land_use        VARCHAR(64) NOT NULL,
    zoning          VARCHAR(64),
    master_plan     VARCHAR(128),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tax (
    id                  SERIAL PRIMARY KEY,
    ulpin               VARCHAR(32) NOT NULL UNIQUE REFERENCES parcels(ulpin) ON DELETE CASCADE,
    status              VARCHAR(32) NOT NULL,
    last_payment_date   DATE,
    amount_due          NUMERIC(12, 2) NOT NULL DEFAULT 0,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS restrictions (
    id              SERIAL PRIMARY KEY,
    ulpin           VARCHAR(32) NOT NULL UNIQUE REFERENCES parcels(ulpin) ON DELETE CASCADE,
    status          VARCHAR(32) NOT NULL,
    type            VARCHAR(64),
    description     TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS disputes (
    id              SERIAL PRIMARY KEY,
    ulpin           VARCHAR(32) NOT NULL UNIQUE REFERENCES parcels(ulpin) ON DELETE CASCADE,
    status          VARCHAR(32) NOT NULL,
    description     TEXT,
    filed_date      DATE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS building_permissions (
    id              SERIAL PRIMARY KEY,
    ulpin           VARCHAR(32) NOT NULL UNIQUE REFERENCES parcels(ulpin) ON DELETE CASCADE,
    status          VARCHAR(32) NOT NULL,
    permit_number   VARCHAR(64),
    issued_date     DATE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS service_requests (
    id              SERIAL PRIMARY KEY,
    request_id      VARCHAR(32) NOT NULL UNIQUE,
    ulpin           VARCHAR(32) NOT NULL REFERENCES parcels(ulpin),
    service_type    VARCHAR(64) NOT NULL,
    status          VARCHAR(32) NOT NULL DEFAULT 'SUBMITTED'
                    CHECK (status IN ('SUBMITTED', 'UNDER_REVIEW', 'APPROVED', 'REJECTED')),
    remarks         TEXT,
    submitted_date  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_updated    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_service_requests_ulpin ON service_requests (ulpin);
CREATE INDEX IF NOT EXISTS idx_service_requests_status ON service_requests (status);

CREATE TABLE IF NOT EXISTS users (
    id              SERIAL PRIMARY KEY,
    username        VARCHAR(64) NOT NULL UNIQUE,
    password_hash   VARCHAR(128) NOT NULL,
    role            VARCHAR(16) NOT NULL CHECK (role IN ('CITIZEN', 'ADMIN')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id              SERIAL PRIMARY KEY,
    audit_id        VARCHAR(32) NOT NULL UNIQUE,
    username        VARCHAR(64),
    action          VARCHAR(64) NOT NULL,
    ulpin           VARCHAR(32),
    description     TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_ulpin ON audit_logs (ulpin);

CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
DECLARE
    t TEXT;
BEGIN
    FOREACH t IN ARRAY ARRAY[
        'parcels', 'ownership', 'ror', 'registrations',
        'land_use', 'tax', 'restrictions', 'disputes', 'building_permissions'
    ]
    LOOP
        EXECUTE format(
            'DROP TRIGGER IF EXISTS trg_%s_updated_at ON %I;
             CREATE TRIGGER trg_%s_updated_at
             BEFORE UPDATE ON %I
             FOR EACH ROW EXECUTE FUNCTION set_updated_at();',
            t, t, t, t
        );
    END LOOP;
END $$;
