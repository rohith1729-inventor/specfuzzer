import type { CSSProperties } from "react";
import type { Finding } from "../types";

interface Props {
  findings: Finding[];
  loading: boolean;
}

const severityColors: Record<string, string> = {
  high: "#dc2626",
  medium: "#f97316",
  low: "#16a34a",
};

function TestResultsTable({ findings, loading }: Props) {
  if (loading) {
    return <p>Executing tests...</p>;
  }

  if (!findings.length) {
    return <p>No issues detected. 🎯</p>;
  }

  return (
    <div style={{ overflowX: "auto" }}>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ textAlign: "left", borderBottom: "1px solid #e2e8f0" }}>
            <th style={thStyle}>Endpoint</th>
            <th style={thStyle}>Method</th>
            <th style={thStyle}>Severity</th>
            <th style={thStyle}>Description</th>
            <th style={thStyle}>Expected</th>
            <th style={thStyle}>Actual</th>
            <th style={thStyle}>Status</th>
          </tr>
        </thead>
        <tbody>
          {findings.map((finding, index) => (
            <tr key={`${finding.endpoint}-${index}`} style={rowStyle}>
              <td style={tdStyle}>{finding.endpoint}</td>
              <td style={tdStyle}>{finding.method}</td>
              <td style={tdStyle}>
                <span
                  style={{
                    padding: "0.2rem 0.8rem",
                    borderRadius: "999px",
                    background: `${severityColors[finding.severity] ?? "#94a3b8"}20`,
                    color: severityColors[finding.severity] ?? "#334155",
                    fontWeight: 600,
                    fontSize: "0.85rem",
                  }}
                >
                  {finding.severity}
                </span>
              </td>
              <td style={tdStyle}>{finding.description}</td>
              <td style={tdStyle}>{finding.details.expected_status}</td>
              <td style={tdStyle}>{finding.details.actual_status ?? "–"}</td>
              <td style={tdStyle}>{finding.details.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const thStyle: CSSProperties = {
  padding: "0.75rem",
  fontSize: "0.85rem",
  color: "#64748b",
  textTransform: "uppercase",
  letterSpacing: "0.08em",
};

const tdStyle: CSSProperties = {
  padding: "0.85rem",
  borderBottom: "1px solid #e2e8f0",
};

const rowStyle: CSSProperties = {
  borderBottom: "1px solid #e2e8f0",
};

export default TestResultsTable;
