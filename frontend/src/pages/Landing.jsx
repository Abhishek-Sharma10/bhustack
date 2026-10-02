import { Link } from "react-router-dom";

export default function Landing() {
  return (
    <div className="mx-auto max-w-6xl px-4 py-12">
      <p className="text-sm font-medium text-clay">Digital Public Infrastructure · Land Governance</p>
      <h1 className="mt-2 max-w-3xl text-4xl font-semibold leading-tight text-earth-900">
        BhuStack — One Parcel. One Identity. Complete Land Intelligence.
      </h1>
      <p className="mt-4 max-w-2xl text-slate-600">
        A land governance prototype that connects parcel records to administrative GIS context and
        parcel-level intelligence through a common <strong>ULPIN</strong>.
      </p>
      <div className="mt-6 flex flex-wrap gap-3">
        <a href="/satellite_parcel_view.html" target="_blank" rel="noopener noreferrer" className="rounded-lg bg-earth-800 px-4 py-2 text-white">
          Open Satellite View
        </a>
        <Link to="/interop" className="rounded-lg border border-earth-800 px-4 py-2 text-earth-800">
          See interoperability
        </Link>
      </div>
      <div className="mt-10 grid gap-4 md:grid-cols-3">
        {[
          ["Search", "ULPIN, survey number, or parcel number"],
          ["GIS + ULPIN", "Parcel geometry on live satellite imagery"],
          ["Unified profile", "Ownership, RoR, tax, disputes, permissions, and admin context"],
        ].map(([t, d]) => (
          <div key={t} className="rounded-xl border bg-white p-4">
            <h2 className="font-semibold">{t}</h2>
            <p className="mt-1 text-sm text-slate-600">{d}</p>
          </div>
        ))}
      </div>
      <p className="mt-10 rounded-lg bg-amber-50 p-3 text-sm text-amber-900">
        This app uses the existing BhuStack Postgres/PostGIS data model and the authoritative
        satellite parcel viewer as the primary GIS workflow.
      </p>
    </div>
  );
}
