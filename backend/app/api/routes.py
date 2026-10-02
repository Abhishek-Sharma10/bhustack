from fastapi import APIRouter, Depends, HTTPException, Query

from app.adapters.demo_state_adapter import DemoStateAdapter
from app.auth.security import create_token, require_admin, verify_password
from app.database.connection import fetch_one
from app.schemas.parcel import LoginRequest, ServiceRequestCreate, StatusUpdate, TokenOut
from app.services import parcel_service, request_service

router = APIRouter()
adapter = DemoStateAdapter()


@router.get("/health")
def health():
    try:
        row = fetch_one("SELECT COUNT(*) AS parcels FROM parcels")
        postgis = fetch_one("SELECT PostGIS_Version() AS version")
        return {
            "status": "ok",
            "service": "BhuStack",
            "parcels": row["parcels"] if row else 0,
            "postgis": postgis["version"] if postgis else None,
        }
    except Exception as exc:
        return {"status": "degraded", "error": str(exc)}


@router.get("/parcels")
def list_parcels():
    return parcel_service.list_parcels()


@router.get("/parcels/search")
def search_parcels(
    q: str | None = Query(default=None),
    ulpin: str | None = None,
    survey_number: str | None = None,
    parcel_number: str | None = None,
    state: str | None = None,
    district: str | None = None,
    village: str | None = None,
    block: str | None = None,
):
    term = q or ulpin or survey_number or parcel_number or state or district or village or block
    if not term:
        raise HTTPException(status_code=400, detail="Provide q, ulpin, survey_number, parcel_number, state, district, village, or block")
    return parcel_service.search_parcels(term)


@router.get("/gis/search")
def gis_search(q: str | None = Query(default=None), type: str = Query(default="ulpin")):
    term = (q or "").strip()
    area_type = (type or "ulpin").lower()
    if not term:
        raise HTTPException(status_code=400, detail="Provide q and type for GIS search")
    if area_type == "ulpin":
        profile = parcel_service.get_profile(term)
        return {
            "type": "parcel",
            "name": profile.ulpin,
            "label": profile.ulpin,
            "owner": profile.ownership.owner_name,
            "geometry": parcel_service.get_geojson_for_ulpin(profile.ulpin),
            "summary": {
                "state": profile.state,
                "district": profile.district,
                "block": profile.block,
                "village": profile.village,
                "parcels": 1,
            },
        }
    try:
        results = parcel_service.search_administrative_area(area_type, term)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if not results:
        raise HTTPException(status_code=404, detail=f"No {area_type} found for '{term}'")
    return {
        "type": area_type,
        "query": term,
        "count": len(results),
        "results": results,
    }


@router.get("/gis/parcel/{ulpin}")
def gis_parcel(ulpin: str):
    profile = parcel_service.get_profile(ulpin)
    return {
        "type": "parcel",
        "name": profile.ulpin,
        "owning": profile.ownership.owner_name,
        "summary": {
            "state": profile.state,
            "district": profile.district,
            "block": profile.block,
            "village": profile.village,
            "area": profile.area,
        },
        "geometry": parcel_service.get_geojson_for_ulpin(ulpin),
        "profile": profile,
    }


@router.get("/parcels/{ulpin}")
def get_parcel(ulpin: str):
    return parcel_service.get_profile(ulpin)


@router.get("/parcels/{ulpin}/ownership")
def get_ownership(ulpin: str):
    return parcel_service.get_child("ownership", ulpin)


@router.get("/parcels/{ulpin}/ror")
def get_ror(ulpin: str):
    return parcel_service.get_child("ror", ulpin)


@router.get("/parcels/{ulpin}/registration")
def get_registration(ulpin: str):
    return parcel_service.get_child("registrations", ulpin)


@router.get("/parcels/{ulpin}/land-use")
def get_land_use(ulpin: str):
    return parcel_service.get_child("land_use", ulpin)


@router.get("/parcels/{ulpin}/tax")
def get_tax(ulpin: str):
    return parcel_service.get_child("tax", ulpin)


@router.get("/parcels/{ulpin}/restrictions")
def get_restrictions(ulpin: str):
    return parcel_service.get_child("restrictions", ulpin)


@router.get("/parcels/{ulpin}/disputes")
def get_disputes(ulpin: str):
    return parcel_service.get_child("disputes", ulpin)


@router.get("/parcels/{ulpin}/building-permission")
def get_building_permission(ulpin: str):
    return parcel_service.get_child("building_permissions", ulpin)


@router.get("/geojson")
def get_geojson():
    return parcel_service.get_geojson()


@router.get("/admin/regions")
def get_admin_regions(region_type: str | None = Query(default=None, alias="type")):
    if region_type and region_type.lower() not in {"state", "district", "block", "village"}:
        raise HTTPException(status_code=400, detail="Unsupported administrative region type")
    return parcel_service.get_admin_regions(region_type.lower() if region_type else None)


@router.post("/service-requests", status_code=201)
def create_service_request(body: ServiceRequestCreate):
    return request_service.create_request(body.ulpin, body.service_type, body.remarks)


@router.get("/service-requests/{request_id}")
def get_service_request(request_id: str):
    return request_service.get_request(request_id)


@router.patch("/service-requests/{request_id}")
def patch_service_request(request_id: str, body: StatusUpdate, user=Depends(require_admin)):
    return request_service.update_status(request_id, body.status, body.remarks, user["sub"])


@router.get("/dashboard")
def dashboard():
    return parcel_service.dashboard_stats()


@router.get("/synthetic-government/parcels/{ulpin}")
def synthetic_government(ulpin: str):
    profile = parcel_service.get_profile(ulpin)
    return {
        "state": profile.state,
        "department": adapter.department,
        "ulpin": profile.ulpin,
        "khasra_no": profile.survey_number,
        "owner": profile.ownership.owner_name,
        "area_sq_m": profile.area,
        "land_category": profile.land_use,
        "disclaimer": "Synthetic demonstration payload. Not a live government land record.",
        "source_type": "SYNTHETIC",
    }


@router.get("/adapters/demo-state/parcels/{ulpin}")
def adapted_parcel(ulpin: str):
    gov = synthetic_government(ulpin)
    return adapter.to_common(gov)


@router.post("/auth/login", response_model=TokenOut)
def login(body: LoginRequest):
    row = fetch_one("SELECT username, password_hash, role FROM users WHERE username = %s", (body.username,))
    if not row or not verify_password(body.password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(row["username"], row["role"])
    return TokenOut(access_token=token, role=row["role"], username=row["username"])
