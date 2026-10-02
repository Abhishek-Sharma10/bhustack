-- BhuStack SQL query reference
-- Keep this file in sync with schema.sql and backend queries.
-- All examples use synthetic ULPIN IND-DEMO-000001.

-- ============================================================
-- DATABASE SETUP
-- ============================================================

-- Enable PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

-- Verify PostGIS
SELECT PostGIS_Version();
SELECT extname, extversion FROM pg_extension WHERE extname = 'postgis';

-- ============================================================
-- PARCEL OPERATIONS
-- ============================================================

-- Get all parcels
SELECT id, ulpin, survey_number, parcel_number, area, state, district, village, land_type
FROM parcels
ORDER BY ulpin;

-- Get parcel by ULPIN
SELECT *
FROM parcels
WHERE ulpin = 'IND-DEMO-000001';

-- Search by survey number
SELECT ulpin, survey_number, parcel_number, village
FROM parcels
WHERE survey_number ILIKE '%245%' OR survey_number ILIKE '%200/1%';

-- Search by parcel number
SELECT ulpin, survey_number, parcel_number
FROM parcels
WHERE parcel_number ILIKE '%P-001%';

-- Combined search (ULPIN / survey / parcel number)
SELECT ulpin, survey_number, parcel_number, village
FROM parcels
WHERE ulpin ILIKE '%IND-DEMO-000001%'
   OR survey_number ILIKE '%200/1%'
   OR parcel_number ILIKE '%P-001%';

-- Search by village
SELECT ulpin, parcel_number, village
FROM parcels
WHERE village ILIKE '%Demo Campus%';

-- Search by district
SELECT ulpin, district, village
FROM parcels
WHERE district ILIKE '%Demo District%';

-- ============================================================
-- GOVERNANCE DATA
-- ============================================================

-- Get ownership
SELECT * FROM ownership WHERE ulpin = 'IND-DEMO-000001';

-- Get RoR
SELECT * FROM ror WHERE ulpin = 'IND-DEMO-000001';

-- Get registration
SELECT * FROM registrations WHERE ulpin = 'IND-DEMO-000001';

-- Get land use
SELECT * FROM land_use WHERE ulpin = 'IND-DEMO-000001';

-- Get tax
SELECT * FROM tax WHERE ulpin = 'IND-DEMO-000001';

-- Get restrictions
SELECT * FROM restrictions WHERE ulpin = 'IND-DEMO-000001';

-- Get disputes
SELECT * FROM disputes WHERE ulpin = 'IND-DEMO-000001';

-- Get building permission
SELECT * FROM building_permissions WHERE ulpin = 'IND-DEMO-000001';

-- ============================================================
-- UNIFIED PARCEL PROFILE
-- ============================================================

SELECT
    p.ulpin,
    p.survey_number,
    p.parcel_number,
    p.area,
    p.state,
    p.district,
    p.village,
    p.land_type,
    p.source_type,
    o.owner_name,
    o.status AS ownership_status,
    ror.status AS ror_status,
    ror.khata_number,
    r.status AS registration_status,
    r.registration_date,
    lu.land_use,
    lu.zoning,
    lu.master_plan,
    t.status AS tax_status,
    t.last_payment_date,
    t.amount_due,
    res.status AS restriction_status,
    res.type AS restriction_type,
    d.status AS dispute_status,
    d.description AS dispute_description,
    bp.status AS building_permission_status,
    bp.permit_number,
    ST_AsGeoJSON(p.geometry)::json AS geometry
FROM parcels p
LEFT JOIN ownership o ON p.ulpin = o.ulpin
LEFT JOIN ror ON p.ulpin = ror.ulpin
LEFT JOIN registrations r ON p.ulpin = r.ulpin
LEFT JOIN land_use lu ON p.ulpin = lu.ulpin
LEFT JOIN tax t ON p.ulpin = t.ulpin
LEFT JOIN restrictions res ON p.ulpin = res.ulpin
LEFT JOIN disputes d ON p.ulpin = d.ulpin
LEFT JOIN building_permissions bp ON p.ulpin = bp.ulpin
WHERE p.ulpin = 'IND-DEMO-000001';

-- ============================================================
-- GEOJSON
-- ============================================================

SELECT json_build_object(
    'type', 'FeatureCollection',
    'features', COALESCE(json_agg(feature), '[]'::json)
)
FROM (
    SELECT json_build_object(
        'type', 'Feature',
        'properties', json_build_object(
            'ulpin', p.ulpin,
            'survey_number', p.survey_number,
            'parcel_number', p.parcel_number,
            'land_use', lu.land_use,
            'ownership_status', o.status,
            'restriction_status', res.status,
            'dispute_status', d.status
        ),
        'geometry', ST_AsGeoJSON(p.geometry)::json
    ) AS feature
    FROM parcels p
    LEFT JOIN land_use lu ON p.ulpin = lu.ulpin
    LEFT JOIN ownership o ON p.ulpin = o.ulpin
    LEFT JOIN restrictions res ON p.ulpin = res.ulpin
    LEFT JOIN disputes d ON p.ulpin = d.ulpin
) features;

-- ============================================================
-- DASHBOARD QUERIES
-- ============================================================

-- Total parcels
SELECT COUNT(*) AS total_parcels FROM parcels;

-- Verified parcels
SELECT COUNT(*) AS verified_parcels
FROM ownership
WHERE status = 'Verified';

-- Pending requests
SELECT COUNT(*) AS pending_requests
FROM service_requests
WHERE status IN ('SUBMITTED', 'UNDER_REVIEW');

-- Disputed parcels
SELECT COUNT(*) AS disputed_parcels
FROM disputes
WHERE status = 'Disputed';

-- Restricted parcels
SELECT COUNT(*) AS restricted_parcels
FROM restrictions
WHERE status IN ('Restricted', 'Mortgaged');

-- Tax status distribution
SELECT status, COUNT(*) AS count
FROM tax
GROUP BY status
ORDER BY count DESC;

-- Land-use distribution
SELECT land_use, COUNT(*) AS count
FROM land_use
GROUP BY land_use
ORDER BY count DESC;

-- Recent changes / requests
SELECT request_id, ulpin, service_type, status, submitted_date, last_updated
FROM service_requests
ORDER BY last_updated DESC
LIMIT 10;

SELECT audit_id, username, action, ulpin, description, created_at
FROM audit_logs
ORDER BY created_at DESC
LIMIT 10;

-- ============================================================
-- VALIDATION QUERIES
-- ============================================================

-- Duplicate ULPIN
SELECT ulpin, COUNT(*)
FROM parcels
GROUP BY ulpin
HAVING COUNT(*) > 1;

-- NULL ULPIN
SELECT id FROM parcels WHERE ulpin IS NULL;

-- Missing ownership
SELECT p.ulpin
FROM parcels p
LEFT JOIN ownership o ON p.ulpin = o.ulpin
WHERE o.ulpin IS NULL;

-- Missing registration
SELECT p.ulpin
FROM parcels p
LEFT JOIN registrations r ON p.ulpin = r.ulpin
WHERE r.ulpin IS NULL;

-- Missing land-use information
SELECT p.ulpin
FROM parcels p
LEFT JOIN land_use lu ON p.ulpin = lu.ulpin
WHERE lu.ulpin IS NULL;

-- Invalid geometry
SELECT ulpin
FROM parcels
WHERE geometry IS NULL OR NOT ST_IsValid(geometry);

-- Missing child records (any of the P0 child tables)
SELECT p.ulpin
FROM parcels p
LEFT JOIN ownership o ON p.ulpin = o.ulpin
LEFT JOIN ror ON p.ulpin = ror.ulpin
LEFT JOIN registrations r ON p.ulpin = r.ulpin
LEFT JOIN land_use lu ON p.ulpin = lu.ulpin
LEFT JOIN tax t ON p.ulpin = t.ulpin
LEFT JOIN restrictions res ON p.ulpin = res.ulpin
LEFT JOIN disputes d ON p.ulpin = d.ulpin
LEFT JOIN building_permissions bp ON p.ulpin = bp.ulpin
WHERE o.ulpin IS NULL OR ror.ulpin IS NULL OR r.ulpin IS NULL
   OR lu.ulpin IS NULL OR t.ulpin IS NULL OR res.ulpin IS NULL
   OR d.ulpin IS NULL OR bp.ulpin IS NULL;

-- ============================================================
-- SPATIAL QUERIES
-- ============================================================

-- Parcels within campus bounding box
SELECT ulpin, parcel_number
FROM parcels
WHERE ST_Intersects(
    geometry,
    ST_MakeEnvelope(77.5800, 12.9900, 77.5880, 12.9960, 4326)
);

-- Parcel area (sq.m approx using geography)
SELECT ulpin, area AS recorded_area,
       ST_Area(geometry::geography) AS computed_area_sq_m
FROM parcels
WHERE ulpin = 'IND-DEMO-000001';

-- Parcel intersection (self-overlap check)
SELECT a.ulpin AS ulpin_a, b.ulpin AS ulpin_b
FROM parcels a
JOIN parcels b ON a.id < b.id
WHERE ST_Intersects(a.geometry, b.geometry)
  AND ST_Area(ST_Intersection(a.geometry, b.geometry)) > 0;

-- Nearby parcels (within ~80m of target)
SELECT p.ulpin, p.parcel_number,
       ST_Distance(p.geometry::geography, t.geometry::geography) AS distance_m
FROM parcels p
JOIN parcels t ON t.ulpin = 'IND-DEMO-000001'
WHERE p.ulpin <> t.ulpin
  AND ST_DWithin(p.geometry::geography, t.geometry::geography, 80)
ORDER BY distance_m;

-- ============================================================
-- SERVICE REQUESTS (API TESTING)
-- ============================================================

SELECT * FROM service_requests WHERE request_id = 'REQ-000001';

INSERT INTO service_requests (request_id, ulpin, service_type, status, remarks)
VALUES ('REQ-TEST-001', 'IND-DEMO-000001', 'LAND_RECORD_VERIFICATION', 'SUBMITTED', 'API test');

UPDATE service_requests
SET status = 'UNDER_REVIEW', last_updated = NOW()
WHERE request_id = 'REQ-TEST-001';

-- Next request id helper
SELECT 'REQ-' || LPAD((COALESCE(MAX(SUBSTRING(request_id FROM 5)::INT), 0) + 1)::TEXT, 6, '0') AS next_request_id
FROM service_requests
WHERE request_id ~ '^REQ-[0-9]{6}$';

-- ============================================================
-- BACKEND API TESTING HELPERS
-- ============================================================

-- Health / counts
SELECT
    (SELECT COUNT(*) FROM parcels) AS parcels,
    (SELECT COUNT(*) FROM ownership) AS ownership,
    (SELECT COUNT(*) FROM ror) AS ror,
    (SELECT COUNT(*) FROM registrations) AS registrations;

-- Profile payload shape for GET /api/v1/parcels/{ulpin}
SELECT p.ulpin
FROM parcels p
WHERE p.ulpin IN ('IND-DEMO-000001', 'IND-DEMO-000008', 'IND-DEMO-000017', 'IND-DEMO-000022');
