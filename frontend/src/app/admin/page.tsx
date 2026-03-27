"use client";

export default function AdminPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-simpsons-yellow">Admin</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <h3 className="font-semibold mb-2">Re-index Episode</h3>
          <p className="text-sm text-gray-400 mb-4">
            Re-run Gemini analysis on the current episode.
          </p>
          <button
            disabled
            className="bg-gray-800 text-gray-400 px-4 py-2 rounded text-sm cursor-not-allowed"
          >
            Re-index (Phase 2)
          </button>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <h3 className="font-semibold mb-2">Export Metadata</h3>
          <p className="text-sm text-gray-400 mb-4">
            Download scene metadata as JSON.
          </p>
          <button
            disabled
            className="bg-gray-800 text-gray-400 px-4 py-2 rounded text-sm cursor-not-allowed"
          >
            Export JSON (Phase 3)
          </button>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <h3 className="font-semibold mb-2">Token Usage</h3>
          <p className="text-sm text-gray-400">
            Gemini: <span className="text-gray-300">$0.00</span>
          </p>
          <p className="text-sm text-gray-400">
            Veo: <span className="text-gray-300">$0.00</span>
          </p>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-lg p-6">
          <h3 className="font-semibold mb-2">Search Analytics</h3>
          <p className="text-sm text-gray-400">
            Total searches: <span className="text-gray-300">0</span>
          </p>
          <p className="text-sm text-gray-400">
            Avg latency: <span className="text-gray-300">-- ms</span>
          </p>
        </div>
      </div>
    </div>
  );
}
