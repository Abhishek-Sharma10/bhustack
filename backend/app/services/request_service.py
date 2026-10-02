from app.database.connection import execute, fetch_one
from app.services.parcel_service import _clean_row
from app.services.parcel_service import write_audit
from app.utils.errors import not_found

ALLOWED_STATUS = {"SUBMITTED", "UNDER_REVIEW", "APPROVED", "REJECTED"}
ALLOWED_TYPES = {
    "LAND_RECORD_VERIFICATION",
    "MUTATION_REQUEST",
    "TAX_CLARIFICATION",
    "BUILDING_PERMISSION_STATUS",
    "DISPUTE_STATUS_CHECK",
}


def _next_request_id() -> str:
    row = fetch_one(
        """
        SELECT 'REQ-' || LPAD((COALESCE(MAX(SUBSTRING(request_id FROM 5)::INT), 0) + 1)::TEXT, 6, '0') AS next_id
        FROM service_requests
        WHERE request_id ~ '^REQ-[0-9]{6}$'
        """
    )
    return row["next_id"]


def create_request(ulpin: str, service_type: str, remarks: str | None):
    parcel = fetch_one("SELECT ulpin FROM parcels WHERE ulpin = %s", (ulpin,))
    if not parcel:
        raise not_found("Parcel", ulpin)
    if service_type not in ALLOWED_TYPES:
        service_type = service_type or "LAND_RECORD_VERIFICATION"
    request_id = _next_request_id()
    row = execute(
        """
        INSERT INTO service_requests (request_id, ulpin, service_type, status, remarks)
        VALUES (%s, %s, %s, 'SUBMITTED', %s)
        RETURNING request_id, ulpin, service_type, status, remarks, submitted_date, last_updated
        """,
        (request_id, ulpin, service_type, remarks),
    )
    write_audit("citizen", "CREATE_SERVICE_REQUEST", ulpin, f"Created {request_id}")
    return _clean_row(row)


def get_request(request_id: str):
    row = fetch_one(
        """
        SELECT request_id, ulpin, service_type, status, remarks, submitted_date, last_updated
        FROM service_requests
        WHERE request_id = %s
        """,
        (request_id,),
    )
    if not row:
        raise not_found("Service request", request_id)
    return _clean_row(row)


def update_status(request_id: str, status: str, remarks: str | None, username: str):
    if status not in ALLOWED_STATUS:
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
    existing = get_request(request_id)
    row = execute(
        """
        UPDATE service_requests
        SET status = %s,
            remarks = COALESCE(%s, remarks),
            last_updated = NOW()
        WHERE request_id = %s
        RETURNING request_id, ulpin, service_type, status, remarks, submitted_date, last_updated
        """,
        (status, remarks, request_id),
    )
    write_audit(username, "UPDATE_REQUEST_STATUS", existing["ulpin"], f"{request_id} -> {status}")
    return _clean_row(row)
