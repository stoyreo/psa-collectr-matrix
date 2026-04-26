// Default to a relative URL so the browser hits Vercel's same-origin
// /api/[...path] proxy (web/src/app/api/[...path]/route.ts), which forwards
// server-side to the ngrok-tunneled Flask backend with the ngrok-skip-
// browser-warning header. Set NEXT_PUBLIC_API_BASE to override (e.g. for
// local dev pointing directly at http://localhost:5000).
const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? '';
const API_KEY = process.env.TRACER_API_KEY;

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

export async function fetchAPI<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  // API_BASE === '' is fine — it means "use Vercel's same-origin proxy".
  const url = `${API_BASE}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    // Bypass ngrok-free.dev abuse warning page which otherwise
    // intercepts the browser fetch and returns its HTML interstitial.
    'ngrok-skip-browser-warning': '1',
    ...(API_KEY && { 'X-Tracer-Key': API_KEY }),
    ...options.headers,
  };

  const response = await fetch(url, { ...options, headers });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.error || `API error: ${response.status}`);
  }

  return response.json();
}

export async function getPortfolio(): Promise<ApiResponse> {
  try {
    return await fetchAPI<ApiResponse>('/api/status');
  } catch (error) {
    // Fallback to snapshot when live backend is unreachable
    console.warn('Live backend unreachable, falling back to snapshot...', error);
    try {
      const snapshot = await fetch('/snapshot.json').then(r => r.json());
      return {
        ...snapshot,
        data_source: 'snapshot',
      };
    } catch (snapshotError) {
      console.error('Snapshot fallback also failed:', snapshotError);
      throw error; // Re-throw original error
    }
  }
}

export function refreshPortfolio() {
  return fetchAPI<ApiResponse>('/api/refresh', { method: 'POST' });
}
