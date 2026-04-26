/**
 * Server-side proxy to the ngrok-tunneled Flask backend.
 *
 * Why this exists:
 *   The browser cannot call the ngrok endpoint directly because every
 *   request from a "browser" User-Agent triggers ngrok's free-tier abuse
 *   interstitial. Setting `ngrok-skip-browser-warning` on the actual
 *   request would help — except that this header is non-simple, so
 *   browsers fire a CORS preflight OPTIONS first which itself gets the
 *   interstitial (no CORS headers, no JSON, just an HTML warning page).
 *   The result: browser blocks the call.
 *
 * Fix: route every `/api/*` call through this Vercel route handler.
 *   - Browser → Vercel: same-origin, no CORS, no preflight.
 *   - Vercel → ngrok:   server-side fetch, sets the bypass header,
 *                       so ngrok forwards to Flask cleanly.
 */

import { NextRequest, NextResponse } from 'next/server';

const BACKEND =
  process.env.BACKEND_API_URL ||
  process.env.NEXT_PUBLIC_API_BASE ||
  'https://automated-crummiest-puritan.ngrok-free.dev';

export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';

async function proxy(req: NextRequest, ctx: { params: Promise<{ path: string[] }> }) {
  const { path } = await ctx.params;
  const search = req.nextUrl.search;
  const targetUrl = `${BACKEND}/api/${path.join('/')}${search}`;

  // Forward only the headers Flask actually inspects + the ngrok bypass.
  const headers: Record<string, string> = {
    'ngrok-skip-browser-warning': '1',
    'User-Agent': 'psa-collectr-vercel-proxy/1.0',
  };
  const ct = req.headers.get('content-type');
  if (ct) headers['Content-Type'] = ct;
  const tracerKey = req.headers.get('x-tracer-key') || process.env.TRACER_API_KEY;
  if (tracerKey) headers['X-Tracer-Key'] = tracerKey;

  const init: RequestInit = {
    method: req.method,
    headers,
    cache: 'no-store',
  };

  // Body for non-GET/HEAD methods.
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    init.body = await req.text();
  }

  let upstream: Response;
  try {
    upstream = await fetch(targetUrl, init);
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Upstream fetch failed';
    return NextResponse.json(
      { error: 'Backend unreachable', detail: message, target: targetUrl },
      { status: 502 }
    );
  }

  // Stream upstream response back unmodified, preserving status + content type.
  const body = await upstream.arrayBuffer();
  const responseHeaders = new Headers();
  const upstreamCt = upstream.headers.get('content-type');
  if (upstreamCt) responseHeaders.set('content-type', upstreamCt);
  responseHeaders.set('cache-control', 'no-store');
  return new NextResponse(body, {
    status: upstream.status,
    headers: responseHeaders,
  });
}

export const GET = proxy;
export const POST = proxy;
export const PUT = proxy;
export const DELETE = proxy;
export const PATCH = proxy;
export const OPTIONS = proxy;
