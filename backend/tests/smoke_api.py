"""Lightweight black-box smoke test for a running local BhuStack API.

Run after loading the synthetic database and starting Uvicorn:
    python tests/smoke_api.py
"""

import json
import urllib.error
import urllib.request


BASE_URL = "http://localhost:8000/api/v1"


def request(path, method="GET", body=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=json.dumps(body).encode() if body else None,
        headers=headers,
        method=method,
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())


def expected_error(path, method, body, token, status):
    try:
        request(path, method, body, token)
    except urllib.error.HTTPError as error:
        assert error.code == status, f"Expected {status}, got {error.code}"
        return
    raise AssertionError(f"Expected HTTP {status}")


def main():
    assert request("/health")["status"] == "ok"
    assert len(request("/parcels")) == 32
    assert request("/parcels/search?q=IND-DEMO-000015")[0]["ulpin"] == "IND-DEMO-000015"
    assert request("/parcels/IND-DEMO-000001")["ulpin"] == "IND-DEMO-000001"
    assert len(request("/geojson")["features"]) == 32
    assert request("/dashboard")["total_parcels"] == 32

    government = request("/synthetic-government/parcels/IND-DEMO-000001")
    adapted = request("/adapters/demo-state/parcels/IND-DEMO-000001")
    assert government["khasra_no"] == adapted["survey_number"]

    created = request(
        "/service-requests",
        "POST",
        {"ulpin": "IND-DEMO-000030", "service_type": "LAND_RECORD_VERIFICATION", "remarks": "Local smoke test"},
    )
    request_id = created["request_id"]
    assert request(f"/service-requests/{request_id}")["status"] == "SUBMITTED"

    admin = request("/auth/login", "POST", {"username": "admin", "password": "admin123"})
    citizen = request("/auth/login", "POST", {"username": "citizen", "password": "citizen123"})
    patch_path = f"/service-requests/{request_id}"
    expected_error(patch_path, "PATCH", {"status": "UNDER_REVIEW"}, None, 401)
    expected_error(patch_path, "PATCH", {"status": "UNDER_REVIEW"}, citizen["access_token"], 403)
    assert request(patch_path, "PATCH", {"status": "UNDER_REVIEW"}, admin["access_token"])["status"] == "UNDER_REVIEW"
    print(f"Smoke test passed: {request_id}")


if __name__ == "__main__":
    main()
