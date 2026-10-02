export function StatusBadge({ status }) {
  const map = {
    verified: "bg-green-100 text-green-800",
    Verified: "bg-green-100 text-green-800",
    Paid: "bg-green-100 text-green-800",
    Registered: "bg-green-100 text-green-800",
    Approved: "bg-green-100 text-green-800",
    Issued: "bg-green-100 text-green-800",
    None: "bg-slate-100 text-slate-700",
    pending: "bg-amber-100 text-amber-800",
    Pending: "bg-amber-100 text-amber-800",
    SUBMITTED: "bg-amber-100 text-amber-800",
    UNDER_REVIEW: "bg-sky-100 text-sky-800",
    APPROVED: "bg-green-100 text-green-800",
    REJECTED: "bg-red-100 text-red-800",
    disputed: "bg-red-100 text-red-800",
    Disputed: "bg-red-100 text-red-800",
    restricted: "bg-purple-100 text-purple-800",
    Restricted: "bg-purple-100 text-purple-800",
    Mortgaged: "bg-blue-100 text-blue-800",
    Overdue: "bg-red-100 text-red-800",
    "Not Applied": "bg-slate-100 text-slate-600",
  };
  const cls = map[status] || "bg-slate-100 text-slate-700";
  return <span className={`status-chip ${cls}`}>{status || "—"}</span>;
}
