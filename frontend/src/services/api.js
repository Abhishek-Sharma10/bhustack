const BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const message = data.detail || `Request failed (${res.status})`;
    throw new Error(typeof message === "string" ? message : JSON.stringify(message));
  }
  return data;
}

export const api = {
  health: () => request("/health"),
  parcels: () => request("/parcels"),
  parcel: (ulpin) => request(`/parcels/${encodeURIComponent(ulpin)}`),
  search: (q) => request(`/parcels/search?q=${encodeURIComponent(q)}`),
  geojson: () => request("/geojson"),
  ownership: (ulpin) => request(`/parcels/${encodeURIComponent(ulpin)}/ownership`),
  createRequest: (body) =>
    request("/service-requests", { method: "POST", body: JSON.stringify(body) }),
  getRequest: (id) => request(`/service-requests/${encodeURIComponent(id)}`),
  updateRequest: (id, body, token) =>
    request(`/service-requests/${encodeURIComponent(id)}`, {
      method: "PATCH",
      body: JSON.stringify(body),
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    }),
  dashboard: () => request("/dashboard"),
  syntheticGov: (ulpin) =>
    request(`/synthetic-government/parcels/${encodeURIComponent(ulpin)}`),
  adapted: (ulpin) =>
    request(`/adapters/demo-state/parcels/${encodeURIComponent(ulpin)}`),
  login: (username, password) =>
    request("/auth/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    }),
};

export { BASE as API_BASE };
