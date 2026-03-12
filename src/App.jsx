import { useState, useEffect, useCallback } from "react";
import SkillRoadmap from "./components/SkillRoadmap";
import DatasetLibrary from "./components/DatasetLibrary";
import CourseLibrary from "./components/CourseLibrary";
import { DOMAINS } from "./data/roadmapData";
import { DATASETS } from "./data/datasetData";
import { COURSES } from "./data/courseData";

const TABS = [
  { id: "roadmap",  label: "Skill Roadmap",    icon: "🗺️" },
  { id: "datasets", label: "Dataset Library",  icon: "🗂️" },
  { id: "courses",  label: "Course Library",   icon: "🎓" },
];

function computeOverallProgress() {
  // Roadmap
  let roadmapDone = 0, roadmapTotal = 0;
  try {
    const checked = JSON.parse(localStorage.getItem("roadmap_checked") || "{}");
    DOMAINS.forEach((d) =>
      d.levels.forEach((l) => {
        roadmapTotal += l.ready.length;
        roadmapDone += l.ready.filter((_, i) => checked[`${d.id}_L${l.level}_r${i}`]).length;
      })
    );
  } catch {}

  // Datasets
  let datasetDone = 0;
  try {
    const comp = JSON.parse(localStorage.getItem("dataset_completed") || "{}");
    datasetDone = Object.values(comp).filter(Boolean).length;
  } catch {}

  // Courses
  let courseDone = 0;
  try {
    const comp = JSON.parse(localStorage.getItem("course_completed") || "{}");
    courseDone = Object.values(comp).filter(Boolean).length;
  } catch {}

  const total = roadmapTotal + DATASETS.length + COURSES.length;
  const done = roadmapDone + datasetDone + courseDone;
  return { done, total, pct: total === 0 ? 0 : Math.round((done / total) * 100) };
}

export default function App() {
  const [activeTab, setActiveTab] = useState("roadmap");
  const [progress, setProgress] = useState(() => computeOverallProgress());
  const [saveFlash, setSaveFlash] = useState(false);

  // Recalculate progress whenever localStorage changes (via storage event or after tab switch)
  const refreshProgress = useCallback(() => {
    setProgress(computeOverallProgress());
    setSaveFlash(true);
    setTimeout(() => setSaveFlash(false), 1600);
  }, []);

  useEffect(() => {
    // Listen for storage changes from checkbox/toggle interactions
    const handler = () => refreshProgress();
    window.addEventListener("storage", handler);
    return () => window.removeEventListener("storage", handler);
  }, [refreshProgress]);

  // Refresh when switching tabs (catches same-tab changes)
  const handleTabSwitch = (tabId) => {
    setActiveTab(tabId);
    setTimeout(() => setProgress(computeOverallProgress()), 50);
  };

  // Intercept localStorage writes to trigger progress refresh
  useEffect(() => {
    const origSetItem = localStorage.setItem.bind(localStorage);
    localStorage.setItem = (key, value) => {
      origSetItem(key, value);
      if (["roadmap_checked", "dataset_completed", "course_completed"].includes(key)) {
        // Debounce slightly
        setTimeout(() => {
          setProgress(computeOverallProgress());
          setSaveFlash(true);
          setTimeout(() => setSaveFlash(false), 1600);
        }, 10);
      }
    };
    return () => {
      localStorage.setItem = origSetItem;
    };
  }, []);

  const { done, total, pct } = progress;

  return (
    <div className="min-h-screen bg-gray-950 text-gray-200 font-sans">
      {/* ── GLOBAL HEADER ── */}
      <header className="sticky top-0 z-30 bg-gray-950/95 backdrop-blur border-b border-gray-800">
        <div className="max-w-5xl mx-auto px-4 sm:px-6">
          <div className="flex items-center justify-between py-3 gap-4">
            {/* Brand */}
            <div className="flex items-center gap-3 min-w-0">
              <div className="w-9 h-9 rounded-xl bg-emerald-600/20 border border-emerald-600/30 flex items-center justify-center text-lg shrink-0">
                🧠
              </div>
              <div className="min-w-0">
                <h1 className="font-bold text-white text-sm sm:text-base leading-tight truncate">
                  Data Scientist Learning Hub
                </h1>
                <p className="text-xs text-gray-500 hidden sm:block">
                  Skill Roadmap · Datasets · Courses
                </p>
              </div>
            </div>

            {/* Global progress */}
            <div className="flex items-center gap-3 shrink-0">
              {/* Save indicator */}
              <span
                className={`text-xs text-emerald-400 font-medium transition-opacity ${
                  saveFlash ? "opacity-100" : "opacity-0"
                }`}
                aria-live="polite"
              >
                ✓ Saved
              </span>
              <div className="text-right">
                <div className="text-xs text-gray-500 mb-1">Overall Progress</div>
                <div className="flex items-center gap-2">
                  <div className="w-24 sm:w-32 h-1.5 rounded-full bg-gray-800">
                    <div
                      className="h-full rounded-full bg-emerald-500 transition-all duration-500"
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                  <span className="text-xs font-bold text-white w-8">{pct}%</span>
                </div>
              </div>
            </div>
          </div>

          {/* Tab nav */}
          <nav className="flex gap-0.5 pb-0" role="tablist">
            {TABS.map((tab) => {
              const active = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  role="tab"
                  aria-selected={active}
                  onClick={() => handleTabSwitch(tab.id)}
                  className={`flex items-center gap-1.5 px-4 py-2.5 text-sm font-medium border-b-2 transition-all rounded-t-lg ${
                    active
                      ? "border-emerald-500 text-white bg-gray-900/40"
                      : "border-transparent text-gray-400 hover:text-gray-200 hover:border-gray-700"
                  }`}
                >
                  <span>{tab.icon}</span>
                  <span className="hidden sm:inline">{tab.label}</span>
                  <span className="sm:hidden">{tab.label.split(" ")[0]}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </header>

      {/* ── MAIN CONTENT ── */}
      <main className="max-w-5xl mx-auto px-4 sm:px-6 py-6">
        {/* Summary cards for all 3 sections */}
        <div className="grid grid-cols-3 gap-3 mb-8">
          {(() => {
            const roadmapChecked = (() => {
              try { return JSON.parse(localStorage.getItem("roadmap_checked") || "{}"); } catch { return {}; }
            })();
            const roadmapTotal = DOMAINS.reduce((s, d) => s + d.levels.reduce((ss, l) => ss + l.ready.length, 0), 0);
            const roadmapDone = DOMAINS.reduce((s, d) => s + d.levels.reduce((ss, l) => ss + l.ready.filter((_, i) => roadmapChecked[`${d.id}_L${l.level}_r${i}`]).length, 0), 0);
            const datasetDone = (() => { try { return Object.values(JSON.parse(localStorage.getItem("dataset_completed") || "{}")).filter(Boolean).length; } catch { return 0; } })();
            const courseDone = (() => { try { return Object.values(JSON.parse(localStorage.getItem("course_completed") || "{}")).filter(Boolean).length; } catch { return 0; } })();
            return [
              { label: "🗺️ Roadmap", done: roadmapDone, total: roadmapTotal, tab: "roadmap" },
              { label: "🗂️ Datasets", done: datasetDone, total: DATASETS.length, tab: "datasets" },
              { label: "🎓 Courses", done: courseDone, total: COURSES.length, tab: "courses" },
            ].map((s) => {
              const sectionPct = s.total === 0 ? 0 : Math.round((s.done / s.total) * 100);
              return (
                <button
                  key={s.tab}
                  onClick={() => handleTabSwitch(s.tab)}
                  className={`bg-gray-900 border rounded-xl p-3 text-left transition-all hover:border-gray-700 ${
                    activeTab === s.tab ? "border-emerald-800/60 ring-1 ring-emerald-800/40" : "border-gray-800"
                  }`}
                >
                  <div className="text-xs text-gray-400 mb-1 font-medium">{s.label}</div>
                  <div className="flex items-end justify-between mb-2">
                    <span className="text-lg font-bold text-white">{sectionPct}%</span>
                    <span className="text-xs text-gray-500 font-mono">{s.done}/{s.total}</span>
                  </div>
                  <div className="h-1 rounded-full bg-gray-800">
                    <div
                      className="h-full rounded-full bg-emerald-500 transition-all"
                      style={{ width: `${sectionPct}%` }}
                    />
                  </div>
                </button>
              );
            });
          })()}
        </div>

        {/* Tab panels */}
        <div role="tabpanel">
          {activeTab === "roadmap"  && <SkillRoadmap />}
          {activeTab === "datasets" && <DatasetLibrary />}
          {activeTab === "courses"  && <CourseLibrary />}
        </div>
      </main>

      {/* Footer */}
      <footer className="max-w-5xl mx-auto px-4 sm:px-6 py-6 mt-4 border-t border-gray-900">
        <p className="text-xs text-gray-600 text-center">
          Data Scientist Learning Hub · All progress saved to browser localStorage · No backend needed
        </p>
      </footer>
    </div>
  );
}
