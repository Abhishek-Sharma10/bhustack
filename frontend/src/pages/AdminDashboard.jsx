import { useEffect, useState } from "react";
import { api } from "../services/api";
import { StatusBadge } from "../components/StatusBadge";

function BarList({ items }) {
  const max = Math.max(...items.map((i) => Number(i.count)), 1);
  return (
    <div className="space-y-2">
      {items.map((i) => (
        <div key={i.label}>
          <div className="mb-1 flex justify-between text-xs">
            <span>{i.label}</span>
            <span>{i.count}</span>
          </div>
          <div className="h-2 rounded bg-slate-100">
            <div className="h-2 rounded bg-earth-700" style={{ width: `${(Number(i.count) / max) * 100}%` }} />
          </div>
        </div>
      ))}
    </div>
  );
}

export default function AdminDashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [advanceId, setAdvanceId] = useState("");
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("admin123");
  const [token, setToken] = useState("");
  const [authError, setAuthError] = useState("");

  useEffect(() => {
    api.dashboard().then(setData).catch((err) => setError(err.message));
  }, []);

  async function advance(status) {
    if (!advanceId) return;
    setAuthError("");
    try {
      await api.updateRequest(advanceId, { status }, token);
      setData(await api.dashboard());
    } catch (err) {
      setAuthError(err.message);
    }
  }

  async function login(e) {
    e.preventDefault();
    setAuthError("");
    try {
      const result = await api.login(username, password);
      if (result.role !== "ADMIN") throw new Error("An ADMIN account is required to update request status.");
      setToken(result.access_token);
    } catch (err) {
      setToken("");
      setAuthError(err.message);
    }
  }

  if (error) return <p className="p-8 text-red-600">{error}</p>;
  if (!data) return <p className="p-8 text-slate-500">Loading dashboard…</p>;

  const cards = [
    ["Total parcels", data.total_parcels],
    ["Verified parcels", data.verified_parcels],
    ["Pending requests", data.pending_requests],
    ["Disputed parcels", data.disputed_parcels],
    ["Restricted parcels", data.restricted_parcels],
  ];

  return (
    <div className="mx-auto max-w-6xl px-4 py-8">
      <h1 className="text-2xl font-semibold">Admin dashboard</h1>
      <p className="text-sm text-slate-600">Synthetic campus statistics — not live government metrics.</p>
      <form onSubmit={login} className="mt-4 flex flex-wrap items-end gap-2 rounded-xl border bg-slate-50 p-3 text-sm">
        <label>Admin username<input className="ml-2 rounded border px-2 py-1" value={username} onChange={(e) => setUsername(e.target.value)} /></label>
        <label>Password<input className="ml-2 rounded border px-2 py-1" type="password" value={password} onChange={(e) => setPassword(e.target.value)} /></label>
        <button className="rounded bg-slate-800 px-3 py-1 text-white" type="submit">{token ? "Admin authenticated" : "Authenticate"}</button>
        <span className="text-xs text-slate-500">Local demo credentials only.</span>
      </form>
      {authError && <p className="mt-2 text-sm text-red-600">{authError}</p>}
      <div className="mt-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
        {cards.map(([l, v]) => (
          <div key={l} className="rounded-xl border bg-white p-4">
            <p className="text-xs text-slate-500">{l}</p>
            <p className="text-2xl font-semibold">{v}</p>
          </div>
        ))}
      </div>
      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <section className="rounded-xl border bg-white p-4">
          <h2 className="mb-3 font-medium">Land use distribution</h2>
          <BarList items={data.land_use_distribution} />
        </section>
        <section className="rounded-xl border bg-white p-4">
          <h2 className="mb-3 font-medium">Tax status distribution</h2>
          <BarList items={data.tax_status_distribution} />
        </section>
      </div>
      <section className="mt-6 rounded-xl border bg-white p-4">
        <h2 className="mb-3 font-medium">Recent requests</h2>
        <div className="overflow-x-auto text-sm">
          <table className="w-full">
            <thead className="text-left text-slate-500">
              <tr>
                <th className="py-1">ID</th>
                <th>ULPIN</th>
                <th>Type</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {data.recent_requests.map((r) => (
                <tr key={r.request_id} className="border-t">
                  <td className="py-2">{r.request_id}</td>
                  <td>{r.ulpin}</td>
                  <td>{r.service_type}</td>
                  <td><StatusBadge status={r.status} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="mt-4 flex flex-wrap items-center gap-2 text-sm">
          <input
            className="rounded border px-2 py-1"
            placeholder="REQ-000001"
            value={advanceId}
            onChange={(e) => setAdvanceId(e.target.value)}
          />
          <button className="rounded bg-sky-700 px-3 py-1 text-white" onClick={() => advance("UNDER_REVIEW")}>
            Mark under review
          </button>
          <button className="rounded bg-green-700 px-3 py-1 text-white" onClick={() => advance("APPROVED")}>
            Approve
          </button>
          <button className="rounded bg-red-700 px-3 py-1 text-white" onClick={() => advance("REJECTED")}>
            Reject
          </button>
        </div>
        {!token && <p className="mt-2 text-xs text-slate-500">Authenticate as an admin before changing a request status.</p>}
      </section>
    </div>
  );
}
