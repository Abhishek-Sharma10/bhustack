import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Home" },
  { to: "/services", label: "Service Request" },
  { to: "/tracking", label: "Tracking" },
  { to: "/admin", label: "Admin" },
  { to: "/interop", label: "Interop Demo" },
];

export function Navbar() {
  return (
    <header className="border-b border-earth-100 bg-white/90 backdrop-blur sticky top-0 z-[1000]">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3">
        <NavLink to="/" className="flex items-center gap-2 font-semibold text-earth-900">
          <span className="inline-flex h-8 w-8 items-center justify-center rounded bg-earth-800 text-white">B</span>
          BhuStack
        </NavLink>
        <nav className="flex flex-wrap gap-1 text-sm">
          {links.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              className={({ isActive }) =>
                `rounded-md px-3 py-1.5 ${isActive ? "bg-earth-800 text-white" : "text-slate-600 hover:bg-earth-50"}`
              }
            >
              {l.label}
            </NavLink>
          ))}
          <a
            href="/satellite_parcel_view.html"
            target="_blank"
            rel="noopener noreferrer"
            className="rounded-md px-3 py-1.5 bg-amber-600 hover:bg-amber-700 text-white font-medium flex items-center gap-1 transition-colors"
          >
            🛰️ Satellite View
          </a>
        </nav>
      </div>
    </header>
  );
}
