# Phase C.3 Quick Start — Create Next.js Project

**ngrok URL:** `https://automated-crummiest-puritan.ngrok-free.dev`  
**Status:** Ready to scaffold

---

## Step 1: Create Next.js 14 App (PowerShell)

```powershell
cd "PSA x Collectr Tracer"
npx create-next-app@latest web --ts --tailwind --eslint --app --src-dir --import-alias "@/*"
cd web
npm install -D @tanstack/react-query @tanstack/react-table recharts lucide-react zod
```

Choose these options when prompted:
```
✔ TypeScript? › Yes
✔ ESLint? › Yes
✔ Tailwind CSS? › Yes
✔ Use app router? › Yes
✔ Use src/ directory? › Yes
✔ Import alias? › @/*
✔ Would you like to use Turbopack? › No
```

---

## Step 2: Create `.env.local` File

**File:** `web/.env.local`

```env
NEXT_PUBLIC_API_BASE=https://automated-crummiest-puritan.ngrok-free.dev
TRACER_API_KEY=dev-secret-key-change-in-prod
```

---

## Step 3: Create API Client

**File:** `web/src/lib/api.ts`

```typescript
const API_BASE = process.env.NEXT_PUBLIC_API_BASE;
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
  if (!API_BASE) {
    throw new Error('NEXT_PUBLIC_API_BASE not configured');
  }

  const url = `${API_BASE}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
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

export function getPortfolio() {
  return fetchAPI<ApiResponse>('/api/status');
}

export function refreshPortfolio() {
  return fetchAPI<ApiResponse>('/api/refresh', { method: 'POST' });
}
```

---

## Step 4: Create Format Helpers

**File:** `web/src/lib/format.ts`

```typescript
export const fmt = (n: number | null | undefined): string => {
  if (n == null) return '—';
  return Number(n).toLocaleString('en-US', { maximumFractionDigits: 0 });
};

export const fmtPct = (n: number | null | undefined): string => {
  if (n == null) return '—';
  return (n >= 0 ? '+' : '') + Number(n).toFixed(1) + '%';
};

export const pnlClass = (n: number | null | undefined): string => {
  if (n == null) return 'text-gray-500';
  return n > 0 ? 'text-green-600' : n < 0 ? 'text-red-600' : 'text-gray-500';
};

export const signalColor = (signal: string): string => {
  const colors: Record<string, string> = {
    BUY: '#4CAF50',
    HOLD: '#2196F3',
    SELL: '#F44336',
    REVIEW: '#FF9800',
  };
  return colors[signal] || '#FF9800';
};
```

---

## Step 5: Create Global Layout

**File:** `web/src/app/layout.tsx`

```typescript
import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'PSA × Collectr Tracer',
  description: 'Portfolio Intelligence for PSA-Graded Pokemon Cards',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900">
        <header className="bg-blue-900 text-white sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <h1 className="text-xl font-bold">🃏 PSA × Collectr Tracer</h1>
          </div>
        </header>
        <main className="max-w-7xl mx-auto px-4 py-8">
          {children}
        </main>
      </body>
    </html>
  );
}
```

---

## Step 6: Create Dashboard Page

**File:** `web/src/app/page.tsx`

```typescript
'use client';

import { useEffect, useState } from 'react';
import { getPortfolio, ApiResponse } from '@/lib/api';
import { fmt, fmtPct, pnlClass, signalColor } from '@/lib/format';
import Link from 'next/link';

export default function Dashboard() {
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        const result = await getPortfolio();
        setData(result);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load portfolio');
        setData(null);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-gray-600">Loading portfolio…</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <h3 className="text-red-900 font-bold">Connection failed</h3>
        <p className="text-red-700 mt-2">{error}</p>
        <button
          onClick={() => window.location.reload()}
          className="mt-4 bg-red-600 text-white px-4 py-2 rounded"
        >
          🔄 Retry
        </button>
      </div>
    );
  }

  if (!data) {
    return <div className="text-center py-12 text-gray-500">No data loaded</div>;
  }

  const { portfolio, summary, ts_display } = data;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold">Dashboard</h2>
        <div className="text-sm text-gray-600">
          Last update: <span className="font-mono">{ts_display}</span>
        </div>
      </div>

      {/* KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <div className="text-sm text-gray-600">Cards</div>
          <div className="text-2xl font-bold mt-2">{summary.card_count}</div>
          <div className="text-xs text-gray-500 mt-1">PSA graded</div>
        </div>
        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <div className="text-sm text-gray-600">Total Cost</div>
          <div className="text-2xl font-bold mt-2">฿{fmt(summary.total_cost)}</div>
        </div>
        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <div className="text-sm text-gray-600">Market Value</div>
          <div className="text-2xl font-bold mt-2">฿{fmt(summary.total_market_value)}</div>
        </div>
        <div className="bg-white p-6 rounded-lg border border-gray-200">
          <div className="text-sm text-gray-600">Total P&L</div>
          <div className={`text-2xl font-bold mt-2 ${pnlClass(summary.total_pnl)}`}>
            ฿{fmt(summary.total_pnl)}
          </div>
          <div className="text-xs text-gray-500 mt-1">{fmtPct(summary.pnl_pct)}</div>
        </div>
      </div>

      {/* Portfolio Table */}
      <div className="bg-white rounded-lg border border-gray-200 overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-100 border-b border-gray-200">
            <tr>
              <th className="px-4 py-3 text-left font-semibold">Card</th>
              <th className="px-4 py-3 text-right font-semibold">Cost (฿)</th>
              <th className="px-4 py-3 text-right font-semibold">Market (฿)</th>
              <th className="px-4 py-3 text-right font-semibold">P&L (฿)</th>
              <th className="px-4 py-3 text-right font-semibold">P&L %</th>
              <th className="px-4 py-3 text-center font-semibold">Signal</th>
            </tr>
          </thead>
          <tbody>
            {portfolio.map((card, idx) => (
              <tr key={idx} className="border-b border-gray-200 hover:bg-blue-50">
                <td className="px-4 py-3">
                  <div className="font-medium">{card.subject}</div>
                  <div className="text-xs text-gray-600">PSA {card.grade} #{card.card_number}</div>
                </td>
                <td className="px-4 py-3 text-right">฿{fmt(card.my_cost)}</td>
                <td className="px-4 py-3 text-right">฿{fmt(card.market_value)}</td>
                <td className={`px-4 py-3 text-right ${pnlClass(card.pnl)}`}>
                  ฿{fmt(card.pnl)}
                </td>
                <td className={`px-4 py-3 text-right font-medium ${pnlClass(card.pnl_pct)}`}>
                  {fmtPct(card.pnl_pct)}
                </td>
                <td className="px-4 py-3 text-center">
                  <span
                    className="inline-block px-3 py-1 rounded text-white text-xs font-bold"
                    style={{ backgroundColor: signalColor(card.signal) }}
                  >
                    {card.signal}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Navigation Links */}
      <div className="flex gap-4 justify-center">
        <Link
          href="/portfolio"
          className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          📋 Portfolio
        </Link>
        <Link
          href="/add-card"
          className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          ➕ Add Card
        </Link>
        <Link
          href="/pnl"
          className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          💹 P&L
        </Link>
      </div>
    </div>
  );
}
```

---

## Step 7: Create Placeholder Pages

**File:** `web/src/app/portfolio/page.tsx`

```typescript
'use client';

import Link from 'next/link';

export default function Portfolio() {
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">📋 Portfolio</h2>
      <p className="text-gray-600">Portfolio page coming soon…</p>
      <Link href="/" className="text-blue-600 hover:underline">
        ← Back to Dashboard
      </Link>
    </div>
  );
}
```

**File:** `web/src/app/add-card/page.tsx`

```typescript
'use client';

import Link from 'next/link';

export default function AddCard() {
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">➕ Add Card</h2>
      <p className="text-gray-600">Add card page coming soon…</p>
      <Link href="/" className="text-blue-600 hover:underline">
        ← Back to Dashboard
      </Link>
    </div>
  );
}
```

**File:** `web/src/app/pnl/page.tsx`

```typescript
'use client';

import Link from 'next/link';

export default function PnL() {
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">💹 P&L Performance</h2>
      <p className="text-gray-600">P&L page coming soon…</p>
      <Link href="/" className="text-blue-600 hover:underline">
        ← Back to Dashboard
      </Link>
    </div>
  );
}
```

---

## Step 8: Update Global CSS

**File:** `web/src/app/globals.css`

Replace the default content with:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

html {
  color-scheme: light;
}

body {
  background: #f9fafb;
  color: #111827;
}

/* Sticky table headers */
thead {
  position: sticky;
  top: 0;
  z-index: 10;
}

/* Loading skeleton animation */
@keyframes loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}
```

---

## Step 9: Test Locally

```bash
npm run dev
```

Visit: `http://localhost:3000`

You should see the Dashboard with your portfolio data loaded from the Flask backend! ✅

---

## Step 10: Deploy to Vercel

1. **Push to GitHub** (if using GitHub)
2. **Go to:** https://vercel.com/import
3. **Select your repo**
4. **Add Environment Variables:**
   - `NEXT_PUBLIC_API_BASE` = `https://automated-crummiest-puritan.ngrok-free.dev`
   - `TRACER_API_KEY` = `dev-secret-key-change-in-prod`
5. **Click Deploy**

Your app will be live at: `https://psa-collectr-tracer.vercel.app` (or similar)

---

## 🎯 What's Next

After testing locally:
- Run `npm run build` to check for errors
- Deploy to Vercel
- Run Lighthouse audit on all pages
- Monitor the 7-day grace period

✅ **Phase C.3 ready to execute!**

