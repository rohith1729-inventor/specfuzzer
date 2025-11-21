export interface SeverityBreakdown {
  high?: number;
  medium?: number;
  low?: number;
  [key: string]: number | undefined;
}

export interface Summary {
  tests: number;
  issues: number;
  severity: SeverityBreakdown;
}

export interface FindingDetails {
  expected_status: number;
  actual_status?: number | null;
  status: string;
  error?: string | null;
  payload: Record<string, unknown>;
}

export interface Finding {
  endpoint: string;
  method: string;
  severity: string;
  description: string;
  details: FindingDetails;
}

export interface Report {
  summary: Summary;
  findings: Finding[];
}
