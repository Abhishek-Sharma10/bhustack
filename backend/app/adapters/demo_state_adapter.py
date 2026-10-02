"""Maps fictional state/department field names into the BhuStack common contract."""


STATE_TO_COMMON = {
    "khasra_no": "survey_number",
    "owner": "owner_name",
    "area_sq_m": "area",
    "land_category": "land_use",
}


class DemoStateAdapter:
    department = "Demo Land Records Department"
    state_name = "Demo State"

    def to_common(self, government_payload: dict) -> dict:
        mapped = {
            "ulpin": government_payload.get("ulpin"),
            "survey_number": government_payload.get("khasra_no"),
            "owner_name": government_payload.get("owner"),
            "area": government_payload.get("area_sq_m"),
            "land_use": government_payload.get("land_category"),
            "state": government_payload.get("state") or self.state_name,
            "source_type": "SYNTHETIC",
            "adapter": "DemoStateAdapter",
            "field_map": STATE_TO_COMMON,
        }
        return mapped
