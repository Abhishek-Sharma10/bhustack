from datetime import date, datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class OwnershipBlock(BaseModel):
    owner_name: Optional[str] = None
    status: Optional[str] = None


class RegistrationBlock(BaseModel):
    status: Optional[str] = None
    registration_date: Optional[date] = None


class TaxBlock(BaseModel):
    status: Optional[str] = None
    last_payment_date: Optional[date] = None


class RestrictionBlock(BaseModel):
    status: Optional[str] = None
    type: Optional[str] = None


class DisputeBlock(BaseModel):
    status: Optional[str] = None
    description: Optional[str] = None


class BuildingPermissionBlock(BaseModel):
    status: Optional[str] = None


class UnifiedParcelProfile(BaseModel):
    ulpin: str
    survey_number: str
    parcel_number: str
    area: float
    state: str
    district: str
    block: Optional[str] = None
    village: str
    land_use: Optional[str] = None
    ownership: OwnershipBlock
    registration: RegistrationBlock
    tax: TaxBlock
    restriction: RestrictionBlock
    dispute: DisputeBlock
    building_permission: BuildingPermissionBlock
    ror_status: Optional[str] = None
    zoning: Optional[str] = None
    source_type: str = "SYNTHETIC"
    land_type: Optional[str] = None


class ParcelSummary(BaseModel):
    ulpin: str
    survey_number: str
    parcel_number: str
    area: float
    village: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    land_use: Optional[str] = None
    ownership_status: Optional[str] = None


class ServiceRequestCreate(BaseModel):
    ulpin: str = Field(..., examples=["IND-DEMO-000001"])
    service_type: str = Field(..., examples=["LAND_RECORD_VERIFICATION"])
    remarks: Optional[str] = None


class ServiceRequestOut(BaseModel):
    request_id: str
    ulpin: str
    service_type: str
    status: str
    remarks: Optional[str] = None
    submitted_date: datetime
    last_updated: datetime


class StatusUpdate(BaseModel):
    status: str
    remarks: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str


def row_to_profile(row: dict[str, Any]) -> UnifiedParcelProfile:
    return UnifiedParcelProfile(
        ulpin=row["ulpin"],
        survey_number=row["survey_number"],
        parcel_number=row["parcel_number"],
        area=float(row["area"]),
        state=row["state"],
        district=row["district"],
        block=row.get("block"),
        village=row["village"],
        land_use=row.get("land_use"),
        ownership=OwnershipBlock(
            owner_name=row.get("owner_name"),
            status=row.get("ownership_status"),
        ),
        registration=RegistrationBlock(
            status=row.get("registration_status"),
            registration_date=row.get("registration_date"),
        ),
        tax=TaxBlock(
            status=row.get("tax_status"),
            last_payment_date=row.get("last_payment_date"),
        ),
        restriction=RestrictionBlock(
            status=row.get("restriction_status"),
            type=row.get("restriction_type"),
        ),
        dispute=DisputeBlock(
            status=row.get("dispute_status"),
            description=row.get("dispute_description"),
        ),
        building_permission=BuildingPermissionBlock(
            status=row.get("building_permission_status"),
        ),
        ror_status=row.get("ror_status"),
        zoning=row.get("zoning"),
        source_type=row.get("source_type") or "SYNTHETIC",
        land_type=row.get("land_type"),
    )
