export const CAMPUS_BOUNDS = [
  [25.2615, 82.9815],
  [25.2745, 83.0005],
];

export const CAMPUS_CENTER = [25.268, 82.991];

// Database geometry is intentionally synthetic. These source bounds are only used
// to position the demonstration overlay within the BHU map context in the browser.
const SYNTHETIC_SOURCE_BOUNDS = {
  minLat: 12.99,
  maxLat: 12.996,
  minLng: 77.58,
  maxLng: 77.588,
};

function projectCoordinate([lng, lat]) {
  const x = (lng - SYNTHETIC_SOURCE_BOUNDS.minLng) / (SYNTHETIC_SOURCE_BOUNDS.maxLng - SYNTHETIC_SOURCE_BOUNDS.minLng);
  const y = (lat - SYNTHETIC_SOURCE_BOUNDS.minLat) / (SYNTHETIC_SOURCE_BOUNDS.maxLat - SYNTHETIC_SOURCE_BOUNDS.minLat);
  const targetLng = CAMPUS_BOUNDS[0][1] + x * (CAMPUS_BOUNDS[1][1] - CAMPUS_BOUNDS[0][1]);
  const targetLat = CAMPUS_BOUNDS[0][0] + y * (CAMPUS_BOUNDS[1][0] - CAMPUS_BOUNDS[0][0]);
  return [targetLng, targetLat];
}

export function projectSyntheticFeature(feature) {
  if (!feature?.geometry?.coordinates) return feature;
  return {
    ...feature,
    geometry: {
      ...feature.geometry,
      coordinates: feature.geometry.coordinates.map((ring) => ring.map(projectCoordinate)),
    },
  };
}

export function categoryForFeature(properties = {}) {
  if (properties.campus_category) return properties.campus_category;
  const text = `${properties.land_type || ""} ${properties.land_use || ""}`.toLowerCase();
  if (/academic|lecture|library|lab|computer|book/.test(text)) return "Academic";
  if (/admin|auditorium/.test(text)) return "Administrative";
  if (/hostel|guest|staff|housing/.test(text)) return "Hostel";
  if (/sport|playground/.test(text)) return "Sports";
  if (/green|environment/.test(text)) return "Green Area";
  if (/residential/.test(text)) return "Residential";
  if (/facility|health|canteen|utility|parking|maintenance|water/.test(text)) return "Facilities";
  return "Other";
}

export function mapStatus(profile) {
  if (!profile) return "unavailable";
  if (profile.dispute?.status === "Disputed") return "disputed";
  if (profile.restriction?.status === "Restricted") return "restricted";
  if (profile.restriction?.status === "Mortgaged") return "mortgaged";
  if (profile.ownership?.status === "Pending") return "pending";
  if (profile.ownership?.status === "Verified") return "verified";
  return "unavailable";
}

export function featureStatus(props) {
  if (!props) return "unavailable";
  if (props.dispute_status === "Disputed") return "disputed";
  if (props.restriction_status === "Restricted") return "restricted";
  if (props.restriction_status === "Mortgaged") return "mortgaged";
  if (props.ownership_status === "Pending") return "pending";
  if (props.ownership_status === "Verified") return "verified";
  return "unavailable";
}

export const STATUS_COLORS = {
  verified: "#2f7d4a",
  pending: "#d4a017",
  disputed: "#c0392b",
  restricted: "#6c3483",
  mortgaged: "#1f618d",
  government: "#1a5276",
  unavailable: "#7f8c8d",
};

export const STATUS_LABELS = {
  verified: "Verified / Clear",
  pending: "Pending",
  disputed: "Disputed",
  restricted: "Restricted",
  mortgaged: "Mortgaged",
  government: "Government / Public",
  unavailable: "Data Unavailable",
};
