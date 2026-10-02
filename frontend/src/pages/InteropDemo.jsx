import { useState } from "react";
import { api } from "../services/api";

export default function InteropDemo() {
  const [ulpin, setUlpin] = useState("IND-DEMO-000001");
  const [gov, setGov] = useState(null);
  const [common, setCommon] = useState(null);
  const [error, setError] = useState("");

  async function run(e) {
    e.preventDefault();
    setError("");
    try {
      const [g, c] = await Promise.all([api.syntheticGov(ulpin), api.adapted(ulpin)]);
      setGov(g);
      setCommon(c);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-8">
      <h1 className="text-2xl font-semibold">Synthetic government API → DemoStateAdapter</h1>
      <p className="mt-2 text-sm text-slate-600">
        State departments may use khasra_no / owner / area_sq_m. The adapter maps those fields into the
        BhuStack common contract keyed by ULPIN.
      </p>
      <form onSubmit={run} className="mt-4 flex gap-2">
        <input className="rounded-lg border px-3 py-2" value={ulpin} onChange={(e) => setUlpin(e.target.value)} />
        <button className="rounded-lg bg-earth-800 px-4 py-2 text-white">Transform</button>
      </form>
      {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <pre className="overflow-auto rounded-xl border bg-slate-950 p-4 text-xs text-slate-100">
          {gov ? JSON.stringify(gov, null, 2) : "// Synthetic government payload"}
        </pre>
        <pre className="overflow-auto rounded-xl border bg-slate-950 p-4 text-xs text-slate-100">
          {common ? JSON.stringify(common, null, 2) : "// Common land schema after DemoStateAdapter"}
        </pre>
      </div>
      <p className="mt-6 text-sm text-amber-900 bg-amber-50 rounded-lg p-3">
        The government API shown in this prototype is synthetic. It demonstrates how authorized state or
        department APIs could be integrated in a future implementation.
      </p>
    </div>
  );
}
