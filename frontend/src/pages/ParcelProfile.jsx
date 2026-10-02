import { useEffect } from "react";
import { Link, useParams } from "react-router-dom";
import { ProfilePanel } from "../components/ProfilePanel";
import { useParcel } from "../hooks/useParcel";

export default function ParcelProfile() {
  const { ulpin } = useParams();
  const { profile, loading, error, load } = useParcel();

  useEffect(() => {
    load(ulpin);
  }, [ulpin, load]);

  return (
    <div className="mx-auto max-w-3xl px-4 py-8">
      <a href="/satellite_parcel_view.html" target="_blank" rel="noopener noreferrer" className="text-sm text-earth-700">
        ← Open Satellite View
      </a>
      <h1 className="mt-3 text-2xl font-semibold">Unified Parcel Profile</h1>
      <p className="mb-4 text-sm text-slate-600">
        Loaded via GET /api/v1/parcels/{ulpin}
      </p>
      <ProfilePanel profile={profile} loading={loading} error={error} />
    </div>
  );
}
