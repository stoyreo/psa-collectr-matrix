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
