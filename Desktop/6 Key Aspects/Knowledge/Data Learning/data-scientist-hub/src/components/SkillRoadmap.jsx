import { useState, useEffect } from "react";
import { DOMAINS } from "../data/roadmapData";

const LEVEL_COLORS = [
  { bg: "bg-blue-950/60", border: "border-blue-800/40", badge: "bg-blue-900/60 text-blue-300", ring: "ring-blue-500" },
  { bg: "bg-emerald-950/60", border: "border-emerald-800/40", badge: "bg-emerald-900/60 text-emerald-300", ring: "ring-emerald-500" },
  { bg: "bg-purple-950/60", border: "border-purple-800/40", badge: "bg-purple-900/60 text-purple-300", ring: "ring-purple-500" },
  { bg: "bg-orange-950/60", border: "border-orange-800/40", badge: "bg-orange-900/60 text-orange-300", ring: "ring-orange-500" },
];

function useRoadmapProgress() {
  const [checked, setChecked] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem("roadmap_checked") || "{}");
    } catch {
      return {};
    }
  });

  const toggle = (key) => {
    setChecked((prev) => {
      const next = { ...prev, [key]: !prev[key] };
      localStorage.setItem("roadmap_checked", JSON.stringify(next));
      return next;
    });
  };

  return { checked, toggle };
}

function DomainProgressBar({ domain, checked }) {
  const totalReady = domain.levels.reduce((sum, l) => sum + l.ready.length, 0);
  const doneReady = domain.levels.reduce(
    (sum, l) =>
      sum + l.ready.filter((_, i) => checked[`${domain.id}_L${l.level}_r${i}`]).length,
    0
  );
  const pct = totalReady === 0 ? 0 : Math.round((doneReady / totalReady) * 100);

  return (
    <div className="flex items-center gap-3 min-w-0">
      <div className="flex-1 h-1.5 rounded-full bg-gray-800">
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{ width: `${pct}%`, backgroundColor: domain.color }}
        />
      </div>
      <span className="text-xs font-mono text-gray-400 w-8 text-right">{pct}%</span>
    </div>
  );
}

function LevelCard({ domain, levelData, checked, toggle, levelIndex }) {
  const colors = LEVEL_COLORS[levelIndex] || LEVEL_COLORS[0];
  const readyDone = levelData.ready.filter((_, i) => checked[`${domain.id}_L${levelData.level}_r${i}`]).length;
  const readyTotal = levelData.ready.length;
  const isComplete = readyDone === readyTotal;
  const [expanded, setExpanded] = useState(levelIndex === 0);

  const completionPct = readyTotal === 0 ? 0 : Math.round((readyDone / readyTotal) * 100);

  return (
    <div
      className={`rounded-xl border transition-all duration-200 ${colors.bg} ${colors.border} ${
        isComplete ? "ring-1 ring-emerald-500/50" : ""
      }`}
    >
      {/* Level header */}
      <button
        onClick={() => setExpanded((e) => !e)}
        className="w-full flex items-center gap-3 p-4 text-left"
      >
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className={`text-xs font-bold px-2 py-0.5 rounded ${colors.badge}`}>
              L{levelData.level} · {levelData.label}
            </span>
            <span className="text-xs text-gray-500">{levelData.tag}</span>
            {isComplete && (
              <span className="text-xs font-bold text-emerald-400 bg-emerald-900/50 px-2 py-0.5 rounded level-complete-banner">
                ✓ Level Complete
              </span>
            )}
          </div>
        </div>
        <div className="flex items-center gap-3 shrink-0">
          <div className="text-right">
            <div className="text-xs text-gray-400">{readyDone}/{readyTotal} ready</div>
            <div className="h-1 w-20 rounded-full bg-gray-800 mt-1">
              <div
                className="h-full rounded-full transition-all"
                style={{ width: `${completionPct}%`, backgroundColor: isComplete ? "#22c55e" : domain.color }}
              />
            </div>
          </div>
          <span className="text-gray-600 text-sm">{expanded ? "▲" : "▼"}</span>
        </div>
      </button>

      {expanded && (
        <div className="px-4 pb-4 space-y-4">
          {/* What to Learn */}
          <div>
            <div className="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">
              📚 What to Learn
            </div>
            <ul className="space-y-1.5">
              {levelData.learn.map((item, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-gray-300">
                  <span className="mt-1 w-1.5 h-1.5 rounded-full shrink-0" style={{ backgroundColor: domain.color }} />
                  {item}
                </li>
              ))}
            </ul>
          </div>

          {/* Ready When */}
          <div>
            <div className="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-2">
              ✅ You're Ready When...
            </div>
            <div className="space-y-2">
              {levelData.ready.map((item, i) => {
                const key = `${domain.id}_L${levelData.level}_r${i}`;
                const done = !!checked[key];
                return (
                  <label
                    key={i}
                    className={`flex items-start gap-3 cursor-pointer rounded-lg p-2.5 transition-colors ${
                      done ? "bg-emerald-950/50" : "bg-gray-900/40 hover:bg-gray-800/40"
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={done}
                      onChange={() => toggle(key)}
                      className="mt-0.5 shrink-0 w-4 h-4 rounded accent-emerald-500"
                    />
                    <span className={`text-sm leading-relaxed ${done ? "text-emerald-400 line-through decoration-emerald-700" : "text-gray-300"}`}>
                      {item}
                    </span>
                  </label>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function DomainPanel({ domain, checked, toggle }) {
  const [expanded, setExpanded] = useState(false);

  const totalReady = domain.levels.reduce((sum, l) => sum + l.ready.length, 0);
  const doneReady = domain.levels.reduce(
    (sum, l) =>
      sum + l.ready.filter((_, i) => checked[`${domain.id}_L${l.level}_r${i}`]).length,
    0
  );
  const pct = totalReady === 0 ? 0 : Math.round((doneReady / totalReady) * 100);
  const isDomainComplete = pct === 100;

  return (
    <div className="rounded-2xl border border-gray-800 bg-gray-900/50 overflow-hidden">
      {/* Domain header */}
      <button
        onClick={() => setExpanded((e) => !e)}
        className="w-full flex items-center gap-4 p-5 text-left hover:bg-gray-800/30 transition-colors"
      >
        <span className="text-3xl shrink-0">{domain.icon}</span>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-1">
            <h3 className="font-bold text-white text-base">{domain.title}</h3>
            {isDomainComplete && (
              <span className="text-xs font-bold text-emerald-400 bg-emerald-900/50 px-2 py-0.5 rounded">
                🏆 Mastered
              </span>
            )}
          </div>
          <p className="text-xs text-gray-500 mb-2">{domain.subtitle}</p>
          <DomainProgressBar domain={domain} checked={checked} />
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <span className="text-sm font-bold" style={{ color: domain.color }}>{pct}%</span>
          <span className="text-gray-600">{expanded ? "▲" : "▼"}</span>
        </div>
      </button>

      {expanded && (
        <div className="px-5 pb-5 space-y-3">
          {domain.levels.map((levelData, i) => (
            <LevelCard
              key={levelData.level}
              domain={domain}
              levelData={levelData}
              checked={checked}
              toggle={toggle}
              levelIndex={i}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default function SkillRoadmap() {
  const { checked, toggle } = useRoadmapProgress();

  const totalReady = DOMAINS.reduce(
    (s, d) => s + d.levels.reduce((ss, l) => ss + l.ready.length, 0),
    0
  );
  const doneReady = DOMAINS.reduce(
    (s, d) =>
      s +
      d.levels.reduce(
        (ss, l) =>
          ss + l.ready.filter((_, i) => checked[`${d.id}_L${l.level}_r${i}`]).length,
        0
      ),
    0
  );

  return (
    <div className="max-w-4xl mx-auto">
      {/* Section stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
        {[
          { label: "Domains", value: DOMAINS.length },
          { label: "Skill Levels", value: "4 each" },
          { label: "Milestones", value: totalReady },
          { label: "Completed", value: `${doneReady}/${totalReady}` },
        ].map((s) => (
          <div key={s.label} className="bg-gray-900 border border-gray-800 rounded-xl p-3 text-center">
            <div className="text-xl font-bold text-white">{s.value}</div>
            <div className="text-xs text-gray-500 mt-0.5">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Overall progress */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 mb-6">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-semibold text-gray-300">Overall Roadmap Progress</span>
          <span className="text-sm font-bold text-white">
            {totalReady === 0 ? 0 : Math.round((doneReady / totalReady) * 100)}%
          </span>
        </div>
        <div className="h-2 rounded-full bg-gray-800">
          <div
            className="h-full rounded-full bg-emerald-500 transition-all duration-500"
            style={{ width: `${totalReady === 0 ? 0 : (doneReady / totalReady) * 100}%` }}
          />
        </div>
      </div>

      {/* Domain grid */}
      <div className="space-y-4">
        {DOMAINS.map((domain) => (
          <DomainPanel key={domain.id} domain={domain} checked={checked} toggle={toggle} />
        ))}
      </div>
    </div>
  );
}

// Export progress accessor for global header
export function getRoadmapProgress(checked) {
  const totalReady = DOMAINS.reduce(
    (s, d) => s + d.levels.reduce((ss, l) => ss + l.ready.length, 0),
    0
  );
  const doneReady = DOMAINS.reduce(
    (s, d) =>
      s +
      d.levels.reduce(
        (ss, l) =>
          ss + l.ready.filter((_, i) => checked[`${d.id}_L${l.level}_r${i}`]).length,
        0
      ),
    0
  );
  return { done: doneReady, total: totalReady };
}
