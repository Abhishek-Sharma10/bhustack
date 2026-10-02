import json
from decimal import Decimal
from datetime import date, datetime

from app.database.connection import execute, fetch_all, fetch_one
from app.database.sql import GEOJSON_SQL, PARCEL_LIST_SQL, PROFILE_SQL, SEARCH_SQL
from app.schemas.parcel import row_to_profile
from app.utils.errors import not_found


def _clean(value):
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


def _clean_row(row):
    if row is None:
        return None
    return {k: _clean(v) for k, v in dict(row).items()}


def list_parcels():
    return [_clean_row(r) for r in fetch_all(PARCEL_LIST_SQL)]


def get_profile(ulpin: str):
    row = fetch_one(PROFILE_SQL, (ulpin,))
    if not row:
        raise not_found("Parcel", ulpin)
    return row_to_profile(dict(row))


def search_parcels(query: str):
    like = f"%{query}%"
    return [_clean_row(r) for r in fetch_all(SEARCH_SQL, (like, like, like, like, like, like, like, like, like))]


def get_geojson_for_ulpin(ulpin: str):
    row = fetch_one(
        "SELECT ST_AsGeoJSON(geometry) AS geojson FROM parcels WHERE ulpin = %s",
        (ulpin,),
    )
    if not row or row["geojson"] is None:
        return {"type": "FeatureCollection", "features": []}
    geojson = row["geojson"]
    if isinstance(geojson, str):
        return json.loads(geojson)
    return geojson


def search_administrative_area(area_type: str, query: str):
    like = f"%{query}%"
    area_type = (area_type or "").lower()
    if area_type not in {"state", "district", "block", "village"}:
        raise ValueError("Unsupported GIS area type")
    boundary_results = _search_boundary_regions(area_type, like)
    return boundary_results if boundary_results else _search_parcel_area_union(area_type, like)


def _search_boundary_regions(area_type: str, like: str):
    boundary_rows = fetch_all(
        """
        SELECT name, state, district, block, village, properties,
               ST_AsGeoJSON(geometry) AS geojson
        FROM administrative_regions
        WHERE type = %s AND name ILIKE %s
        ORDER BY name
        """,
        (area_type, like),
    )
    results = []
    for row in boundary_rows:
        properties = row.get("properties") or {}
        geometry = row.get("geojson")
        results.append({
            "name": row["name"],
            "label": row["name"],
            "type": area_type,
            "state": row.get("state"),
            "district": row.get("district"),
            "block": row.get("block"),
            "village": row.get("village"),
            "districts": properties.get("districts_count"),
            "villages": properties.get("villages_count"),
            "parcels": properties.get("parcels_count"),
            "geometry": json.loads(geometry) if isinstance(geometry, str) else geometry,
        })
    return results


def _search_parcel_area_union(area_type: str, like: str):
    if area_type == "state":
        rows = fetch_all(
            """
            SELECT state AS name, state AS label, COUNT(DISTINCT district) AS districts,
                   COUNT(DISTINCT village) AS villages, COUNT(*) AS parcels,
                   ST_Union(geometry) AS geometry
            FROM parcels
            WHERE state ILIKE %s
            GROUP BY state
            ORDER BY state
            """,
            (like,),
        )
    elif area_type == "district":
        rows = fetch_all(
            """
            SELECT district AS name, district AS label, COUNT(DISTINCT village) AS villages,
                   COUNT(*) AS parcels, ST_Union(geometry) AS geometry
            FROM parcels
            WHERE district ILIKE %s
            GROUP BY district
            ORDER BY district
            """,
            (like,),
        )
    elif area_type == "block":
        rows = fetch_all(
            """
            SELECT COALESCE(block, village) AS name, COALESCE(block, village) AS label,
                   COUNT(DISTINCT village) AS villages, COUNT(*) AS parcels,
                   ST_Union(geometry) AS geometry
            FROM parcels
            WHERE COALESCE(block, village) ILIKE %s
            GROUP BY COALESCE(block, village)
            ORDER BY COALESCE(block, village)
            """,
            (like,),
        )
    elif area_type == "village":
        rows = fetch_all(
            """
            SELECT village AS name, village AS label, COUNT(*) AS parcels,
                   ST_Union(geometry) AS geometry
            FROM parcels
            WHERE village ILIKE %s
            GROUP BY village
            ORDER BY village
            """,
            (like,),
        )
    results = []
    for row in rows:
        geometry = row["geometry"]
        results.append({
            "name": row["name"],
            "label": row["label"],
            "type": area_type,
            "districts": row.get("districts"),
            "villages": row.get("villages"),
            "parcels": row.get("parcels"),
            "geometry": json.loads(geometry) if isinstance(geometry, str) else geometry,
        })
    return results


def get_geojson():
    row = fetch_one(GEOJSON_SQL)
    if not row or row["geojson"] is None:
        return {"type": "FeatureCollection", "features": []}
    data = row["geojson"]
    if isinstance(data, str):
        return json.loads(data)
    return data


def get_admin_regions(region_type: str | None = None):
    query = """
        SELECT name, type, state, district, block, village, properties,
               ST_AsGeoJSON(geometry) AS geojson
        FROM administrative_regions
        WHERE (%s::text IS NULL OR type = %s)
        ORDER BY type, name
    """
    rows = fetch_all(query, (region_type, region_type))
    features = []
    for row in rows:
        geometry = row.get("geojson")
        if not geometry:
            continue
        features.append({
            "type": "Feature",
            "properties": {
                "name": row.get("name"),
                "type": row.get("type"),
                "state": row.get("state"),
                "district": row.get("district"),
                "block": row.get("block"),
                "village": row.get("village"),
                **(row.get("properties") or {}),
            },
            "geometry": json.loads(geometry) if isinstance(geometry, str) else geometry,
        })
    return {"type": "FeatureCollection", "features": features}


def get_child(table: str, ulpin: str):
    allowed = {
        "ownership",
        "ror",
        "registrations",
        "land_use",
        "tax",
        "restrictions",
        "disputes",
        "building_permissions",
    }
    if table not in allowed:
        raise ValueError("Invalid table")
    row = fetch_one(f"SELECT * FROM {table} WHERE ulpin = %s", (ulpin,))
    if not row:
        raise not_found(table, ulpin)
    return _clean_row(row)


def dashboard_stats():
    return {
        "total_parcels": fetch_one("SELECT COUNT(*) AS n FROM parcels")["n"],
        "verified_parcels": fetch_one(
            "SELECT COUNT(*) AS n FROM ownership WHERE status = 'Verified'"
        )["n"],
        "pending_requests": fetch_one(
            "SELECT COUNT(*) AS n FROM service_requests WHERE status IN ('SUBMITTED', 'UNDER_REVIEW')"
        )["n"],
        "disputed_parcels": fetch_one(
            "SELECT COUNT(*) AS n FROM disputes WHERE status = 'Disputed'"
        )["n"],
        "restricted_parcels": fetch_one(
            "SELECT COUNT(*) AS n FROM restrictions WHERE status IN ('Restricted', 'Mortgaged')"
        )["n"],
        "land_use_distribution": [_clean_row(r) for r in fetch_all(
            "SELECT land_use AS label, COUNT(*) AS count FROM land_use GROUP BY land_use ORDER BY count DESC"
        )],
        "tax_status_distribution": [_clean_row(r) for r in fetch_all(
            "SELECT status AS label, COUNT(*) AS count FROM tax GROUP BY status ORDER BY count DESC"
        )],
        "recent_requests": [_clean_row(r) for r in fetch_all(
            """
            SELECT request_id, ulpin, service_type, status, submitted_date, last_updated, remarks
            FROM service_requests
            ORDER BY last_updated DESC
            LIMIT 8
            """
        )],
        "recent_changes": [_clean_row(r) for r in fetch_all(
            """
            SELECT audit_id, username, action, ulpin, description, created_at
            FROM audit_logs
            ORDER BY created_at DESC
            LIMIT 8
            """
        )],
    }


def write_audit(username: str, action: str, ulpin: str | None, description: str):
    next_id = fetch_one(
        """
        SELECT 'AUD-' || LPAD((COALESCE(MAX(SUBSTRING(audit_id FROM 5)::INT), 0) + 1)::TEXT, 6, '0') AS next_id
        FROM audit_logs
        WHERE audit_id ~ '^AUD-[0-9]{6}$'
        """
    )["next_id"]
    execute(
        """
        INSERT INTO audit_logs (audit_id, username, action, ulpin, description)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (next_id, username, action, ulpin, description),
    )
    return next_id
