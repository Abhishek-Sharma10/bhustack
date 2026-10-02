import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { api } from "../services/api";

const TYPES = [
  "LAND_RECORD_VERIFICATION",
  "MUTATION_REQUEST",
  "TAX_CLARIFICATION",
  "BUILDING_PERMISSION_STATUS",
  "DISPUTE_STATUS_CHECK",
];

export default function ServiceRequest() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const [ulpin, setUlpin] = useState(params.get("ulpin") || "IND-DEMO-000001");
  const [serviceType, setServiceType] = useState(TYPES[0]);
  const [remarks, setRemarks] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      const data = await api.createRequest({
        ulpin,
        service_type: serviceType,
        remarks,
      });
      setResult(data);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="mx-auto max-w-xl px-4 py-8">
      <h1 className="text-2xl font-semibold">Citizen service request</h1>
      <p className="mt-1 text-sm text-slate-600">
        SUBMITTED → UNDER_REVIEW → APPROVED / REJECTED
      </p>
      <form onSubmit={onSubmit} className="mt-6 space-y-4 rounded-xl border bg-white p-5">
        <label className="block text-sm">
          ULPIN
          <input className="mt-1 w-full rounded-lg border px-3 py-2" value={ulpin} onChange={(e) => setUlpin(e.target.value)} />
        </label>
        <label className="block text-sm">
          Service type
          <select className="mt-1 w-full rounded-lg border px-3 py-2" value={serviceType} onChange={(e) => setServiceType(e.target.value)}>
            {TYPES.map((t) => (
              <option key={t}>{t}</option>
            ))}
          </select>
        </label>
        <label className="block text-sm">
          Remarks
          <textarea className="mt-1 w-full rounded-lg border px-3 py-2" rows="3" value={remarks} onChange={(e) => setRemarks(e.target.value)} />
        </label>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <button className="rounded-lg bg-earth-800 px-4 py-2 text-white" type="submit">
          Submit request
        </button>
      </form>
      {result && (
        <div className="mt-4 rounded-xl border bg-green-50 p-4 text-sm">
          <p>
            Created <strong>{result.request_id}</strong> with status <strong>{result.status}</strong>
          </p>
          <button
            className="mt-2 text-earth-800 underline"
            onClick={() => navigate(`/tracking?id=${result.request_id}`)}
          >
            Track this application
          </button>
        </div>
      )}
    </div>
  );
}
