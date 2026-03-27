"use client";

import { useEffect, useState } from "react";
import { getEpisodes, getHealth, type Episode } from "@/lib/api";

export default function Dashboard() {
  const [episodes, setEpisodes] = useState<Episode[]>([]);
  const [health, setHealth] = useState<string>("checking...");

  useEffect(() => {
    getHealth()
      .then(() => setHealth("connected"))
      .catch(() => setHealth("offline"));
    getEpisodes()
      .then(setEpisodes)
      .catch(() => {});
  }, []);

  const statusColor: Record<string, string> = {
    pending: "bg-gray-600",
    compressing: "bg-yellow-600",
    detecting: "bg-blue-600",
    indexing: "bg-purple-600",
    ready: "bg-green-600",
    error: "bg-red-600",
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-simpsons-yellow">Dashboard</h1>
        <p className="text-gray-400 mt-1">
          API: <span className={health === "connected" ? "text-green-400" : "text-red-400"}>{health}</span>
        </p>
      </div>

      {/* Episode Pipeline */}
      <section>
        <h2 className="text-xl font-semibold mb-4">Processing Pipeline</h2>
        <div className="grid gap-4">
          {episodes.length === 0 ? (
            <div className="bg-gray-900 rounded-lg border border-gray-800 p-6 text-center text-gray-500">
              No episodes loaded yet. Start by running the compression script on your M5 Mac.
            </div>
          ) : (
            episodes.map((ep) => (
              <div
                key={ep.id}
                className="bg-gray-900 rounded-lg border border-gray-800 p-4 flex items-center justify-between"
              >
                <div>
                  <h3 className="font-medium">
                    S{String(ep.season).padStart(2, "0")}E
                    {String(ep.episode_number).padStart(2, "0")} &mdash;{" "}
                    {ep.title}
                  </h3>
                  <p className="text-sm text-gray-400">
                    {ep.duration_seconds
                      ? `${Math.round(ep.duration_seconds / 60)} min`
                      : "Duration unknown"}
                    {ep.gemini_cost_usd > 0 &&
                      ` | Cost: $${ep.gemini_cost_usd.toFixed(2)}`}
                  </p>
                </div>
                <span
                  className={`px-3 py-1 rounded-full text-xs font-medium ${statusColor[ep.status] || "bg-gray-600"}`}
                >
                  {ep.status}
                </span>
              </div>
            ))
          )}
        </div>
      </section>

      {/* Quick Stats Placeholder */}
      <section>
        <h2 className="text-xl font-semibold mb-4">Quick Stats</h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {[
            { label: "Total Scenes", value: "--" },
            { label: "Avg Confidence", value: "--" },
            { label: "Searches Today", value: "--" },
          ].map((stat) => (
            <div
              key={stat.label}
              className="bg-gray-900 rounded-lg border border-gray-800 p-4 text-center"
            >
              <p className="text-2xl font-bold text-simpsons-yellow">
                {stat.value}
              </p>
              <p className="text-sm text-gray-400">{stat.label}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
