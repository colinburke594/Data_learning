import { useState } from "react";
import { CLEAN_DATASETS, DOMAIN_FILTERS } from "../data/cleanDatasetData";

function useCleanDatasetCompletion() {
  const [completed, setCompleted] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem("clean_dataset_completed") || "{}");
    } catch {
      return {};
    }
  });

  const toggle = (id) => {
    setCompleted((prev) => {
      const next = { ...prev, [id]: !prev[id] };
      localStorage.setItem("clean_dataset_completed", JSON.stringify(next));
      return next;
    });
  };

  return { completed, toggle };
}

export default function CleanDatasetLibrary() {
  const { completed, toggle } = useCleanDatasetCompletion();
  const [activeDomain, setActiveDomain] = useState("all");
  const [expandedId, setExpandedId] = useState(null);

  const filtered = CLEAN_DATASETS.filter(
    (d) => activeDomain === "all" || d.domain === activeDomain
  );

  const totalCount = CLEAN_DATASETS.length;
  const completedCount = Object.values(completed).filter(Boolean).length;

  return (
    <div className="max-w-4xl mx-auto">
      {/* Intro banner */}
      <div className="bg-emerald-950/30 border border-emerald-800/40 rounded-xl p-4 mb-6">
        <div className="flex items-start gap-3">
          <span className="text-2xl">✨</span>
          <div>
            <h3 className="text-sm font-bold text-emerald-400 mb-1">Clean Synthetic Datasets</h3>
            <p className="text-xs text-gray-400 leading-relaxed">
              These are pre-cleaned, synthetic datasets ready for analysis, modeling, and visualization practice.
              Each dataset mirrors its dirty counterpart but with consistent formatting, proper types, and no quality issues.
              Download any dataset and start building immediately.
            </p>
          </div>
        </div>
      </div>

      {/* Stats header */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
        {[
          { label: "Total Datasets", value: totalCount },
          { label: "Explored", value: completedCount },
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
          <span className="text-sm font-semibold text-gray-300">Dataset Exploration</span>
          <span className="text-sm font-bold text-white">{completedCount}/{totalCount}</span>
        </div>
        <div className="h-2 rounded-full bg-gray-800">
          <div
            className="h-full rounded-full bg-blue-500 transition-all duration-500"
            style={{ width: `${totalCount === 0 ? 0 : (completedCount / totalCount) * 100}%` }}
          />
        </div>
      </div>

      {/* Domain filter tabs */}
      <div className="flex gap-1.5 flex-wrap mb-5">
        {DOMAIN_FILTERS.map((f) => {
          const count = f.id === "all"
            ? CLEAN_DATASETS.length
            : CLEAN_DATASETS.filter((d) => d.domain === f.id).length;
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

          return (
            <div
              key={dataset.id}
              className={`rounded-xl border transition-all duration-200 overflow-hidden ${
                isDone
                  ? "bg-blue-950/20 border-blue-900/50"
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
                    <span className={`font-semibold text-sm ${isDone ? "text-blue-400 line-through decoration-blue-700" : "text-white"}`}>
                      {dataset.name}
                    </span>
                    <span
                      className="text-xs px-2 py-0.5 rounded font-medium"
                      style={{ backgroundColor: `${dataset.domainColor}22`, color: dataset.domainColor }}
                    >
                      {dataset.domainLabel}
                    </span>
                    <span className="text-xs px-2 py-0.5 rounded font-medium bg-emerald-950/50 text-emerald-400 border border-emerald-900/50">
                      Clean
                    </span>
                    {isDone && (
                      <span className="text-xs font-bold text-blue-400 bg-blue-900/40 px-2 py-0.5 rounded">
                        ✓ Explored
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-gray-400 mb-2">{dataset.description}</p>
                  <div className="flex gap-2 flex-wrap">
                    {[
                      { label: dataset.format, icon: "📁" },
                      { label: `${dataset.rows} rows`, icon: "📊" },
                      { label: `${dataset.cols} cols`, icon: "🔢" },
                    ].map((tag) => (
                      <span key={tag.label} className="text-xs text-gray-500 bg-gray-800 px-2 py-0.5 rounded font-mono">
                        {tag.icon} {tag.label}
                      </span>
                    ))}
                    <span className="text-xs text-emerald-400 bg-emerald-950/50 border border-emerald-900/50 px-2 py-0.5 rounded font-mono">
                      ✓ No quality issues
                    </span>
                  </div>
                </div>

                <span className="text-gray-600 text-sm shrink-0">{isExpanded ? "▲" : "▼"}</span>
              </div>

              {/* Expanded content */}
              {isExpanded && (
                <div className="border-t border-gray-800 px-4 pb-4 pt-4 space-y-4">
                  {/* Columns */}
                  <div>
                    <div className="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-3">
                      📋 Columns ({dataset.columns.length})
                    </div>
                    <div className="flex gap-1.5 flex-wrap">
                      {dataset.columns.map((col) => (
                        <span
                          key={col}
                          className="text-xs font-mono px-2 py-1 rounded bg-gray-800 text-gray-300 border border-gray-700"
                        >
                          {col}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Use cases */}
                  <div>
                    <div className="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-3">
                      🎯 Practice Use Cases
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {dataset.useCases.map((uc, i) => (
                        <div
                          key={i}
                          className="flex items-center gap-2 bg-gray-900/60 border border-gray-800 rounded-lg p-3"
                        >
                          <div
                            className="w-2 h-2 rounded-full shrink-0"
                            style={{ backgroundColor: dataset.domainColor }}
                          />
                          <span className="text-xs text-gray-300">{uc}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Actions row */}
                  <div className="flex items-center justify-between pt-1 gap-3 flex-wrap">
                    <a
                      href={`/datasets/clean/${dataset.file}`}
                      download={dataset.file}
                      onClick={(e) => e.stopPropagation()}
                      className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-semibold transition-all border bg-blue-950/30 border-blue-800 text-blue-400 hover:border-blue-600 hover:bg-blue-950/50"
                    >
                      ⬇ Download Clean Dataset
                    </a>
                    <button
                      onClick={(e) => { e.stopPropagation(); toggle(dataset.id); }}
                      className={`px-4 py-2 rounded-lg text-sm font-semibold transition-all border ${
                        isDone
                          ? "bg-blue-950/50 border-blue-700 text-blue-400 hover:bg-blue-900/40"
                          : "bg-gray-800 border-gray-700 text-gray-300 hover:border-gray-600"
                      }`}
                    >
                      {isDone ? "✓ Marked as Explored" : "Mark as Explored"}
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
          <div className="text-4xl mb-3">✨</div>
          <div>No datasets match this filter</div>
        </div>
      )}
    </div>
  );
}

export function getCleanDatasetProgress() {
  try {
    const completed = JSON.parse(localStorage.getItem("clean_dataset_completed") || "{}");
    return {
      done: Object.values(completed).filter(Boolean).length,
      total: CLEAN_DATASETS.length,
    };
  } catch {
    return { done: 0, total: CLEAN_DATASETS.length };
  }
}
