import { StatusBadge } from "./StatusBadge";

const Field = ({ label, value }) => <div><dt>{label}</dt><dd>{value || "—"}</dd></div>;
const Record = ({ label, status }) => <div><span>{label}</span><StatusBadge status={status} /></div>;

export function ProfilePanel({ profile, loading, error }) {
  if (loading) return <div className="gis-panel-state">Loading Unified Parcel Profile…</div>;
  if (error) return <div className="gis-panel-state error">{error}</div>;
  if (!profile) return <div className="gis-empty"><span>⌖</span><h2>Select a parcel</h2><p>Click a highlighted parcel or search by UL PIN, survey number, village, or district to view the parcel profile.</p></div>;

  return <section className="gis-profile">
    <header><div><p>Unified Parcel Profile</p><h2>{profile.ulpin}</h2></div><StatusBadge status={profile.ownership?.status} /></header>
    <div className="gis-profile-section"><h3>Basic information</h3><dl><Field label="UL PIN" value={profile.ulpin} /><Field label="Parcel number" value={profile.parcel_number} /><Field label="Survey number" value={profile.survey_number} /><Field label="Area" value={profile.area ? `${profile.area} sq.m` : null} /><Field label="State" value={profile.state} /><Field label="District" value={profile.district} /><Field label="Village" value={profile.village} /><Field label="Land use" value={profile.land_use || profile.land_type} /><Field label="Location" value={profile.village ? `${profile.village}, ${profile.district}, ${profile.state}` : "—"} /></dl></div>
    <div className="gis-profile-section"><h3>Ownership & record source</h3><dl><Field label="Owner" value={profile.ownership?.owner_name} /><Field label="Verification" value={profile.ownership?.status} /><Field label="Source" value={profile.source_type} /></dl></div>
    <div className="gis-profile-section"><h3>Records</h3><div className="gis-record-grid"><Record label="RoR" status={profile.ror_status} /><Record label="Registration" status={profile.registration?.status} /><Record label="Tax" status={profile.tax?.status} /><Record label="Building permit" status={profile.building_permission?.status} /></div></div>
    <div className="gis-profile-section"><h3>Risk & restrictions</h3><div className="gis-record-grid"><Record label="Restriction" status={profile.restriction?.status} /><Record label="Dispute" status={profile.dispute?.status} /></div></div>
  </section>;
}
