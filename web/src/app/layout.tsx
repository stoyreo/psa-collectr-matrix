'use client';

import type { Metadata } from 'next';
import { useEffect, useState } from 'react';
import './globals.css';

// export const metadata: Metadata = {
//   title: 'PSA × Collectr Tracer',
//   description: 'Portfolio Intelligence for PSA-Graded Pokemon Cards',
// };

function StatusPill() {
  const [status, setStatus] = useState<'live' | 'snapshot' | 'unknown'>('unknown');

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await fetch('/api/health', { method: 'GET' });
        if (response.ok) {
          setStatus('live');
        } else {
          setStatus('snapshot');
        }
      } catch {
        setStatus('snapshot');
      }
    };

    checkStatus();
    const interval = setInterval(checkStatus, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const statusColor = status === 'live' ? 'bg-green-100 text-green-800' : status === 'snapshot' ? 'bg-amber-100 text-amber-800' : 'bg-gray-100 text-gray-800';
  const statusDot = status === 'live' ? '🟢' : status === 'snapshot' ? '🟡' : '⚪';

  return (
    <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${statusColor}`}>
      {statusDot} {status === 'live' ? 'Live' : status === 'snapshot' ? 'Snapshot' : 'Checking...'}
    </span>
  );
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900">
        <header className="bg-blue-900 text-white sticky top-0 z-50 shadow">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <h1 className="text-xl font-bold">🃏 PSA × Collectr Tracer</h1>
            <p className="text-xs text-blue-200 mt-1">Portfolio Intelligence Platform</p>
          </div>
        </header>
        <main className="max-w-7xl mx-auto px-4 py-8">
          {children}
        </main>
        <footer className="bg-gray-100 border-t border-gray-200 mt-12 py-4 text-center text-sm text-gray-600">
          <div className="flex items-center justify-center gap-4">
            <p>Phase C: Vercel Hybrid Migration</p>
            <StatusPill />
          </div>
        </footer>
      </body>
    </html>
  );
}
