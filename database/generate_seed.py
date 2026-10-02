#!/usr/bin/env python3
"""Generate synthetic campus parcel seed.sql and sample GeoJSON. Fictional data only."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

WEST, SOUTH, EAST, NORTH = 77.5800, 12.9900, 77.5880, 12.9960
COLS, ROWS = 6, 5
TOTAL = COLS * ROWS

OWNERS = [
    "Demo University",
    "Demo University Trust",
    "Demo Campus Housing Board",
    "Demo State Public Works",
    "Demo University Sports Board",
]

PARCEL_META = [
    ("Academic Block A", "Institutional", "Academic Zone"),
    ("Academic Block B", "Institutional", "Academic Zone"),
    ("Academic Block C", "Institutional", "Academic Zone"),
    ("Lecture Hall Complex", "Institutional", "Academic Zone"),
    ("Central Library", "Institutional", "Academic Zone"),
    ("Computer Science Lab", "Institutional", "Academic Zone"),
    ("Electronics Lab", "Institutional", "Academic Zone"),
    ("Workshop Shed", "Institutional", "Utility Zone"),
    ("Hostel A", "Institutional", "Residential Zone"),
    ("Hostel B", "Institutional", "Residential Zone"),
    ("Hostel C", "Institutional", "Residential Zone"),
    ("Dining Hall", "Institutional", "Residential Zone"),
    ("Sports Complex", "Recreational", "Recreation Zone"),
    ("Playground", "Recreational", "Recreation Zone"),
    ("Admin Block", "Institutional", "Administrative Zone"),
    ("Staff Quarters 1", "Residential", "Residential Zone"),
    ("Staff Quarters 2", "Residential", "Residential Zone"),
    ("Guest House", "Residential", "Residential Zone"),
    ("Auditorium", "Institutional", "Academic Zone"),
    ("Innovation Centre", "Institutional", "Academic Zone"),
    ("Utility Substation", "Utility", "Utility Zone"),
    ("Green Belt East", "Environmental", "Green Zone"),
    ("Parking Lot North", "Utility", "Utility Zone"),
    ("Open Amphitheatre", "Recreational", "Recreation Zone"),
    ("Health Centre", "Institutional", "Institutional Zone"),
    ("Campus Canteen", "Commercial", "Mixed Use Zone"),
    ("Book Store", "Commercial", "Mixed Use Zone"),
    ("Maintenance Yard", "Utility", "Utility Zone"),
    ("Water Tank Parcel", "Utility", "Utility Zone"),
    ("Vacant Plot West", "Vacant", "Future Expansion"),
]


def hash_password(password: str) -> str:
    return hashlib.sha256(f"bhustack-demo:{password}".encode()).hexdigest()


def cell_ring(index: int) -> list[tuple[float, float]]:
    row, col = divmod(index, COLS)
    cw = (EAST - WEST) / COLS
    ch = (NORTH - SOUTH) / ROWS
    w = WEST + col * cw
    s = SOUTH + row * ch
    e = w + cw
    n = s + ch
    pad_w, pad_h = cw * 0.04, ch * 0.04
    w, s, e, n = w + pad_w, s + pad_h, e - pad_w, n - pad_h
    return [(w, s), (e, s), (e, n), (w, n), (w, s)]


def wkt(ring: list[tuple[float, float]]) -> str:
    return "POLYGON((" + ", ".join(f"{lon:.8f} {lat:.8f}" for lon, lat in ring) + "))"


def sql_str(value) -> str:
    if value is None:
        return "NULL"
    return "'" + str(value).replace("'", "''") + "'"


def main() -> None:
    root = Path(__file__).resolve().parent
    sample = root / "sample_data"
    sample.mkdir(exist_ok=True)

    parcels_sql = []
    child_sql = {k: [] for k in [
        "ownership", "ror", "registrations", "land_use", "tax",
        "restrictions", "disputes", "building_permissions",
    ]}
    features = []

    disputed = {7, 16}
    restricted = {21, 28}
    pending_own = {29}
    overdue_tax = {11, 25}
    mortgaged = {17}
    pending_reg = {29}
    pending_bp = {8, 29}

    for i in range(TOTAL):
        n = i + 1
        ulpin = f"IND-DEMO-{n:06d}"
        survey = f"{200 + (i // 3)}/{(i % 3) + 1}"
        parcel_number = f"P-{n:03d}"
        name, land_use, zoning = PARCEL_META[i]
        area = round(900 + (i * 37) % 800 + (i % 5) * 20, 2)
        ring = cell_ring(i)
        geom = wkt(ring)

        parcels_sql.append(
            "INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) "
            f"VALUES ({sql_str(ulpin)}, {sql_str(survey)}, {sql_str(parcel_number)}, {area}, "
            f"'Demo State', 'Demo District', 'Demo Campus', {sql_str(name)}, 'SYNTHETIC', "
            f"ST_GeomFromText({sql_str(geom)}, 4326));"
        )

        owner = OWNERS[i % len(OWNERS)]
        own_status = "Pending" if i in pending_own else "Verified"
        child_sql["ownership"].append(
            f"INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES "
            f"({sql_str(ulpin)}, {sql_str(owner)}, {sql_str(own_status)}, 'Institution');"
        )

        ror_status = "Issued" if own_status == "Verified" else "Pending"
        child_sql["ror"].append(
            f"INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES "
            f"({sql_str(ulpin)}, {sql_str(ror_status)}, {sql_str(f'KH-CAMP-{n:03d}')}, "
            f"{sql_str('Synthetic campus RoR record')});"
        )

        if i in pending_reg:
            reg_status, reg_date, doc = "Pending", None, None
        else:
            reg_status, reg_date, doc = "Registered", f"2024-{(i % 12) + 1:02d}-{(i % 27) + 1:02d}", f"REG-DEMO-{n:04d}"
        child_sql["registrations"].append(
            f"INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES "
            f"({sql_str(ulpin)}, {sql_str(reg_status)}, {sql_str(reg_date)}, {sql_str(doc)});"
        )

        child_sql["land_use"].append(
            f"INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES "
            f"({sql_str(ulpin)}, {sql_str(land_use)}, {sql_str(zoning)}, 'Demo Campus Master Plan 2026');"
        )

        if i in overdue_tax:
            tax_status, pay_date, due = "Overdue", "2025-12-01", 18500
        else:
            tax_status, pay_date, due = "Paid", f"2026-0{(i % 8) + 1}-10", 0
        child_sql["tax"].append(
            f"INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES "
            f"({sql_str(ulpin)}, {sql_str(tax_status)}, {sql_str(pay_date)}, {due});"
        )

        if i in restricted:
            res_status, res_type, res_desc = "Restricted", "Environmental Buffer", "No new construction in green/utility buffer"
        elif i in mortgaged:
            res_status, res_type, res_desc = "Mortgaged", "Mortgage", "Synthetic housing board mortgage flag"
        else:
            res_status, res_type, res_desc = "None", None, None
        child_sql["restrictions"].append(
            f"INSERT INTO restrictions (ulpin, status, type, description) VALUES "
            f"({sql_str(ulpin)}, {sql_str(res_status)}, {sql_str(res_type)}, {sql_str(res_desc)});"
        )

        if i in disputed:
            d_status, d_desc, d_date = "Disputed", "Synthetic boundary overlap claim for demo", "2026-03-12"
        else:
            d_status, d_desc, d_date = "None", None, None
        child_sql["disputes"].append(
            f"INSERT INTO disputes (ulpin, status, description, filed_date) VALUES "
            f"({sql_str(ulpin)}, {sql_str(d_status)}, {sql_str(d_desc)}, {sql_str(d_date)});"
        )

        if i in pending_bp:
            bp_status, permit, issued = "Pending", None, None
        elif land_use == "Vacant":
            bp_status, permit, issued = "Not Applied", None, None
        else:
            bp_status, permit, issued = "Approved", f"BP-DEMO-{n:04d}", "2025-06-15"
        child_sql["building_permissions"].append(
            f"INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES "
            f"({sql_str(ulpin)}, {sql_str(bp_status)}, {sql_str(permit)}, {sql_str(issued)});"
        )

        features.append({
            "type": "Feature",
            "properties": {
                "ulpin": ulpin,
                "survey_number": survey,
                "parcel_number": parcel_number,
                "name": name,
                "land_use": land_use,
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[round(lon, 8), round(lat, 8)] for lon, lat in ring]],
            },
        })

    admin_hash = hash_password("admin123")
    citizen_hash = hash_password("citizen123")

    lines = [
        "-- BhuStack synthetic seed data (fictional campus).",
        "-- This prototype uses synthetic demonstration data and does not claim",
        "-- access to live government land records.",
        "BEGIN;",
        "TRUNCATE audit_logs, service_requests, users, building_permissions, disputes,",
        "         restrictions, tax, land_use, registrations, ror, ownership, parcels",
        "         RESTART IDENTITY CASCADE;",
        "",
        "-- Parcels",
        *parcels_sql,
        "",
        "-- Ownership",
        *child_sql["ownership"],
        "",
        "-- Record of Rights",
        *child_sql["ror"],
        "",
        "-- Registrations",
        *child_sql["registrations"],
        "",
        "-- Land use",
        *child_sql["land_use"],
        "",
        "-- Tax",
        *child_sql["tax"],
        "",
        "-- Restrictions",
        *child_sql["restrictions"],
        "",
        "-- Disputes",
        *child_sql["disputes"],
        "",
        "-- Building permissions",
        *child_sql["building_permissions"],
        "",
        "-- Demo users (SHA256 of bhustack-demo:<password>)",
        f"INSERT INTO users (username, password_hash, role) VALUES ('admin', '{admin_hash}', 'ADMIN');",
        f"INSERT INTO users (username, password_hash, role) VALUES ('citizen', '{citizen_hash}', 'CITIZEN');",
        "",
        "-- Sample service requests",
        "INSERT INTO service_requests (request_id, ulpin, service_type, status, remarks) VALUES",
        "('REQ-000001', 'IND-DEMO-000001', 'LAND_RECORD_VERIFICATION', 'SUBMITTED', 'Citizen requested RoR verification'),",
        "('REQ-000002', 'IND-DEMO-000008', 'MUTATION_REQUEST', 'UNDER_REVIEW', 'Synthetic mutation demo'),",
        "('REQ-000003', 'IND-DEMO-000017', 'TAX_CLARIFICATION', 'APPROVED', 'Tax status clarified for demo');",
        "",
        "INSERT INTO audit_logs (audit_id, username, action, ulpin, description) VALUES",
        "('AUD-000001', 'system', 'SEED_LOAD', NULL, 'Loaded synthetic campus dataset'),",
        "('AUD-000002', 'admin', 'UPDATE_TAX_STATUS', 'IND-DEMO-000017', 'Demo tax clarification');",
        "",
        "COMMIT;",
    ]

    (root / "seed.sql").write_text("\n".join(lines) + "\n", encoding="utf-8")

    geojson = {
        "type": "FeatureCollection",
        "name": "bhustack_demo_campus",
        "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
        "features": features,
    }
    (sample / "campus_parcels.geojson").write_text(json.dumps(geojson, indent=2), encoding="utf-8")
    print(f"Wrote seed.sql with {TOTAL} parcels and sample GeoJSON")


if __name__ == "__main__":
    main()
