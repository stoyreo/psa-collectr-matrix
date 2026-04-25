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
