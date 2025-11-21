import type { Summary } from "../types";

interface Props {
  summary: Summary;
  loading: boolean;
}

function SummaryPanel({ summary, loading }: Props) {
  return (
    <div style={{ display: "flex", gap: "2rem", flexWrap: "wrap" }}>
      <SummaryTile label="Tests" value={summary.tests} loading={loading} />
      <SummaryTile label="Issues" value={summary.issues} loading={loading} />
      <SummaryTile
        label="High Severity"
        value={summary.severity.high ?? 0}
        loading={loading}
      />
      <SummaryTile
        label="Medium Severity"
        value={summary.severity.medium ?? 0}
        loading={loading}
      />
      <SummaryTile
        label="Low Severity"
        value={summary.severity.low ?? 0}
        loading={loading}
      />
    </div>
  );
}

interface TileProps {
  label: string;
  value: number;
  loading: boolean;
}

function SummaryTile({ label, value, loading }: TileProps) {
  return (
    <div
      style={{
        flex: "1 1 160px",
        padding: "1rem 1.25rem",
        borderRadius: "12px",
        background: "#f1f5f9",
      }}
    >
      <p style={{ margin: 0, color: "#64748b", fontSize: "0.9rem" }}>{label}</p>
      <strong style={{ fontSize: "2rem" }}>{loading ? "…" : value}</strong>
    </div>
  );
}

export default SummaryPanel;
