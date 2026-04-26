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

  const { portfolio, summary, ts_display, data_source } = data;

  return (
    <div className="space-y-8">
      {data_source === 'snapshot' && (
        <div className="bg-blue-50 border border-blue-300 rounded-lg p-4">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 5v8a2 2 0 01-2 2h-5l-5 4v-4H4a2 2 0 01-2-2V5a2 2 0 012-2h12a2 2 0 012 2z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-blue-800">Static snapshot from {ts_display}</h3>
              <p className="text-sm text-blue-700 mt-1">Data is read-only. To update, run <code className="bg-blue-100 px-2 py-1 rounded text-xs font-mono">REFRESH_AND_PUSH.bat</code> locally.</p>
            </div>
          </div>
        </div>
      )}

      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold">Dashboard</h2>
        <div className="text-sm text-gray-600">
          Last update: <span className="font-mono">{ts_display}</span>
        </div>
      </div>

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
