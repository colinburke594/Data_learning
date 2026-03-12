import { useState } from "react";
import { COURSES, DOMAIN_FILTERS, LEVEL_NAMES } from "../data/courseData";

const LEVEL_BADGE = {
  1: "bg-blue-900/60 text-blue-300",
  2: "bg-emerald-900/60 text-emerald-300",
  3: "bg-purple-900/60 text-purple-300",
  4: "bg-orange-900/60 text-orange-300",
};

const PLATFORM_STYLES = {
  "Udemy":                      { bg: "bg-violet-950/60", text: "text-violet-300", border: "border-violet-900/40" },
  "Coursera":                   { bg: "bg-blue-950/60",   text: "text-blue-300",   border: "border-blue-900/40" },
  "DeepLearning.AI (Free)":     { bg: "bg-emerald-950/60",text: "text-emerald-300",border: "border-emerald-900/40" },
  "fast.ai (Free)":             { bg: "bg-emerald-950/60",text: "text-emerald-300",border: "border-emerald-900/40" },
  "YouTube (Free)":             { bg: "bg-red-950/60",    text: "text-red-300",    border: "border-red-900/40" },
  "GitHub / YouTube (Free)":    { bg: "bg-emerald-950/60",text: "text-emerald-300",border: "border-emerald-900/40" },
  "Mode (Free)":                { bg: "bg-emerald-950/60",text: "text-emerald-300",border: "border-emerald-900/40" },
  "Udacity (Free)":             { bg: "bg-emerald-950/60",text: "text-emerald-300",border: "border-emerald-900/40" },
  "Free Online":                { bg: "bg-emerald-950/60",text: "text-emerald-300",border: "border-emerald-900/40" },
  "Mixpanel (Free)":            { bg: "bg-emerald-950/60",text: "text-emerald-300",border: "border-emerald-900/40" },
  "edX / CS50 (Free)":          { bg: "bg-emerald-950/60",text: "text-emerald-300",border: "border-emerald-900/40" },
  "Coursera / DeepLearning.AI": { bg: "bg-blue-950/60",   text: "text-blue-300",   border: "border-blue-900/40" },
};

function useCourseCompletion() {
  const [completed, setCompleted] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem("course_completed") || "{}");
    } catch {
      return {};
    }
  });

  const toggle = (id) => {
    setCompleted((prev) => {
      const next = { ...prev, [id]: !prev[id] };
      localStorage.setItem("course_completed", JSON.stringify(next));
      return next;
    });
  };

  return { completed, toggle };
}

export default function CourseLibrary() {
  const { completed, toggle } = useCourseCompletion();
  const [activeDomain, setActiveDomain] = useState("all");
  const [freeOnly, setFreeOnly] = useState(false);
  const [expandedId, setExpandedId] = useState(null);
  const [search, setSearch] = useState("");

  const filtered = COURSES.filter((c) => {
    const dMatch = activeDomain === "all" || c.domain === activeDomain;
    const fMatch = !freeOnly || c.free;
    const sMatch =
      search.length < 2 ||
      c.title.toLowerCase().includes(search.toLowerCase()) ||
      c.covers.some((t) => t.toLowerCase().includes(search.toLowerCase())) ||
      c.instructor.toLowerCase().includes(search.toLowerCase());
    return dMatch && fMatch && sMatch;
  });

  const freeCount = COURSES.filter((c) => c.free).length;
  const totalCount = COURSES.length;
  const completedCount = Object.values(completed).filter(Boolean).length;

  const domainColor = (id) => DOMAIN_FILTERS.find((d) => d.id === id)?.color || "#8B949E";
  const domainIcon = (id) => DOMAIN_FILTERS.find((d) => d.id === id)?.icon || "📚";

  return (
    <div className="max-w-4xl mx-auto">
      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
        {[
          { label: "Total Courses", value: totalCount },
          { label: "Free", value: freeCount },
          { label: "Completed", value: completedCount },
          { label: "Progress", value: `${totalCount === 0 ? 0 : Math.round((completedCount / totalCount) * 100)}%` },
        ].map((s) => (
          <div key={s.label} className="bg-gray-900 border border-gray-800 rounded-xl p-3 text-center">
            <div className="text-xl font-bold text-white">{s.value}</div>
            <div className="text-xs text-gray-500 mt-0.5">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Progress bar */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-4 mb-6">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-semibold text-gray-300">Course Completion</span>
          <span className="text-sm font-bold text-white">{completedCount}/{totalCount}</span>
        </div>
        <div className="h-2 rounded-full bg-gray-800">
          <div
            className="h-full rounded-full bg-emerald-500 transition-all duration-500"
            style={{ width: `${totalCount === 0 ? 0 : (completedCount / totalCount) * 100}%` }}
          />
        </div>
      </div>

      {/* Filters row */}
      <div className="flex flex-col sm:flex-row gap-3 mb-4">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search by title, skill, or instructor..."
          className="flex-1 bg-gray-900 border border-gray-800 rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-gray-600 transition-colors"
        />
        <button
          onClick={() => setFreeOnly((f) => !f)}
          className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold border transition-all shrink-0 ${
            freeOnly
              ? "bg-emerald-950/50 border-emerald-700 text-emerald-400"
              : "bg-gray-900 border-gray-800 text-gray-400 hover:border-gray-700"
          }`}
        >
          🆓 Free Only
        </button>
      </div>

      {/* Domain filter tabs */}
      <div className="flex gap-1.5 flex-wrap mb-5">
        {DOMAIN_FILTERS.map((f) => {
          const count = f.id === "all"
            ? COURSES.length
            : COURSES.filter((c) => c.domain === f.id).length;
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

      <div className="text-xs text-gray-500 mb-4">
        {filtered.length} course{filtered.length !== 1 ? "s" : ""} shown
        {search && ` matching "${search}"`}
        {freeOnly && " · free only"}
      </div>

      {/* Course list */}
      <div className="space-y-3">
        {filtered.map((course) => {
          const isDone = !!completed[course.id];
          const isExpanded = expandedId === course.id;
          const dc = domainColor(course.domain);
          const icon = domainIcon(course.domain);
          const ps = PLATFORM_STYLES[course.platform] || { bg: "bg-gray-900", text: "text-gray-400", border: "border-gray-800" };

          return (
            <div
              key={course.id}
              className={`rounded-xl border overflow-hidden transition-all duration-200 ${
                isDone
                  ? "bg-emerald-950/20 border-emerald-900/50"
                  : isExpanded
                  ? "bg-gray-900 border-gray-700"
                  : "bg-gray-900/60 border-gray-800 hover:border-gray-700"
              }`}
            >
              {/* Card header */}
              <div
                className="flex items-start gap-4 p-4 cursor-pointer"
                onClick={() => setExpandedId(isExpanded ? null : course.id)}
              >
                {/* Domain icon */}
                <div
                  className="w-10 h-10 rounded-lg shrink-0 flex items-center justify-center text-xl border"
                  style={{ backgroundColor: `${dc}22`, borderColor: `${dc}44` }}
                >
                  {icon}
                </div>

                <div className="flex-1 min-w-0">
                  {/* Title + free badge */}
                  <div className="flex items-center gap-2 flex-wrap mb-1">
                    <span className={`font-semibold text-sm leading-snug ${isDone ? "text-emerald-400 line-through decoration-emerald-700" : "text-white"}`}>
                      {course.title}
                    </span>
                    {course.free && (
                      <span className="text-xs font-bold text-emerald-400 bg-emerald-900/50 px-1.5 py-0.5 rounded shrink-0">
                        FREE
                      </span>
                    )}
                    {isDone && (
                      <span className="text-xs font-bold text-emerald-400 bg-emerald-900/40 px-1.5 py-0.5 rounded shrink-0">
                        ✓ Done
                      </span>
                    )}
                  </div>

                  {/* Instructor + platform row */}
                  <div className="flex items-center gap-2 flex-wrap mb-2">
                    <span className="text-xs text-gray-400">{course.instructor}</span>
                    <span className="text-gray-700">·</span>
                    <span className={`text-xs px-2 py-0.5 rounded border font-medium ${ps.bg} ${ps.text} ${ps.border}`}>
                      {course.platform}
                    </span>
                    <span className="text-xs text-gray-500">{course.hours}</span>
                    <span className={`text-xs font-medium ${course.free ? "text-emerald-400" : "text-gray-500"}`}>
                      {course.price}
                    </span>
                  </div>

                  {/* Level tags */}
                  <div className="flex flex-wrap gap-1">
                    {course.levels.map((lv) => (
                      <span
                        key={lv}
                        className={`text-xs px-1.5 py-0.5 rounded font-mono ${LEVEL_BADGE[lv]}`}
                      >
                        L{lv} {LEVEL_NAMES[lv]}
                      </span>
                    ))}
                  </div>
                </div>

                <span className="text-gray-600 text-sm shrink-0 mt-1">{isExpanded ? "▲" : "▼"}</span>
              </div>

              {/* Expanded */}
              {isExpanded && (
                <div className="border-t border-gray-800 px-4 pb-4 pt-4 space-y-4">
                  {/* Why this course */}
                  <div
                    className="rounded-lg p-3 border text-sm"
                    style={{ backgroundColor: `${dc}11`, borderColor: `${dc}33` }}
                  >
                    <div className="text-xs font-bold uppercase tracking-wider mb-1" style={{ color: dc }}>
                      Why This Course
                    </div>
                    <p className="text-gray-300 leading-relaxed">{course.why}</p>
                  </div>

                  {/* Topics + actions */}
                  <div className="flex flex-col sm:flex-row gap-4 items-start">
                    <div className="flex-1">
                      <div className="text-xs text-gray-500 uppercase tracking-wider mb-2">Topics Covered</div>
                      <div className="flex flex-wrap gap-1.5">
                        {course.covers.map((t) => (
                          <span
                            key={t}
                            className="text-xs px-2 py-0.5 rounded-full bg-gray-800 border border-gray-700 text-gray-400"
                          >
                            {t}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div className="flex flex-col gap-2 shrink-0">
                      <a
                        href={course.url}
                        target="_blank"
                        rel="noreferrer"
                        className="px-4 py-2 rounded-lg text-sm font-semibold border text-center transition-all"
                        style={{
                          backgroundColor: `${dc}22`,
                          borderColor: `${dc}44`,
                          color: dc,
                        }}
                      >
                        → Open Course
                      </a>
                      <button
                        onClick={(e) => { e.stopPropagation(); toggle(course.id); }}
                        className={`px-4 py-2 rounded-lg text-sm font-semibold border transition-all ${
                          isDone
                            ? "bg-emerald-950/50 border-emerald-700 text-emerald-400 hover:bg-emerald-900/40"
                            : "bg-gray-800 border-gray-700 text-gray-300 hover:border-gray-600"
                        }`}
                      >
                        {isDone ? "✓ Completed" : "Mark Complete"}
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {filtered.length === 0 && (
        <div className="text-center py-16 text-gray-500">
          <div className="text-4xl mb-3">🎓</div>
          <div>No courses match your filters</div>
        </div>
      )}

      {/* Learning order legend */}
      <div className="mt-8 p-4 bg-gray-900 border border-gray-800 rounded-xl">
        <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Suggested Learning Order</div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {[
            { phase: "Phase 1", items: ["Wrangling L1-2", "Stats L1", "Software L1"], color: "#6BA3D6" },
            { phase: "Phase 2", items: ["Wrangling L3", "Stats L2-3", "ML L1-2", "Viz L1-2"], color: "#5DB878" },
            { phase: "Phase 3", items: ["ML L3", "Data Eng. L2-3", "AI L1-2", "Business L2"], color: "#A87FD4" },
            { phase: "Phase 4", items: ["ML L4", "AI L3-4", "DE L4", "Business L3-4"], color: "#D4934A" },
          ].map((p) => (
            <div key={p.phase}>
              <div className="text-xs font-bold mb-1.5" style={{ color: p.color }}>{p.phase}</div>
              {p.items.map((item) => (
                <div key={item} className="text-xs text-gray-500 mb-1">→ {item}</div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export function getCourseProgress() {
  try {
    const completed = JSON.parse(localStorage.getItem("course_completed") || "{}");
    return {
      done: Object.values(completed).filter(Boolean).length,
      total: COURSES.length,
    };
  } catch {
    return { done: 0, total: COURSES.length };
  }
}
