import { useEffect, useMemo } from "react";
import { GeoJSON, MapContainer, Rectangle, TileLayer, useMap } from "react-leaflet";
import { CAMPUS_BOUNDS, CAMPUS_CENTER, categoryForFeature, featureStatus, STATUS_COLORS } from "../utils/status";

function FitSelected({ feature, focusSignal }) {
  const map = useMap();
  useEffect(() => {
    if (!focusSignal || !feature?.geometry?.coordinates) return;
    const ring = feature.geometry.coordinates[0];
    const lats = ring.map((c) => c[1]);
    const lngs = ring.map((c) => c[0]);
    map.fitBounds(
      [
        [Math.min(...lats), Math.min(...lngs)],
        [Math.max(...lats), Math.max(...lngs)],
      ],
      { maxZoom: 18, padding: [24, 24] }
    );
  }, [feature, focusSignal, map]);
  return null;
}

function ResetCampus({ resetSignal }) {
  const map = useMap();
  useEffect(() => {
    if (resetSignal) map.setView(CAMPUS_CENTER, 16);
  }, [map, resetSignal]);
  return null;
}

export function ParcelMap({ geojson, selectedUlpin, onSelect, activeFilter = "All", showCampus = true, mapStyle = "map", resetSignal, focusSignal }) {
  const projectedGeojson = useMemo(() => ({
    type: "FeatureCollection",
    features: (geojson?.features || []).filter(
      (feature) => activeFilter === "All" || categoryForFeature(feature.properties) === activeFilter
    ),
  }), [geojson, activeFilter]);

  const selectedFeature = useMemo(() => {
    return projectedGeojson.features.find((f) => f.properties?.ulpin === selectedUlpin) || null;
  }, [projectedGeojson, selectedUlpin]);

  function style(feature) {
    const status = featureStatus(feature.properties);
    const selected = feature.properties?.ulpin === selectedUlpin;
    return {
      color: selected ? "#111827" : STATUS_COLORS[status],
      weight: selected ? 3 : 1.1,
      fillColor: STATUS_COLORS[status],
      fillOpacity: selected ? 0.5 : 0.2,
    };
  }

  function onEachFeature(feature, layer) {
    const props = feature.properties || {};
    const label = [props.village, props.district, props.state].filter(Boolean).join(", ") || props.land_use || props.ulpin;
    layer.bindTooltip(`<strong>${props.ulpin}</strong><br/>${label}`, { sticky: true, direction: "top" });
    layer.on("click", () => onSelect(props.ulpin));
  }

  return (
    <MapContainer
      center={CAMPUS_CENTER}
      zoom={16}
      className="h-full min-h-[560px] w-full"
      maxBounds={CAMPUS_BOUNDS}
      scrollWheelZoom
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url={mapStyle === "satellite"
          ? "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
          : "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"}
        opacity={1}
      />
      {showCampus && <Rectangle bounds={CAMPUS_BOUNDS} pathOptions={{ color: "#1c4b36", weight: 2, dashArray: "6 5", fillOpacity: 0.025 }} />}
      {geojson && (
        <GeoJSON
          key={`${selectedUlpin || "all"}-${activeFilter}`}
          data={projectedGeojson}
          style={style}
          onEachFeature={onEachFeature}
        />
      )}
      <FitSelected feature={selectedFeature} focusSignal={focusSignal} />
      <ResetCampus resetSignal={resetSignal} />
    </MapContainer>
  );
}
