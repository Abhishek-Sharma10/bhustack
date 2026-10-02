import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { ParcelMap } from "../map/ParcelMap";
import { ProfilePanel } from "../components/ProfilePanel";
import { useParcel } from "../hooks/useParcel";
import { api } from "../services/api";
import { categoryForFeature, featureStatus, STATUS_COLORS, STATUS_LABELS } from "../utils/status";

const FILTERS = ["All", "Academic", "Administrative", "Hostel", "Sports", "Facilities", "Green Area", "Residential", "Other"];
const Metric = ({ label, value, detail }) => <div className="gis-metric"><small>{label}</small><strong>{value}</strong><span>{detail}</span></div>;

export default function GisExplorer() {
  const [params, setParams] = useSearchParams();
  const navigate = useNavigate();
  const [query, setQuery] = useState(params.get("q") || "");
  const [geojson, setGeojson] = useState(null);
  const [parcelSummaries, setParcelSummaries] = useState([]);
  const [selected, setSelected] = useState(params.get("ulpin") || "");
  const [filter, setFilter] = useState("All");
  const [tab, setTab] = useState("details");
  const [message, setMessage] = useState("");
  const [mapStyle, setMapStyle] = useState("map");
  const [showCampus, setShowCampus] = useState(true);
  const [showParcels, setShowParcels] = useState(true);
  const [resetSignal, setResetSignal] = useState(0);
  const [focusSignal, setFocusSignal] = useState(0);
  const { profile, loading, error, load } = useParcel();

  useEffect(() => { Promise.all([api.geojson(), api.parcels()]).then(([mapData, summaries]) => { setGeojson(mapData); setParcelSummaries(summaries); }).catch((err) => setMessage(`Map data could not be loaded: ${err.message}`)); }, []);
  useEffect(() => { const ulpin = params.get("ulpin"); if (ulpin) { setSelected(ulpin); load(ulpin); } }, [params, load]);

  const features = useMemo(() => geojson?.features || [], [geojson]);
  const visible = useMemo(() => features.filter((f) => filter === "All" || categoryForFeature(f.properties) === filter), [features, filter]);
  const totalArea = useMemo(() => parcelSummaries.reduce((sum, parcel) => sum + Number(parcel.area || 0), 0), [parcelSummaries]);
  const categories = useMemo(() => [...new Set(features.map((feature) => categoryForFeature(feature.properties)))].map((label) => ({ label, count: features.filter((feature) => categoryForFeature(feature.properties) === label).length })).sort((a, b) => b.count - a.count), [features]);
  const statuses = useMemo(() => Object.keys(STATUS_LABELS).map((status) => ({ status, count: features.filter((f) => featureStatus(f.properties) === status).length })).filter((x) => x.count), [features]);

  async function choose(ulpin, q = ulpin) { setMessage(""); setSelected(ulpin); setParams({ ulpin, q }); await load(ulpin); }
  async function search(event) {
    event.preventDefault(); const term = query.trim(); if (!term) return; setMessage("");
    const localMatch = features.find((feature) => {
      const props = feature.properties || {};
      const haystack = [props.ulpin, props.survey_number, props.parcel_number, props.state, props.district, props.village, props.land_use, props.land_type].join(" ").toLowerCase();
      return haystack.includes(term.toLowerCase());
    });
    if (localMatch) return choose(localMatch.properties.ulpin, term);
    try { const results = await api.search(term); if (!results.length) return setMessage("No parcel matched that search."); await choose(results[0].ulpin, term); } catch (err) { setMessage(err.message); }
  }

  function toggleFullscreen() {
    const element = document.querySelector(".gis-map-stage");
    if (!document.fullscreenElement) element?.requestFullscreen?.();
    else document.exitFullscreen?.();
  }

  return <main className="gis-shell"><section className="gis-workspace">
    <div className="gis-map-stage">
      <ParcelMap geojson={showParcels ? geojson : null} selectedUlpin={selected} onSelect={choose} activeFilter={filter} showCampus={showCampus} mapStyle={mapStyle} resetSignal={resetSignal} focusSignal={focusSignal} />
      <div className="gis-topbar"><form onSubmit={search} className="gis-search"><span>⌕</span><input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search UL PIN, parcel number or building" /><button>Search</button></form>{message && <p className="gis-inline-error">{message}</p>}<div className="gis-filter-row">{FILTERS.map((item) => <button key={item} onClick={() => setFilter(item)} className={filter === item ? "active" : ""}>{item}</button>)}</div></div>
      <div className="gis-map-title"><i /><div><strong>BhuStack GIS</strong><small>Administrative parcel map · live GeoJSON layer</small></div></div>
      <div className="gis-legend">{Object.entries(STATUS_LABELS).map(([key, label]) => <span key={key}><i style={{ background: STATUS_COLORS[key] }} />{label}</span>)}</div>
      <div className="gis-actions"><button onClick={() => setResetSignal((n) => n + 1)} title="Reset campus view">⌖</button><button disabled={!selected} onClick={() => setFocusSignal((n) => n + 1)} title="Focus selected parcel">⌗</button><button onClick={toggleFullscreen} title="Fullscreen map">⛶</button><button onClick={() => setMapStyle(mapStyle === "map" ? "satellite" : "map")}>{mapStyle === "map" ? "Satellite" : "Map"}</button></div><div className="gis-note">State / district / village / parcel boundary data from the live BhuStack database · © OpenStreetMap contributors</div>
    </div>
    <aside className="gis-drawer"><header className="gis-drawer-head"><p>BhuStack Campus Land Information</p><h1>Banaras Hindu University</h1><span>Varanasi, Uttar Pradesh, India</span></header>
      <div className="gis-metrics"><Metric label="Parcels" value={features.length || "—"} detail="Live database" /><Metric label="Parcel area" value={totalArea ? `${Math.round(totalArea / 1000) / 10} ha` : "—"} detail="Recorded parcel area" /><Metric label="Zones" value={categories.length || "—"} detail="Land-use categories" /><Metric label="Green area" value={categories.find((x) => x.label === "Green Area")?.count || 0} detail="Mapped parcels" /></div>
      <nav className="gis-tabs"><button onClick={() => setTab("details")} className={tab === "details" ? "active" : ""}>Parcel Details</button><button onClick={() => setTab("layers")} className={tab === "layers" ? "active" : ""}>Layers</button><button onClick={() => setTab("analytics")} className={tab === "analytics" ? "active" : ""}>Analytics</button></nav>
      <div className="gis-drawer-content">
        {tab === "details" && <><ProfilePanel profile={profile} loading={loading} error={error} />{!profile && !loading && !error && <div className="gis-parcel-list"><p>Available parcels</p>{visible.map((f) => <button key={f.properties.ulpin} onClick={() => choose(f.properties.ulpin)}><i style={{ background: STATUS_COLORS[featureStatus(f.properties)] }} /><span><strong>{f.properties.ulpin}</strong><small>{[f.properties.village, f.properties.district].filter(Boolean).join(", ") || f.properties.land_use || "Parcel"}</small></span><b>›</b></button>)}</div>}{profile && <div className="gis-profile-actions"><Link to={`/profile/${profile.ulpin}`}>Full profile</Link><button onClick={() => navigate(`/services?ulpin=${profile.ulpin}`)}>Request service</button></div>}</>}
        {tab === "layers" && <div className="gis-layer-list"><p>Administrative boundary and parcel overlays from the live BhuStack record set.</p><label>Boundary overlay<input type="checkbox" checked={showCampus} onChange={(e) => setShowCampus(e.target.checked)} /></label><label>Parcel layer<input type="checkbox" checked={showParcels} onChange={(e) => setShowParcels(e.target.checked)} /></label>{categories.map(({ label, count }) => <button key={label} onClick={() => setFilter(filter === label ? "All" : label)} className={filter === label ? "selected" : ""}>{label}<span>{count}</span></button>)}</div>}
        {tab === "analytics" && <div className="gis-analytics"><p>Area by category</p>{categories.map((x) => <div className="gis-bar" key={x.label}><span>{x.label}</span><i><b style={{ width: `${(x.count / Math.max(features.length, 1)) * 100}%` }} /></i><strong>{x.count}</strong></div>)}<p>Parcel status</p>{statuses.map((x) => <div className="gis-bar" key={x.status}><span>{STATUS_LABELS[x.status]}</span><i><b style={{ width: `${(x.count / Math.max(features.length, 1)) * 100}%`, background: STATUS_COLORS[x.status] }} /></i><strong>{x.count}</strong></div>)}<small>Calculated from the current live parcel GeoJSON response.</small></div>}
      </div>
    </aside>
  </section></main>;
}
