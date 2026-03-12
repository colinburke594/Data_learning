import { useState, useEffect } from "react";
import { DATASETS, DOMAIN_FILTERS } from "../data/datasetData";

const SEVERITY_STYLES = {
  high:   { dot: "bg-red-500",    badge: "bg-red-950 text-red-400 border-red-900" },
  medium: { dot: "bg-amber-500",  badge: "bg-amber-950 text-amber-400 border-amber-900" },
  low:    { dot: "bg-blue-500",   badge: "bg-blue-950 text-blue-400 border-blue-900" },
};

function useDatasetCompletion() {
  const [completed, setCompleted] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem("dataset_completed") || "{}");
    } catch {
      return {};
    }
  });

  const toggle = (id) => {
    setCompleted((prev) => {
      const next = { ...prev, [id]: !prev[id] };
      localStorage.setItem("dataset_completed", JSON.stringify(next));
      return next;
    });
  };

  return { completed, toggle };
}

export default function DatasetLibrary() {
  const { completed, toggle } = useDatasetCompletion();
  const [activeDomain, setActiveDomain] = useState("all");
  const [expandedId, setExpandedId] = useState(null);

  const filtered = DATASETS.filter(
    (d) => activeDomain === "all" || d.domain === activeDomain
  );

  const totalCount = DATASETS.length;
  const completedCount = Object.values(completed).filter(Boolean).length;

  return (
    <div className="max-w-4xl mx-auto">
      {/* Stats header */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
        {[
          { label: "Total Datasets", value: totalCount },
          { label: "Completed", value: completedCount },
          { label: "Remaining", value: totalCount - completedCount },
          { label: "Progress", value: `${totalCount === 0 ? 0 : Math.round((completedCount / totalCount) * 100)}%` },
        ].map((s) => (
          <div key={s.label} className="bg-gray-900 border border-gray-800 rounded-xl p-3 text-center">
            <div className="text-xl font-bold text-white">{s.value}</div>
            <div className="text-xs text-gray-500 mt-0.5">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Overall progress bar */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 mb-6">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-semibold text-gray-300">Dataset Completion</span>
          <span className="text-sm font-bold text-white">{completedCount}/{totalCount}</span>
        </div>
        <div className="h-2 rounded-full bg-gray-800">
          <div
            className="h-full rounded-full bg-emerald-500 transition-all duration-500"
            style={{ width: `${totalCount === 0 ? 0 : (completedCount / totalCount) * 100}%` }}
          />
        </div>
      </div>

      {/* Domain filter tabs */}
      <div className="flex gap-1.5 flex-wrap mb-5">
        {DOMAIN_FILTERS.map((f) => {
          const count = f.id === "all"
            ? DATASETS.length
            : DATASETS.filter((d) => d.domain === f.id).length;
          const active = activeDomain === f.id;
          return (
            <button
              key={f.id}
              onClick={() => setActiveDomain(f.id)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                active
                  ? "text-white border"
                  : "bg-gray-900 text-gray-400 border border-gray-800 hover:border-gray-700"
              }`}
              style={active ? { backgroundColor: `${f.color}22`, borderColor: `${f.color}66`, color: f.color } : {}}
            >
              {f.icon} {f.label}
              <span className="ml-1 opacity-60 font-mono">{count}</span>
            </button>
          );
        })}
      </div>

      {/* Dataset list */}
      <div className="space-y-3">
        {filtered.map((dataset) => {
          const isDone = !!completed[dataset.id];
          const isExpanded = expandedId === dataset.id;
          const highCount = dataset.issues.filter((i) => i.severity === "high").length;

          return (
            <div
              key={dataset.id}
              className={`rounded-xl border transition-all duration-200 overflow-hidden ${
                isDone
                  ? "bg-emerald-950/20 border-emerald-900/50"
                  : "bg-gray-900/60 border-gray-800 hover:border-gray-700"
              }`}
            >
              {/* Card header */}
              <div
                className="flex items-center gap-4 p-4 cursor-pointer"
                onClick={() => setExpandedId(isExpanded ? null : dataset.id)}
              >
                <span className="text-3xl shrink-0">{dataset.emoji}</span>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap mb-1">
                    <span className={`font-semibold text-sm ${isDone ? "text-emerald-400 line-through decoration-emerald-700" : "text-white"}`}>
                      {dataset.name}
                    </span>
                    <span
                      className="text-xs px-2 py-0.5 rounded font-medium"
                      style={{ backgroundColor: `${dataset.domainColor}22`, color: dataset.domainColor }}
                    >
                      {dataset.domainLabel}
                    </span>
                    {isDone && (
                      <span className="text-xs font-bold text-emerald-400 bg-emerald-900/40 px-2 py-0.5 rounded">
                        ✓ Practiced
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-gray-400 mb-2">{dataset.description}</p>
                  <div className="flex gap-2 flex-wrap">
                    {[
                      { label: dataset.format, icon: "📁" },
                      { label: `${dataset.rows} rows`, icon: "📊" },
                      { label: `${dataset.cols} cols`, icon: "🔢" },
                      { label: `${dataset.nullRate} null`, icon: "⚠️" },
                    ].map((tag) => (
                      <span key={tag.label} className="text-xs text-gray-500 bg-gray-800 px-2 py-0.5 rounded font-mono">
                        {tag.icon} {tag.label}
                      </span>
                    ))}
                    {highCount > 0 && (
                      <span className="text-xs text-red-400 bg-red-950/50 border border-red-900/50 px-2 py-0.5 rounded font-mono">
                        🔴 {highCount} high-severity
                      </span>
                    )}
                  </div>
                </div>

                <span className="text-gray-600 text-sm shrink-0">{isExpanded ? "▲" : "▼"}</span>
              </div>

              {/* Expanded content */}
              {isExpanded && (
                <div className="border-t border-gray-800 px-4 pb-4 pt-4 space-y-4">
                  {/* Practice goal */}
                  <div
                    className="rounded-lg p-3 border text-sm"
                    style={{
                      backgroundColor: `${dataset.domainColor}11`,
                      borderColor: `${dataset.domainColor}33`,
                    }}
                  >
                    <span className="font-bold" style={{ color: dataset.domainColor }}>
                      🎯 Practice Goal:{" "}
                    </span>
                    <span className="text-gray-300">{dataset.target}</span>
                  </div>

                  {/* Issues */}
                  <div>
                    <div className="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-3">
                      🔍 Data Quality Issues ({dataset.issues.length})
                    </div>
                    <div className="space-y-2">
                      {dataset.issues.map((issue, i) => {
                        const sev = SEVERITY_STYLES[issue.severity] || SEVERITY_STYLES.low;
                        return (
                          <div
                            key={i}
                            className="flex items-start gap-3 bg-gray-900/60 border border-gray-800 rounded-lg p-3"
                          >
                            <div className={`w-2 h-2 rounded-full mt-1.5 shrink-0 ${sev.dot}`} />
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 flex-wrap mb-1">
                                <span className="text-sm font-semibold text-gray-200">{issue.type}</span>
                                <span className={`text-xs px-1.5 py-0.5 rounded border font-mono ${sev.badge}`}>
                                  {issue.severity}
                                </span>
                              </div>
                              <p className="text-xs text-gray-400 leading-relaxed">{issue.detail}</p>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>

                  {/* Actions row */}
                  <div className="flex items-center justify-between pt-1 gap-3 flex-wrap">
                    <a
                      href={`/datasets/dirty/${dataset.file}`}
                      download={dataset.file}
                      onClick={(e) => e.stopPropagation()}
                      className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-semibold transition-all border bg-gray-800 border-gray-700 text-gray-300 hover:border-emerald-700 hover:text-emerald-400 hover:bg-emerald-950/30"
                    >
                      ⬇ Download Dataset
                    </a>
                    <button
                      onClick={(e) => { e.stopPropagation(); toggle(dataset.id); }}
                      className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all border ${
                        isDone
                          ? "bg-emerald-950/50 border-emerald-700 text-emerald-400 hover:bg-emerald-900/40"
                          : "bg-gray-800 border-gray-700 text-gray-300 hover:border-gray-600"
                      }`}
                    >
                      {isDone ? "✓ Marked as Practiced" : "Mark as Practiced"}
                    </button>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {filtered.length === 0 && (
        <div className="text-center py-16 text-gray-500">
          <div className="text-4xl mb-3">🗂️</div>
          <div>No datasets match this filter</div>
        </div>
      )}
    </div>
  );
}

export function getDatasetProgress() {
  try {
    const completed = JSON.parse(localStorage.getItem("dataset_completed") || "{}");
    return {
      done: Object.values(completed).filter(Boolean).length,
      total: DATASETS.length,
    };
  } catch {
    return { done: 0, total: DATASETS.length };
  }
}
