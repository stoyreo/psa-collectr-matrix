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
