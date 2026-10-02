import { useState } from "react";
import { useSearchParams } from "react-router-dom";
import { api } from "../services/api";
import { StatusBadge } from "../components/StatusBadge";

export default function ApplicationTracking() {
  const [params] = useSearchParams();
  const [id, setId] = useState(params.get("id") || "REQ-000001");
  const [item, setItem] = useState(null);
  const [error, setError] = useState("");

  async function lookup(e) {
    e.preventDefault();
    setError("");
    try {
      setItem(await api.getRequest(id.trim()));
    } catch (err) {
      setItem(null);
      setError(err.message);
    }
  }

  return (
    <div className="mx-auto max-w-xl px-4 py-8">
      <h1 className="text-2xl font-semibold">Application tracking</h1>
      <form onSubmit={lookup} className="mt-4 flex gap-2">
        <input className="flex-1 rounded-lg border px-3 py-2" value={id} onChange={(e) => setId(e.target.value)} />
        <button className="rounded-lg bg-earth-800 px-4 py-2 text-white" type="submit">
          Track
        </button>
      </form>
      {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
      {item && (
        <dl className="mt-6 space-y-2 rounded-xl border bg-white p-5 text-sm">
          <div className="flex justify-between"><dt>Request ID</dt><dd className="font-medium">{item.request_id}</dd></div>
          <div className="flex justify-between"><dt>ULPIN</dt><dd>{item.ulpin}</dd></div>
          <div className="flex justify-between"><dt>Service type</dt><dd>{item.service_type}</dd></div>
          <div className="flex justify-between"><dt>Status</dt><dd><StatusBadge status={item.status} /></dd></div>
          <div className="flex justify-between"><dt>Submitted</dt><dd>{new Date(item.submitted_date).toLocaleString()}</dd></div>
          <div className="flex justify-between"><dt>Last updated</dt><dd>{new Date(item.last_updated).toLocaleString()}</dd></div>
          <div><dt className="text-slate-500">Remarks</dt><dd>{item.remarks || "—"}</dd></div>
        </dl>
      )}
    </div>
  );
}
