-- BhuStack synthetic seed data (fictional campus).
-- This prototype uses synthetic demonstration data and does not claim
-- access to live government land records.
BEGIN;
TRUNCATE audit_logs, service_requests, users, building_permissions, disputes,
         restrictions, tax, land_use, registrations, ror, ownership, parcels
         RESTART IDENTITY CASCADE;

-- Parcels
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000001', '200/1', 'P-001', 900, 'Demo State', 'Demo District', 'Demo Campus', 'Academic Block A', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58005333 12.99004800, 77.58128000 12.99004800, 77.58128000 12.99115200, 77.58005333 12.99115200, 77.58005333 12.99004800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000002', '200/2', 'P-002', 957, 'Demo State', 'Demo District', 'Demo Campus', 'Academic Block B', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58138667 12.99004800, 77.58261333 12.99004800, 77.58261333 12.99115200, 77.58138667 12.99115200, 77.58138667 12.99004800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000003', '200/3', 'P-003', 1014, 'Demo State', 'Demo District', 'Demo Campus', 'Academic Block C', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58272000 12.99004800, 77.58394667 12.99004800, 77.58394667 12.99115200, 77.58272000 12.99115200, 77.58272000 12.99004800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000004', '201/1', 'P-004', 1071, 'Demo State', 'Demo District', 'Demo Campus', 'Lecture Hall Complex', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58405333 12.99004800, 77.58528000 12.99004800, 77.58528000 12.99115200, 77.58405333 12.99115200, 77.58405333 12.99004800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000005', '201/2', 'P-005', 1128, 'Demo State', 'Demo District', 'Demo Campus', 'Central Library', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58538667 12.99004800, 77.58661333 12.99004800, 77.58661333 12.99115200, 77.58538667 12.99115200, 77.58538667 12.99004800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000006', '201/3', 'P-006', 1085, 'Demo State', 'Demo District', 'Demo Campus', 'Computer Science Lab', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58672000 12.99004800, 77.58794667 12.99004800, 77.58794667 12.99115200, 77.58672000 12.99115200, 77.58672000 12.99004800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000007', '202/1', 'P-007', 1142, 'Demo State', 'Demo District', 'Demo Campus', 'Electronics Lab', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58005333 12.99124800, 77.58128000 12.99124800, 77.58128000 12.99235200, 77.58005333 12.99235200, 77.58005333 12.99124800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000008', '202/2', 'P-008', 1199, 'Demo State', 'Demo District', 'Demo Campus', 'Workshop Shed', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58138667 12.99124800, 77.58261333 12.99124800, 77.58261333 12.99235200, 77.58138667 12.99235200, 77.58138667 12.99124800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000009', '202/3', 'P-009', 1256, 'Demo State', 'Demo District', 'Demo Campus', 'Hostel A', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58272000 12.99124800, 77.58394667 12.99124800, 77.58394667 12.99235200, 77.58272000 12.99235200, 77.58272000 12.99124800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000010', '203/1', 'P-010', 1313, 'Demo State', 'Demo District', 'Demo Campus', 'Hostel B', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58405333 12.99124800, 77.58528000 12.99124800, 77.58528000 12.99235200, 77.58405333 12.99235200, 77.58405333 12.99124800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000011', '203/2', 'P-011', 1270, 'Demo State', 'Demo District', 'Demo Campus', 'Hostel C', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58538667 12.99124800, 77.58661333 12.99124800, 77.58661333 12.99235200, 77.58538667 12.99235200, 77.58538667 12.99124800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000012', '203/3', 'P-012', 1327, 'Demo State', 'Demo District', 'Demo Campus', 'Dining Hall', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58672000 12.99124800, 77.58794667 12.99124800, 77.58794667 12.99235200, 77.58672000 12.99235200, 77.58672000 12.99124800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000013', '204/1', 'P-013', 1384, 'Demo State', 'Demo District', 'Demo Campus', 'Sports Complex', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58005333 12.99244800, 77.58128000 12.99244800, 77.58128000 12.99355200, 77.58005333 12.99355200, 77.58005333 12.99244800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000014', '204/2', 'P-014', 1441, 'Demo State', 'Demo District', 'Demo Campus', 'Playground', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58138667 12.99244800, 77.58261333 12.99244800, 77.58261333 12.99355200, 77.58138667 12.99355200, 77.58138667 12.99244800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000015', '204/3', 'P-015', 1498, 'Demo State', 'Demo District', 'Demo Campus', 'Admin Block', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58272000 12.99244800, 77.58394667 12.99244800, 77.58394667 12.99355200, 77.58272000 12.99355200, 77.58272000 12.99244800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000016', '205/1', 'P-016', 1455, 'Demo State', 'Demo District', 'Demo Campus', 'Staff Quarters 1', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58405333 12.99244800, 77.58528000 12.99244800, 77.58528000 12.99355200, 77.58405333 12.99355200, 77.58405333 12.99244800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000017', '205/2', 'P-017', 1512, 'Demo State', 'Demo District', 'Demo Campus', 'Staff Quarters 2', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58538667 12.99244800, 77.58661333 12.99244800, 77.58661333 12.99355200, 77.58538667 12.99355200, 77.58538667 12.99244800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000018', '205/3', 'P-018', 1569, 'Demo State', 'Demo District', 'Demo Campus', 'Guest House', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58672000 12.99244800, 77.58794667 12.99244800, 77.58794667 12.99355200, 77.58672000 12.99355200, 77.58672000 12.99244800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000019', '206/1', 'P-019', 1626, 'Demo State', 'Demo District', 'Demo Campus', 'Auditorium', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58005333 12.99364800, 77.58128000 12.99364800, 77.58128000 12.99475200, 77.58005333 12.99475200, 77.58005333 12.99364800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000020', '206/2', 'P-020', 1683, 'Demo State', 'Demo District', 'Demo Campus', 'Innovation Centre', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58138667 12.99364800, 77.58261333 12.99364800, 77.58261333 12.99475200, 77.58138667 12.99475200, 77.58138667 12.99364800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000021', '206/3', 'P-021', 1640, 'Demo State', 'Demo District', 'Demo Campus', 'Utility Substation', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58272000 12.99364800, 77.58394667 12.99364800, 77.58394667 12.99475200, 77.58272000 12.99475200, 77.58272000 12.99364800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000022', '207/1', 'P-022', 1697, 'Demo State', 'Demo District', 'Demo Campus', 'Green Belt East', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58405333 12.99364800, 77.58528000 12.99364800, 77.58528000 12.99475200, 77.58405333 12.99475200, 77.58405333 12.99364800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000023', '207/2', 'P-023', 954, 'Demo State', 'Demo District', 'Demo Campus', 'Parking Lot North', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58538667 12.99364800, 77.58661333 12.99364800, 77.58661333 12.99475200, 77.58538667 12.99475200, 77.58538667 12.99364800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000024', '207/3', 'P-024', 1011, 'Demo State', 'Demo District', 'Demo Campus', 'Open Amphitheatre', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58672000 12.99364800, 77.58794667 12.99364800, 77.58794667 12.99475200, 77.58672000 12.99475200, 77.58672000 12.99364800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000025', '208/1', 'P-025', 1068, 'Demo State', 'Demo District', 'Demo Campus', 'Health Centre', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58005333 12.99484800, 77.58128000 12.99484800, 77.58128000 12.99595200, 77.58005333 12.99595200, 77.58005333 12.99484800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000026', '208/2', 'P-026', 1025, 'Demo State', 'Demo District', 'Demo Campus', 'Campus Canteen', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58138667 12.99484800, 77.58261333 12.99484800, 77.58261333 12.99595200, 77.58138667 12.99595200, 77.58138667 12.99484800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000027', '208/3', 'P-027', 1082, 'Demo State', 'Demo District', 'Demo Campus', 'Book Store', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58272000 12.99484800, 77.58394667 12.99484800, 77.58394667 12.99595200, 77.58272000 12.99595200, 77.58272000 12.99484800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000028', '209/1', 'P-028', 1139, 'Demo State', 'Demo District', 'Demo Campus', 'Maintenance Yard', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58405333 12.99484800, 77.58528000 12.99484800, 77.58528000 12.99595200, 77.58405333 12.99595200, 77.58405333 12.99484800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000029', '209/2', 'P-029', 1196, 'Demo State', 'Demo District', 'Demo Campus', 'Water Tank Parcel', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58538667 12.99484800, 77.58661333 12.99484800, 77.58661333 12.99595200, 77.58538667 12.99595200, 77.58538667 12.99484800))', 4326));
INSERT INTO parcels (ulpin, survey_number, parcel_number, area, state, district, village, land_type, source_type, geometry) VALUES ('IND-DEMO-000030', '209/3', 'P-030', 1253, 'Demo State', 'Demo District', 'Demo Campus', 'Vacant Plot West', 'SYNTHETIC', ST_GeomFromText('POLYGON((77.58672000 12.99484800, 77.58794667 12.99484800, 77.58794667 12.99595200, 77.58672000 12.99595200, 77.58672000 12.99484800))', 4326));

-- Ownership
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000001', 'Demo University', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000002', 'Demo University Trust', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000003', 'Demo Campus Housing Board', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000004', 'Demo State Public Works', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000005', 'Demo University Sports Board', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000006', 'Demo University', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000007', 'Demo University Trust', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000008', 'Demo Campus Housing Board', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000009', 'Demo State Public Works', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000010', 'Demo University Sports Board', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000011', 'Demo University', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000012', 'Demo University Trust', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000013', 'Demo Campus Housing Board', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000014', 'Demo State Public Works', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000015', 'Demo University Sports Board', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000016', 'Demo University', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000017', 'Demo University Trust', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000018', 'Demo Campus Housing Board', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000019', 'Demo State Public Works', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000020', 'Demo University Sports Board', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000021', 'Demo University', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000022', 'Demo University Trust', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000023', 'Demo Campus Housing Board', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000024', 'Demo State Public Works', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000025', 'Demo University Sports Board', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000026', 'Demo University', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000027', 'Demo University Trust', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000028', 'Demo Campus Housing Board', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000029', 'Demo State Public Works', 'Verified', 'Institution');
INSERT INTO ownership (ulpin, owner_name, status, owner_type) VALUES ('IND-DEMO-000030', 'Demo University Sports Board', 'Pending', 'Institution');

-- Record of Rights
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000001', 'Issued', 'KH-CAMP-001', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000002', 'Issued', 'KH-CAMP-002', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000003', 'Issued', 'KH-CAMP-003', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000004', 'Issued', 'KH-CAMP-004', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000005', 'Issued', 'KH-CAMP-005', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000006', 'Issued', 'KH-CAMP-006', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000007', 'Issued', 'KH-CAMP-007', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000008', 'Issued', 'KH-CAMP-008', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000009', 'Issued', 'KH-CAMP-009', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000010', 'Issued', 'KH-CAMP-010', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000011', 'Issued', 'KH-CAMP-011', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000012', 'Issued', 'KH-CAMP-012', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000013', 'Issued', 'KH-CAMP-013', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000014', 'Issued', 'KH-CAMP-014', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000015', 'Issued', 'KH-CAMP-015', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000016', 'Issued', 'KH-CAMP-016', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000017', 'Issued', 'KH-CAMP-017', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000018', 'Issued', 'KH-CAMP-018', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000019', 'Issued', 'KH-CAMP-019', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000020', 'Issued', 'KH-CAMP-020', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000021', 'Issued', 'KH-CAMP-021', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000022', 'Issued', 'KH-CAMP-022', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000023', 'Issued', 'KH-CAMP-023', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000024', 'Issued', 'KH-CAMP-024', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000025', 'Issued', 'KH-CAMP-025', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000026', 'Issued', 'KH-CAMP-026', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000027', 'Issued', 'KH-CAMP-027', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000028', 'Issued', 'KH-CAMP-028', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000029', 'Issued', 'KH-CAMP-029', 'Synthetic campus RoR record');
INSERT INTO ror (ulpin, status, khata_number, remarks) VALUES ('IND-DEMO-000030', 'Pending', 'KH-CAMP-030', 'Synthetic campus RoR record');

-- Registrations
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000001', 'Registered', '2024-01-01', 'REG-DEMO-0001');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000002', 'Registered', '2024-02-02', 'REG-DEMO-0002');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000003', 'Registered', '2024-03-03', 'REG-DEMO-0003');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000004', 'Registered', '2024-04-04', 'REG-DEMO-0004');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000005', 'Registered', '2024-05-05', 'REG-DEMO-0005');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000006', 'Registered', '2024-06-06', 'REG-DEMO-0006');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000007', 'Registered', '2024-07-07', 'REG-DEMO-0007');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000008', 'Registered', '2024-08-08', 'REG-DEMO-0008');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000009', 'Registered', '2024-09-09', 'REG-DEMO-0009');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000010', 'Registered', '2024-10-10', 'REG-DEMO-0010');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000011', 'Registered', '2024-11-11', 'REG-DEMO-0011');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000012', 'Registered', '2024-12-12', 'REG-DEMO-0012');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000013', 'Registered', '2024-01-13', 'REG-DEMO-0013');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000014', 'Registered', '2024-02-14', 'REG-DEMO-0014');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000015', 'Registered', '2024-03-15', 'REG-DEMO-0015');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000016', 'Registered', '2024-04-16', 'REG-DEMO-0016');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000017', 'Registered', '2024-05-17', 'REG-DEMO-0017');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000018', 'Registered', '2024-06-18', 'REG-DEMO-0018');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000019', 'Registered', '2024-07-19', 'REG-DEMO-0019');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000020', 'Registered', '2024-08-20', 'REG-DEMO-0020');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000021', 'Registered', '2024-09-21', 'REG-DEMO-0021');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000022', 'Registered', '2024-10-22', 'REG-DEMO-0022');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000023', 'Registered', '2024-11-23', 'REG-DEMO-0023');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000024', 'Registered', '2024-12-24', 'REG-DEMO-0024');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000025', 'Registered', '2024-01-25', 'REG-DEMO-0025');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000026', 'Registered', '2024-02-26', 'REG-DEMO-0026');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000027', 'Registered', '2024-03-27', 'REG-DEMO-0027');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000028', 'Registered', '2024-04-01', 'REG-DEMO-0028');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000029', 'Registered', '2024-05-02', 'REG-DEMO-0029');
INSERT INTO registrations (ulpin, status, registration_date, document_number) VALUES ('IND-DEMO-000030', 'Pending', NULL, NULL);

-- Land use
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000001', 'Institutional', 'Academic Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000002', 'Institutional', 'Academic Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000003', 'Institutional', 'Academic Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000004', 'Institutional', 'Academic Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000005', 'Institutional', 'Academic Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000006', 'Institutional', 'Academic Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000007', 'Institutional', 'Academic Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000008', 'Institutional', 'Utility Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000009', 'Institutional', 'Residential Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000010', 'Institutional', 'Residential Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000011', 'Institutional', 'Residential Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000012', 'Institutional', 'Residential Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000013', 'Recreational', 'Recreation Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000014', 'Recreational', 'Recreation Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000015', 'Institutional', 'Administrative Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000016', 'Residential', 'Residential Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000017', 'Residential', 'Residential Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000018', 'Residential', 'Residential Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000019', 'Institutional', 'Academic Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000020', 'Institutional', 'Academic Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000021', 'Utility', 'Utility Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000022', 'Environmental', 'Green Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000023', 'Utility', 'Utility Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000024', 'Recreational', 'Recreation Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000025', 'Institutional', 'Institutional Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000026', 'Commercial', 'Mixed Use Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000027', 'Commercial', 'Mixed Use Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000028', 'Utility', 'Utility Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000029', 'Utility', 'Utility Zone', 'Demo Campus Master Plan 2026');
INSERT INTO land_use (ulpin, land_use, zoning, master_plan) VALUES ('IND-DEMO-000030', 'Vacant', 'Future Expansion', 'Demo Campus Master Plan 2026');

-- Tax
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000001', 'Paid', '2026-01-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000002', 'Paid', '2026-02-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000003', 'Paid', '2026-03-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000004', 'Paid', '2026-04-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000005', 'Paid', '2026-05-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000006', 'Paid', '2026-06-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000007', 'Paid', '2026-07-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000008', 'Paid', '2026-08-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000009', 'Paid', '2026-01-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000010', 'Paid', '2026-02-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000011', 'Paid', '2026-03-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000012', 'Overdue', '2025-12-01', 18500);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000013', 'Paid', '2026-05-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000014', 'Paid', '2026-06-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000015', 'Paid', '2026-07-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000016', 'Paid', '2026-08-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000017', 'Paid', '2026-01-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000018', 'Paid', '2026-02-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000019', 'Paid', '2026-03-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000020', 'Paid', '2026-04-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000021', 'Paid', '2026-05-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000022', 'Paid', '2026-06-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000023', 'Paid', '2026-07-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000024', 'Paid', '2026-08-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000025', 'Paid', '2026-01-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000026', 'Overdue', '2025-12-01', 18500);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000027', 'Paid', '2026-03-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000028', 'Paid', '2026-04-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000029', 'Paid', '2026-05-10', 0);
INSERT INTO tax (ulpin, status, last_payment_date, amount_due) VALUES ('IND-DEMO-000030', 'Paid', '2026-06-10', 0);

-- Restrictions
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000001', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000002', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000003', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000004', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000005', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000006', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000007', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000008', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000009', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000010', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000011', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000012', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000013', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000014', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000015', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000016', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000017', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000018', 'Mortgaged', 'Mortgage', 'Synthetic housing board mortgage flag');
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000019', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000020', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000021', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000022', 'Restricted', 'Environmental Buffer', 'No new construction in green/utility buffer');
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000023', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000024', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000025', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000026', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000027', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000028', 'None', NULL, NULL);
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000029', 'Restricted', 'Environmental Buffer', 'No new construction in green/utility buffer');
INSERT INTO restrictions (ulpin, status, type, description) VALUES ('IND-DEMO-000030', 'None', NULL, NULL);

-- Disputes
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000001', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000002', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000003', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000004', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000005', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000006', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000007', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000008', 'Disputed', 'Synthetic boundary overlap claim for demo', '2026-03-12');
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000009', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000010', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000011', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000012', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000013', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000014', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000015', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000016', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000017', 'Disputed', 'Synthetic boundary overlap claim for demo', '2026-03-12');
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000018', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000019', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000020', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000021', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000022', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000023', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000024', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000025', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000026', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000027', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000028', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000029', 'None', NULL, NULL);
INSERT INTO disputes (ulpin, status, description, filed_date) VALUES ('IND-DEMO-000030', 'None', NULL, NULL);

-- Building permissions
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000001', 'Approved', 'BP-DEMO-0001', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000002', 'Approved', 'BP-DEMO-0002', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000003', 'Approved', 'BP-DEMO-0003', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000004', 'Approved', 'BP-DEMO-0004', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000005', 'Approved', 'BP-DEMO-0005', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000006', 'Approved', 'BP-DEMO-0006', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000007', 'Approved', 'BP-DEMO-0007', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000008', 'Approved', 'BP-DEMO-0008', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000009', 'Pending', NULL, NULL);
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000010', 'Approved', 'BP-DEMO-0010', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000011', 'Approved', 'BP-DEMO-0011', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000012', 'Approved', 'BP-DEMO-0012', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000013', 'Approved', 'BP-DEMO-0013', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000014', 'Approved', 'BP-DEMO-0014', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000015', 'Approved', 'BP-DEMO-0015', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000016', 'Approved', 'BP-DEMO-0016', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000017', 'Approved', 'BP-DEMO-0017', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000018', 'Approved', 'BP-DEMO-0018', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000019', 'Approved', 'BP-DEMO-0019', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000020', 'Approved', 'BP-DEMO-0020', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000021', 'Approved', 'BP-DEMO-0021', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000022', 'Approved', 'BP-DEMO-0022', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000023', 'Approved', 'BP-DEMO-0023', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000024', 'Approved', 'BP-DEMO-0024', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000025', 'Approved', 'BP-DEMO-0025', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000026', 'Approved', 'BP-DEMO-0026', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000027', 'Approved', 'BP-DEMO-0027', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000028', 'Approved', 'BP-DEMO-0028', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000029', 'Approved', 'BP-DEMO-0029', '2025-06-15');
INSERT INTO building_permissions (ulpin, status, permit_number, issued_date) VALUES ('IND-DEMO-000030', 'Pending', NULL, NULL);

-- Demo users (SHA256 of bhustack-demo:<password>)
INSERT INTO users (username, password_hash, role) VALUES ('admin', '03904b1e9fd6d3bd2d36f9a492eae22bbcb15db69dcc5dc94f51d7a687a08157', 'ADMIN');
INSERT INTO users (username, password_hash, role) VALUES ('citizen', '2d830230f84192c1d714fcd0d1502cbbfa25388ad9449d86d1e055c4b54c0a02', 'CITIZEN');

-- Sample service requests
INSERT INTO service_requests (request_id, ulpin, service_type, status, remarks) VALUES
('REQ-000001', 'IND-DEMO-000001', 'LAND_RECORD_VERIFICATION', 'SUBMITTED', 'Citizen requested RoR verification'),
('REQ-000002', 'IND-DEMO-000008', 'MUTATION_REQUEST', 'UNDER_REVIEW', 'Synthetic mutation demo'),
('REQ-000003', 'IND-DEMO-000017', 'TAX_CLARIFICATION', 'APPROVED', 'Tax status clarified for demo');

INSERT INTO audit_logs (audit_id, username, action, ulpin, description) VALUES
('AUD-000001', 'system', 'SEED_LOAD', NULL, 'Loaded synthetic campus dataset'),
('AUD-000002', 'admin', 'UPDATE_TAX_STATUS', 'IND-DEMO-000017', 'Demo tax clarification');

COMMIT;
