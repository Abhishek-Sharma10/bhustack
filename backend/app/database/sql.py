PROFILE_SQL = """
SELECT
    p.ulpin,
    p.survey_number,
    p.parcel_number,
    p.area,
    p.state,
    p.district,
    p.block,
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
    bp.permit_number
FROM parcels p
LEFT JOIN ownership o ON p.ulpin = o.ulpin
LEFT JOIN ror ON p.ulpin = ror.ulpin
LEFT JOIN registrations r ON p.ulpin = r.ulpin
LEFT JOIN land_use lu ON p.ulpin = lu.ulpin
LEFT JOIN tax t ON p.ulpin = t.ulpin
LEFT JOIN restrictions res ON p.ulpin = res.ulpin
LEFT JOIN disputes d ON p.ulpin = d.ulpin
LEFT JOIN building_permissions bp ON p.ulpin = bp.ulpin
WHERE p.ulpin = %s
"""

PARCEL_LIST_SQL = """
SELECT p.ulpin, p.survey_number, p.parcel_number, p.area, p.block, p.village, p.district, p.state,
       lu.land_use, o.status AS ownership_status
FROM parcels p
LEFT JOIN land_use lu ON p.ulpin = lu.ulpin
LEFT JOIN ownership o ON p.ulpin = o.ulpin
ORDER BY p.ulpin
"""

SEARCH_SQL = """
SELECT p.ulpin, p.survey_number, p.parcel_number, p.area, p.block, p.village, p.district, p.state,
       p.land_type, lu.land_use
FROM parcels p
LEFT JOIN land_use lu ON p.ulpin = lu.ulpin
WHERE p.ulpin ILIKE %s
   OR p.survey_number ILIKE %s
   OR p.parcel_number ILIKE %s
   OR p.state ILIKE %s
   OR p.district ILIKE %s
   OR p.block ILIKE %s
   OR p.village ILIKE %s
   OR p.land_type ILIKE %s
   OR lu.land_use ILIKE %s
ORDER BY p.ulpin
"""

GEOJSON_SQL = """
SELECT json_build_object(
    'type', 'FeatureCollection',
    'features', COALESCE(json_agg(feature), '[]'::json)
) AS geojson
FROM (
    SELECT json_build_object(
        'type', 'Feature',
        'properties', json_build_object(
            'ulpin', p.ulpin,
            'survey_number', p.survey_number,
            'parcel_number', p.parcel_number,
            'area', p.area,
            'state', p.state,
            'district', p.district,
            'block', p.block,
            'village', p.village,
            'land_type', p.land_type,
            'source_type', p.source_type,
            'owner', o.owner_name,
            'land_use', lu.land_use,
            'zoning', lu.zoning,
            'ownership_status', o.status,
            'restriction_status', res.status,
            'dispute_status', d.status,
            'tax_status', t.status
        ),
        'geometry', ST_AsGeoJSON(p.geometry)::json
    ) AS feature
    FROM parcels p
    LEFT JOIN land_use lu ON p.ulpin = lu.ulpin
    LEFT JOIN ownership o ON p.ulpin = o.ulpin
    LEFT JOIN restrictions res ON p.ulpin = res.ulpin
    LEFT JOIN disputes d ON p.ulpin = d.ulpin
    LEFT JOIN tax t ON p.ulpin = t.ulpin
) features
"""
