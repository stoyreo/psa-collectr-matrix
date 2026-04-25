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
          <p>Phase C: Vercel Hybrid Migration | ngrok tunnel active</p>
        </footer>
      </body>
    </html>
  );
}
