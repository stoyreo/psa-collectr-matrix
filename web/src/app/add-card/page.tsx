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
