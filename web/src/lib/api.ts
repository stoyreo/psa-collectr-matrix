/**
 * Static snapshot client — reads from /snapshot.json (same-origin, no backend required).
 * No Flask. No ngrok. No CORS. Pure static.
 */

export interface Portfolio {
  subject: string;
  grade: string;
  card_number: string;
  market_value: number;
  my_cost: number;
  pnl: number;
  pnl_pct: number;
  signal: 'BUY' | 'SELL' | 'HOLD' | 'REVIEW';
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH';
  confidence: number;
  collectr_url?: string;
  [key: string]: any;
}

export interface ApiResponse {
  status: string;
  portfolio: Portfolio[];
  summary: {
    card_count: number;
    total_cost: number;
    total_market_value: number;
    total_pnl: number;
    pnl_pct: number;
    signal_distribution: Record<string, number>;
  };
  ts_display: string;
  data_source: 'live' | 'snapshot';
}

export async function getPortfolio(): Promise<ApiResponse> {
  const response = await fetch('/snapshot.json');
  if (!response.ok) {
    throw new Error(`Failed to load snapshot: ${response.status}`);
  }
  return response.json();
}

/**
 * Snapshot is static — re-fetch the JSON without full page reload.
 * To update, user must run REFRESH_AND_PUSH.bat locally.
 */
export function refreshPortfolio() {
  return getPortfolio();
}
