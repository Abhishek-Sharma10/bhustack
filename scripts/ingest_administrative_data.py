#!/usr/bin/env python3
"""
Ingest administrative boundaries (States, Districts, Blocks, Villages)
and ensure parcels with complete 8-department records exist in PostgreSQL.
"""
import json
import os
import sys
from pathlib import Path
import psycopg2
from psycopg2.extras import Json

DB_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:password@localhost:5433/bhustack")

def get_conn():
    return psycopg2.connect(DB_URL)

def setup_tables(conn):
    with conn.cursor() as cur:
        # Create administrative_regions table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS administrative_regions (
            id SERIAL PRIMARY KEY,
            name VARCHAR(128) NOT NULL,
            type VARCHAR(32) NOT NULL CHECK (type IN ('state', 'district', 'block', 'village')),
            state VARCHAR(128),
            district VARCHAR(128),
            block VARCHAR(128),
            village VARCHAR(128),
            properties JSONB DEFAULT '{}'::jsonb,
            geometry geometry(Geometry, 4326) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_admin_regions_type_name ON administrative_regions (type, name);
        CREATE INDEX IF NOT EXISTS idx_admin_regions_geom ON administrative_regions USING GIST (geometry);
        """)

        # Add block column to parcels if not exists
        cur.execute("""
        ALTER TABLE parcels ADD COLUMN IF NOT EXISTS block VARCHAR(64);
        """)

        # Relax ULPIN constraint to support standard ULPINs while retaining all existing IND-DEMO-* parcels
        cur.execute("""
        ALTER TABLE parcels DROP CONSTRAINT IF EXISTS parcels_ulpin_format;
        ALTER TABLE parcels ADD CONSTRAINT parcels_ulpin_format CHECK (ulpin ~ '^[A-Za-z0-9\\-]{4,32}$');
        """)

        # Update existing demo parcels with a default block if null
        cur.execute("""
        UPDATE parcels SET block = 'Demo Central Block' WHERE block IS NULL;
        """)

    conn.commit()
    print("Database tables and columns verified.")

def ingest_states(conn):
    states_path = Path("database/sample_data/indian_states.geojson")
    if not states_path.exists():
        print(f"File {states_path} not found.")
        return

    with open(states_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    with conn.cursor() as cur:
        for feature in data.get("features", []):
            name = feature["properties"].get("NAME_1")
            if not name:
                continue

            geom = feature["geometry"]
            geom_json = json.dumps(geom)

            # Metadata properties
            props = {
                "name": name,
                "type": "state",
                "state": name,
                "districts_count": 38 if name.lower() == "bihar" else (75 if name.lower() == "uttar pradesh" else 25),
                "blocks_count": 534 if name.lower() == "bihar" else 350,
                "villages_count": 45103 if name.lower() == "bihar" else 30000,
                "parcels_count": 14 if name.lower() == "bihar" else 30,
            }

            cur.execute("""
            INSERT INTO administrative_regions (name, type, state, properties, geometry)
            SELECT %s, 'state', %s, %s, ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326)
            WHERE NOT EXISTS (
                SELECT 1 FROM administrative_regions WHERE type = 'state' AND LOWER(name) = LOWER(%s)
            );
            """, (name, name, Json(props), geom_json, name))

    conn.commit()
    print("Ingested Indian states into administrative_regions.")

def ingest_bihar_admin(conn):
    admin_path = Path("database/sample_data/bihar_admin.json")
    if not admin_path.exists():
        print(f"File {admin_path} not found.")
        return

    with open(admin_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    with conn.cursor() as cur:
        # 1. District: Patna
        patna = data.get("district_patna")
        if patna:
            geom_json = json.dumps(patna["geometry"])
            props = {
                "name": "Patna",
                "type": "district",
                "state": "Bihar",
                "district": "Patna",
                "blocks_count": 23,
                "villages_count": 1384,
                "parcels_count": 6,
                "headquarters": "Patna"
            }
            cur.execute("""
            INSERT INTO administrative_regions (name, type, state, district, properties, geometry)
            SELECT 'Patna', 'district', 'Bihar', 'Patna', %s, ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326)
            WHERE NOT EXISTS (
                SELECT 1 FROM administrative_regions WHERE type = 'district' AND LOWER(name) = 'patna'
            );
            """, (Json(props), geom_json))
            print("Ingested Patna District boundary.")

        # 2. Block: Bihta
        bihta = data.get("block_bihta")
        if bihta:
            geom_json = json.dumps(bihta["geometry"])
            props = {
                "name": "Bihta",
                "type": "block",
                "state": "Bihar",
                "district": "Patna",
                "block": "Bihta",
                "panchayats_count": 25,
                "villages_count": 82,
                "parcels_count": 4,
                "tehsil": "Bihta"
            }
            cur.execute("""
            INSERT INTO administrative_regions (name, type, state, district, block, properties, geometry)
            SELECT 'Bihta', 'block', 'Bihar', 'Patna', 'Bihta', %s, ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326)
            WHERE NOT EXISTS (
                SELECT 1 FROM administrative_regions WHERE type = 'block' AND LOWER(name) = 'bihta'
            );
            """, (Json(props), geom_json))
            print("Ingested Bihta Block boundary.")

        # 3. Village: Amhara
        amhara = data.get("village_amhara")
        if amhara:
            geom_json = json.dumps(amhara["geometry"])
            props = {
                "name": "Amhara",
                "type": "village",
                "state": "Bihar",
                "district": "Patna",
                "block": "Bihta",
                "village": "Amhara",
                "pincode": "801103",
                "parcels_count": 2
            }
            cur.execute("""
            INSERT INTO administrative_regions (name, type, state, district, block, village, properties, geometry)
            SELECT 'Amhara', 'village', 'Bihar', 'Patna', 'Bihta', 'Amhara', %s, ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326)
            WHERE NOT EXISTS (
                SELECT 1 FROM administrative_regions WHERE type = 'village' AND LOWER(name) = 'amhara'
            );
            """, (Json(props), geom_json))
            print("Ingested Amhara Village boundary.")

        # 4. District: Varanasi
        varanasi = data.get("district_varanasi")
        if varanasi:
            geom_json = json.dumps(varanasi["geometry"])
            props = {
                "name": "Varanasi",
                "type": "district",
                "state": "Uttar Pradesh",
                "district": "Varanasi",
                "blocks_count": 8,
                "villages_count": 1328,
                "parcels_count": 30,
                "headquarters": "Varanasi"
            }
            cur.execute("""
            INSERT INTO administrative_regions (name, type, state, district, properties, geometry)
            SELECT 'Varanasi', 'district', 'Uttar Pradesh', 'Varanasi', %s, ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326)
            WHERE NOT EXISTS (
                SELECT 1 FROM administrative_regions WHERE type = 'district' AND LOWER(name) = 'varanasi'
            );
            """, (Json(props), geom_json))
            print("Ingested Varanasi District boundary.")

    conn.commit()

def ingest_sample_parcels(conn):
    """
    Inserts sample parcels with full 8-department records so both
    the drill-down hierarchy (Bihar -> Patna -> Bihta -> Amhara -> 1234-5678-9012)
    and the Varanasi/Assi parcel (9876-5432-1098) are directly in PostgreSQL.
    """
    sample_parcels = [
        {
            "ulpin": "1234-5678-9012",
            "survey_number": "142/2",
            "parcel_number": "P-BIHTA-001",
            "area": 1250.00,
            "state": "Bihar",
            "district": "Patna",
            "block": "Bihta",
            "village": "Amhara",
            "land_type": "Plotted Residential",
            "source_type": "SYNTHETIC",
            # Polygon inside Amhara, Bihta, Patna, Bihar (approx 84.86° E, 25.56° N)
            "wkt": "POLYGON((84.86250 25.56100, 84.86380 25.56100, 84.86380 25.56220, 84.86250 25.56220, 84.86250 25.56100))",
            "ownership": ("Ramesh Kumar", "Verified", "Individual"),
            "ror": ("Issued", "89", "Certified by Tehsildar Bihta; Khasra 142/2"),
            "registration": ("Registered", "2023-08-12", "DOC/2023/4592"),
            "land_use": ("Residential", "R-2 Medium Density", "Patna Master Plan 2031"),
            "tax": ("Paid", "2026-01-15", 0.00),
            "restriction": ("Restricted", "Road Setback", "No permanent construction within 5m of main road buffer"),
            "dispute": ("Mortgaged", "Bank Mortgage Active (State Bank of India, Bihta SME Branch ₹45,00,000)", None),
            "building_permission": ("Approved", "BP/2024/0981", "2024-05-05")
        },
        {
            "ulpin": "9876-5432-1098",
            "survey_number": "182/4",
            "parcel_number": "P-VNS-002",
            "area": 3480.00,
            "state": "Uttar Pradesh",
            "district": "Varanasi",
            "block": "Kashi Vidyapeeth",
            "village": "Assi Ghat",
            "land_type": "Mixed Heritage Commercial",
            "source_type": "SYNTHETIC",
            "wkt": "POLYGON((82.99910 25.28140, 82.99990 25.28140, 82.99980 25.28220, 82.99910 25.28220, 82.99910 25.28140))",
            "ownership": ("Sunita Devi & Anil Sharma", "Verified", "Joint Private"),
            "ror": ("Issued", "34", "Abadi Deh Khata 34"),
            "registration": ("Registered", "2021-02-04", "DOC/2021/1088"),
            "land_use": ("Commercial", "Mixed Heritage Zone", "Varanasi Master Plan 2031"),
            "tax": ("Paid", "2026-01-20", 0.00),
            "restriction": ("Restricted", "River Ganga Buffer", "Ganga 200m Eco-Sensitive Regulated Buffer Zone"),
            "dispute": ("None", "Clear Freehold Title; zero court disputes", None),
            "building_permission": ("Approved", "VDA/BP/2022/411", "2022-06-18")
        }
    ]

    with conn.cursor() as cur:
        for p in sample_parcels:
            cur.execute("""
            INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, block, village, land_type, source_type, geometry)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326))
            ON CONFLICT (ulpin) DO UPDATE SET
                survey_number = EXCLUDED.survey_number,
                area = EXCLUDED.area,
                state = EXCLUDED.state,
                district = EXCLUDED.district,
                block = EXCLUDED.block,
                village = EXCLUDED.village,
                land_type = EXCLUDED.land_type,
                geometry = EXCLUDED.geometry;
            """, (p["ulpin"], p["survey_number"], p["parcel_number"], p["area"],
                  p["state"], p["district"], p["block"], p["village"],
                  p["land_type"], p["source_type"], p["wkt"]))

            # Ownership
            cur.execute("""
            INSERT INTO ownership (ulpin, owner_name, status, owner_type)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (ulpin) DO UPDATE SET owner_name = EXCLUDED.owner_name, status = EXCLUDED.status;
            """, (p["ulpin"], p["ownership"][0], p["ownership"][1], p["ownership"][2]))

            # RoR
            cur.execute("""
            INSERT INTO ror (ulpin, status, khata_number, remarks)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (ulpin) DO UPDATE SET status = EXCLUDED.status, khata_number = EXCLUDED.khata_number, remarks = EXCLUDED.remarks;
            """, (p["ulpin"], p["ror"][0], p["ror"][1], p["ror"][2]))

            # Registration
            cur.execute("""
            INSERT INTO registrations (ulpin, status, registration_date, document_number)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (ulpin) DO UPDATE SET status = EXCLUDED.status, registration_date = EXCLUDED.registration_date, document_number = EXCLUDED.document_number;
            """, (p["ulpin"], p["registration"][0], p["registration"][1], p["registration"][2]))

            # Land Use
            cur.execute("""
            INSERT INTO land_use (ulpin, land_use, zoning, master_plan)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (ulpin) DO UPDATE SET land_use = EXCLUDED.land_use, zoning = EXCLUDED.zoning, master_plan = EXCLUDED.master_plan;
            """, (p["ulpin"], p["land_use"][0], p["land_use"][1], p["land_use"][2]))

            # Tax
            cur.execute("""
            INSERT INTO tax (ulpin, status, last_payment_date, amount_due)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (ulpin) DO UPDATE SET status = EXCLUDED.status, last_payment_date = EXCLUDED.last_payment_date, amount_due = EXCLUDED.amount_due;
            """, (p["ulpin"], p["tax"][0], p["tax"][1], p["tax"][2]))

            # Restrictions
            cur.execute("""
            INSERT INTO restrictions (ulpin, status, type, description)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (ulpin) DO UPDATE SET status = EXCLUDED.status, type = EXCLUDED.type, description = EXCLUDED.description;
            """, (p["ulpin"], p["restriction"][0], p["restriction"][1], p["restriction"][2]))

            # Disputes
            cur.execute("""
            INSERT INTO disputes (ulpin, status, description, filed_date)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (ulpin) DO UPDATE SET status = EXCLUDED.status, description = EXCLUDED.description;
            """, (p["ulpin"], p["dispute"][0], p["dispute"][1], p["dispute"][2]))

            # Building Permissions
            cur.execute("""
            INSERT INTO building_permissions (ulpin, status, permit_number, issued_date)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (ulpin) DO UPDATE SET status = EXCLUDED.status, permit_number = EXCLUDED.permit_number, issued_date = EXCLUDED.issued_date;
            """, (p["ulpin"], p["building_permission"][0], p["building_permission"][1], p["building_permission"][2]))

    conn.commit()
    print("Ingested sample parcels with 8-department data.")

def main():
    conn = get_conn()
    try:
        setup_tables(conn)
        ingest_states(conn)
        ingest_bihar_admin(conn)
        ingest_sample_parcels(conn)
        print("Administrative and parcel ingestion complete!")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
