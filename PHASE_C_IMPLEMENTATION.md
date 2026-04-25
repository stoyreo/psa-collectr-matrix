# Phase C — Vercel Hybrid Migration: Implementation Guide

**Status:** Ready for execution  
**Date:** 2026-04-25  
**Target:** Scaffold Next.js 14 on Vercel with Flask backend via ngrok

---

## Quick Start (5 min)

```bash
# 1. Change to project root
cd "PSA x Collectr Tracer"

# 2. Create Next.js 14 app with TypeScript + Tailwind
npx create-next-app@latest web --ts --tailwind --eslint --app --src-dir --import-alias "@/*"

# 3. Install additional dependencies
cd web
npm install -D shadcn-ui lucide-react recharts @tanstack/react-query @tanstack/react-table zod

# 4. Create environment files
echo "NEXT_PUBLIC_API_BASE=https://abc-123-def.ngrok-free.app
TRACER_API_KEY=your-secret-token-here" > .env.local

# 5. Create Vercel env vars (set in Vercel dashboard)
# NEXT_PUBLIC_API_BASE
# TRACER_API_KEY
```

---

## File Structure

```
PSA x Collectr Tracer/
├── web/                          # ← New Next.js 14 app
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx         # Global layout (nav, theme)
│   │   │   ├── page.tsx           # Dashboard (/)
│   │   │   ├── portfolio/
│   │   │   │   └── page.tsx       # Portfolio (/portfolio)
│   │   │   ├── add-card/
│   │   │   │   └── page.tsx       # Add Card (/add-card)
│   │   │   └── pnl/
│   │   │       └── page.tsx       # P&L Performance (/pnl)
│   │   ├── components/
│   │   │   ├── navbar.tsx         # Top nav with tabs
│   │   │   ├── portfolio-table.tsx # Sortable portfolio table
│   │   │   ├── kpi-grid.tsx       # KPI cards
│   │   │   ├── charts.tsx         # Chart wrappers (Recharts)
│   │   │   ├── error-boundary.tsx # Error fallback
│   │   │   └── loading.tsx        # Loading skeleton
│   │   ├── hooks/
│   │   │   ├── usePortfolio.ts    # React Query hook for /api/status
│   │   │   ├── useRefresh.ts      # React Query hook for /api/refresh
│   │   │   └── useAPI.ts          # Bearer token + error handling
│   │   ├── lib/
│   │   │   ├── api.ts             # Fetch wrapper with auth header
│   │   │   ├── format.ts          # fmt, fmtPct, pnlClass helpers
│   │   │   └── types.ts           # TypeScript interfaces
│   │   └── styles/
│   │       └── globals.css        # Tailwind + CSS variables
│   ├── .env.local                 # ← Dev environment (ngrok URL)
│   ├── next.config.js             # Next.js config (if needed)
│   ├── tailwind.config.js          # Tailwind setup
│   ├── tsconfig.json              # TypeScript config
│   └── package.json               # Dependencies
│
├── webapp.py                       # ← Flask backend (unchanged)
├── start_webapp.bat                # ← Start Flask on port 5000
├── start_tunnel.bat                # ← New: Start ngrok
└── .env                            # ← Backend env (TRACER_API_KEY, etc.)
```

---

## Phase C.0: Prerequisites ✓

- [x] Flask app running (`start_webapp.bat`)
- [x] ngrok downloaded from https://ngrok.com/download
- [x] Vercel account created + GitHub linked
- [x] MIGRATION_REPORT.md reviewed

---

## Phase C.1: Backend Updates (Flask)

**File:** `webapp.py`

Add CORS and auth token validation:

```python
from flask_cors import CORS
import os

CORS(app, resources={r"/api/*": {"origins": "https://psa-collectr-tracer.vercel.app"}})

@app.before_request
def check_api_auth():
    if request.path.startswith('/api/') and request.method != 'GET':
        token = request.headers.get('X-Tracer-Key', '')
        if token != os.environ.get('TRACER_API_KEY', ''):
            return jsonify({"error": "Unauthorized"}), 401
```

**File:** `.env` (project root, not web/)

```
FLASK_ENV=production
TRACER_API_KEY=dev-secret-key-change-in-prod
ANTHROPIC_API_KEY=sk-proj-xxxx  # optional
NGROK_URL=https://abc-123-def.ngrok-free.app  # Update after each ngrok start
```

---

## Phase C.2: Tunnel Setup (ngrok)

**File:** `start_tunnel.bat` (project root)

```batch
@echo off
REM Start ngrok tunnel for Flask backend
REM Note: ngrok free tier resets URL daily (pro: $5/month for static URLs)

ngrok http 5000 --log=stdout --log-level=info

REM After ngrok starts, copy the URL (e.g., https://abc-123-def.ngrok-free.app)
REM and paste into:
REM 1. web/.env.local (NEXT_PUBLIC_API_BASE)
REM 2. Vercel project settings → Environment Variables
```

**First Run Checklist:**
```
1. Open PowerShell in project root
2. Run: .\start_tunnel.bat
3. Wait for: "Session started successfully at https://abc-123-def.ngrok-free.app"
4. Copy that URL
5. Paste into web/.env.local and Vercel
```

---

## Phase C.3: Next.js Frontend Scaffold

### 3.1 Create Next.js 14 App

```bash
# From project root
npx create-next-app@latest web --ts --tailwind --eslint --app --src-dir --import-alias "@/*"
cd web
npm install -D shadcn-ui lucide-react recharts @tanstack/react-query @tanstack/react-table zod

# Optional: Install shadcn components as needed
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add table
```

### 3.2 Create Environment Variables

**File:** `web/.env.local`

```
# After ngrok starts, paste the URL here:
NEXT_PUBLIC_API_BASE=https://abc-123-def.ngrok-free.app

# Backend auth token (same as Flask .env TRACER_API_KEY)
TRACER_API_KEY=dev-secret-key-change-in-prod
```

### 3.3 Create API Client (`src/lib/api.ts`)

```typescript
const API_BASE = process.env.NEXT_PUBLIC_API_BASE;
const API_KEY = process.env.TRACER_API_KEY;

export async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    'X-Tracer-Key': API_KEY,
    ...options.headers,
  };

  const response = await fetch(url, { ...options, headers });
  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }
  return response.json();
}

// Usage: const data = await fetchAPI('/api/status')
```

### 3.4 Create Hooks (`src/hooks/usePortfolio.ts`)

```typescript
import { useQuery } from '@tanstack/react-query';
import { fetchAPI } from '@/lib/api';

export function usePortfolio() {
  return useQuery({
    queryKey: ['portfolio'],
    queryFn: () => fetchAPI('/api/status'),
    staleTime: 5 * 60 * 1000, // 5 minutes
    refetchInterval: 10 * 60 * 1000, // 10 minutes
  });
}

export function useRefresh() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => fetchAPI('/api/refresh', { method: 'POST' }),
    onSuccess: (data) => {
      queryClient.setQueryData(['portfolio'], data);
    },
  });
}
```

### 3.5 Create Pages

**File:** `src/app/page.tsx` (Dashboard)

```typescript
import { Suspense } from 'react';
import DashboardContent from '@/components/dashboard';
import LoadingSkeleton from '@/components/loading';

export default function Dashboard() {
  return (
    <Suspense fallback={<LoadingSkeleton />}>
      <DashboardContent />
    </Suspense>
  );
}
```

Repeat for `/portfolio/page.tsx`, `/add-card/page.tsx`, `/pnl/page.tsx`

### 3.6 Create Global Layout (`src/app/layout.tsx`)

```typescript
import type { Metadata } from 'next';
import Navbar from '@/components/navbar';
import { QueryClientProvider } from '@tanstack/react-query';
import queryClient from '@/lib/queryClient';

export const metadata: Metadata = {
  title: 'PSA × Collectr Tracer',
  description: 'Portfolio Intelligence for PSA-Graded Pokemon Cards',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50">
        <QueryClientProvider client={queryClient}>
          <Navbar />
          <main className="max-w-7xl mx-auto px-4 py-8">
            {children}
          </main>
        </QueryClientProvider>
      </body>
    </html>
  );
}
```

---

## Phase C.4: Vercel Deployment

### 4.1 Link to Vercel

```bash
# From web/ directory
npm install -g vercel
vercel link
# Follow prompts to connect to your GitHub account
```

### 4.2 Set Environment Variables in Vercel

Dashboard → Settings → Environment Variables:
```
NEXT_PUBLIC_API_BASE = https://abc-123-def.ngrok-free.app
TRACER_API_KEY = [same as Flask .env]
```

### 4.3 Deploy

```bash
vercel --prod
```

Your app is now live at: `https://psa-collectr-tracer.vercel.app`

---

## Phase C.5: Lighthouse Gates

After deployment, verify quality metrics:

```bash
# Install Lighthouse CLI
npm install -g lighthouse

# Run audit on all tabs
lighthouse https://psa-collectr-tracer.vercel.app --chrome-flags="--headless --no-sandbox"
lighthouse https://psa-collectr-tracer.vercel.app/portfolio --chrome-flags="--headless --no-sandbox"
lighthouse https://psa-collectr-tracer.vercel.app/add-card --chrome-flags="--headless --no-sandbox"
lighthouse https://psa-collectr-tracer.vercel.app/pnl --chrome-flags="--headless --no-sandbox"
```

**Target Scores:**
- Performance: ≥ 90
- Accessibility: ≥ 95
- Best Practices: ≥ 95
- SEO: ≥ 90

**If scores miss targets:**
- Code-split large components (dynamic imports)
- Optimize images (next/image)
- Lazy-load tables
- Defer chart rendering

---

## Phase C.6: 7-Day Grace Period

Keep both Cloudflare and ngrok running:

```
Days 1-7:   Both tunnels active → users can opt-in to Vercel
Day 8:      Turn off ngrok (or cloudflared — choose one)
Day 30:     Final decommission of old tunnel
```

Rollback if needed: Click "Start Over" in old Flask UI at `localhost:5000`

---

## Checklist

### Pre-Flight
- [ ] Flask backend updated with CORS + auth
- [ ] .env file created with TRACER_API_KEY
- [ ] ngrok downloaded and tested
- [ ] Vercel account linked to GitHub

### Phase C.3 (Next.js Scaffold)
- [ ] `npx create-next-app@latest web ...` executed
- [ ] Dependencies installed (shadcn, lucide, recharts, react-query)
- [ ] .env.local created with ngrok URL
- [ ] API client (lib/api.ts) created
- [ ] Hooks (usePortfolio, useRefresh) created
- [ ] Pages created (dashboard, portfolio, add-card, pnl)
- [ ] Global layout created with QueryClientProvider
- [ ] Tailwind CSS configured

### Phase C.4 (Vercel Deploy)
- [ ] `vercel link` executed
- [ ] Environment variables set in Vercel dashboard
- [ ] `vercel --prod` deployed
- [ ] All 4 tabs load within 3s
- [ ] API auth working (X-Tracer-Key header required)

### Phase C.5 (Lighthouse)
- [ ] Performance ≥ 90 ✓
- [ ] Accessibility ≥ 95 ✓
- [ ] Best Practices ≥ 95 ✓
- [ ] SEO ≥ 90 ✓

### Phase C.6 (Grace Period)
- [ ] Cloudflare + ngrok both running
- [ ] Monitor for 7 days
- [ ] Turn off one tunnel on day 8
- [ ] Final decommission on day 30

---

## Next Steps

1. Execute Phase C.0-C.1: Backend setup + CORS/auth
2. Execute Phase C.2: ngrok tunnel
3. Execute Phase C.3: Next.js scaffold
4. Execute Phase C.4: Vercel deployment
5. Execute Phase C.5: Lighthouse validation
6. Move to Phase D: Tab repairs (portfolio table sticky header, grade column, P&L split)
7. Move to Phase E: Skill suite creation (12 skills for automation)

---

**End of Phase C Implementation Guide**
