import { useState } from "react";

const COURSES = [
  // ─── DATA WRANGLING ───────────────────────────────────────────
  {
    id: "pandas-bootcamp",
    domain: "wrangling",
    levels: [1, 2],
    title: "The Complete Pandas Bootcamp 2025",
    instructor: "Alexander Hagmann",
    platform: "Udemy",
    hours: "36h",
    price: "Paid (~$15)",
    free: false,
    url: "https://www.udemy.com/course/the-pandas-bootcamp/",
    why: "The most thorough pandas course available. 150+ coding exercises, updated to pandas 2.x. Goes from zero to ML-ready data pipelines.",
    covers: ["pandas", "numpy", "matplotlib", "seaborn", "data cleaning", "merging", "time series"],
  },
  {
    id: "sql-masterclass",
    domain: "wrangling",
    levels: [1, 2],
    title: "The Complete SQL Bootcamp",
    instructor: "Jose Portilla",
    platform: "Udemy",
    hours: "9h",
    price: "Paid (~$15)",
    free: false,
    url: "https://www.udemy.com/course/the-complete-sql-bootcamp/",
    why: "Covers everything from basic SELECT to window functions and complex joins. Best-in-class SQL for analysts.",
    covers: ["SQL", "PostgreSQL", "joins", "window functions", "subqueries", "CTEs"],
  },
  {
    id: "mode-sql",
    domain: "wrangling",
    levels: [2, 3],
    title: "Mode SQL Tutorial (Advanced)",
    instructor: "Mode Analytics",
    platform: "Mode (Free)",
    hours: "Self-paced",
    price: "Free",
    free: true,
    url: "https://mode.com/sql-tutorial/",
    why: "The best free advanced SQL resource. Window functions, pivoting, performance tuning — all taught with real datasets in a browser.",
    covers: ["advanced SQL", "window functions", "pivoting", "performance", "analytics patterns"],
  },
  {
    id: "python-bootcamp",
    domain: "wrangling",
    levels: [1],
    title: "100 Days of Code: Python Pro Bootcamp",
    instructor: "Angela Yu",
    platform: "Udemy",
    hours: "60h",
    price: "Paid (~$15)",
    free: false,
    url: "https://www.udemy.com/course/100-days-of-code/",
    why: "The most engaging Python course for building real habits. 100 projects over 100 days — perfect for your hands-on learning style.",
    covers: ["Python fundamentals", "functions", "OOP", "file I/O", "APIs", "pandas", "Flask"],
  },

  // ─── STATISTICS ───────────────────────────────────────────────
  {
    id: "stats-thinking",
    domain: "stats",
    levels: [1, 2],
    title: "Statistics for Data Science and Business Analysis",
    instructor: "365 Careers",
    platform: "Udemy",
    hours: "9h",
    price: "Paid (~$15)",
    free: false,
    url: "https://www.udemy.com/course/statistics-for-data-science-and-business-analysis/",
    why: "Visual, business-focused stats. Covers distributions, hypothesis testing, regression, and A/B testing with real examples.",
    covers: ["descriptive stats", "distributions", "hypothesis testing", "regression", "confidence intervals"],
  },
  {
    id: "statquest",
    domain: "stats",
    levels: [1, 2, 3],
    title: "StatQuest with Josh Starmer (YouTube)",
    instructor: "Josh Starmer",
    platform: "YouTube (Free)",
    hours: "300+ videos",
    price: "Free",
    free: true,
    url: "https://www.youtube.com/@statquest",
    why: "The clearest statistics explanations on the internet. Every concept broken down intuitively with visuals. Essential companion to any stats course.",
    covers: ["probability", "distributions", "machine learning stats", "PCA", "p-values", "Bayes", "linear models"],
  },
  {
    id: "ab-testing-udacity",
    domain: "stats",
    levels: [2, 3],
    title: "A/B Testing by Google",
    instructor: "Google / Udacity",
    platform: "Udacity (Free)",
    hours: "~8h",
    price: "Free",
    free: true,
    url: "https://www.udacity.com/course/ab-testing--ud257",
    why: "The gold standard A/B testing course. Teaches experiment design, statistical significance, and common pitfalls from the people who run experiments at Google scale.",
    covers: ["experiment design", "statistical power", "sample size", "significance", "novelty effects", "business metrics"],
  },
  {
    id: "causal-inference",
    domain: "stats",
    levels: [3, 4],
    title: "Causal Inference: The Mixtape (Book + Videos)",
    instructor: "Scott Cunningham",
    platform: "Free Online",
    hours: "Self-paced",
    price: "Free",
    free: true,
    url: "https://mixtape.scunning.com/",
    why: "The best accessible guide to causal inference. DiD, regression discontinuity, IV — all explained with real econometrics examples.",
    covers: ["causal inference", "DiD", "regression discontinuity", "instrumental variables", "propensity scoring"],
  },

  // ─── MACHINE LEARNING ─────────────────────────────────────────
  {
    id: "andrew-ng-ml",
    domain: "ml",
    levels: [1, 2],
    title: "Machine Learning Specialization",
    instructor: "Andrew Ng",
    platform: "Coursera",
    hours: "~100h",
    price: "Free audit / $49/mo",
    free: true,
    url: "https://www.coursera.org/specializations/machine-learning-introduction",
    why: "The best-rated ML course ever made. 4.9 stars from 4.8M learners. Ng explains the intuition behind algorithms better than anyone. This is your L1-L2 ML foundation.",
    covers: ["supervised learning", "regression", "classification", "neural networks", "clustering", "anomaly detection", "recommender systems"],
  },
  {
    id: "python-ml-bootcamp",
    domain: "ml",
    levels: [2],
    title: "Python for Data Science and ML Bootcamp",
    instructor: "Jose Portilla",
    platform: "Udemy",
    hours: "25h",
    price: "Paid (~$15)",
    free: false,
    url: "https://www.udemy.com/course/python-for-data-science-and-machine-learning-bootcamp/",
    why: "Best hands-on scikit-learn course. Practical ML project-by-project with real datasets. Pairs perfectly with Andrew Ng's theory.",
    covers: ["scikit-learn", "feature engineering", "random forest", "gradient boosting", "cross-validation", "pipelines"],
  },
  {
    id: "deep-learning-spec",
    domain: "ml",
    levels: [3, 4],
    title: "Deep Learning Specialization",
    instructor: "Andrew Ng",
    platform: "Coursera",
    hours: "~80h",
    price: "Free audit / $49/mo",
    free: true,
    url: "https://www.coursera.org/specializations/deep-learning",
    why: "The definitive deep learning curriculum. Neural networks, CNNs, RNNs, tuning strategy — built by the person who built Google Brain.",
    covers: ["neural networks", "backpropagation", "CNNs", "RNNs", "LSTMs", "hyperparameter tuning", "project structuring"],
  },
  {
    id: "fastai",
    domain: "ml",
    levels: [3],
    title: "Practical Deep Learning for Coders",
    instructor: "Jeremy Howard",
    platform: "fast.ai (Free)",
    hours: "~50h",
    price: "Free",
    free: true,
    url: "https://course.fast.ai/",
    why: "Top-down, code-first approach. Build working models first, understand the math after. The best for people who learn by doing.",
    covers: ["deep learning", "CNNs", "NLP", "tabular data", "PyTorch", "transfer learning", "deployment"],
  },
  {
    id: "mlops-specialization",
    domain: "ml",
    levels: [3, 4],
    title: "MLOps Specialization",
    instructor: "Andrew Ng",
    platform: "Coursera / DeepLearning.AI",
    hours: "~40h",
    price: "Free audit / $49/mo",
    free: true,
    url: "https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops",
    why: "Closes the gap between model-building and production. Covers model deployment, monitoring, drift detection, and retraining pipelines.",
    covers: ["ML deployment", "model monitoring", "drift detection", "ML pipelines", "data validation", "serving infrastructure"],
  },

  // ─── VISUALIZATION ────────────────────────────────────────────
  {
    id: "tableau-analyst",
    domain: "viz",
    levels: [1, 2],
    title: "Tableau 2024 A-Z: Hands-On Tableau Training",
    instructor: "Kirill Eremenko",
    platform: "Udemy",
    hours: "9h",
    price: "Paid (~$15)",
    free: false,
    url: "https://www.udemy.com/course/tableau10/",
    why: "The most popular Tableau course on Udemy. Goes from connecting data to building executive dashboards. Very practical with business datasets.",
    covers: ["Tableau", "charts", "calculated fields", "LOD expressions", "dashboard design", "filters", "storytelling"],
  },
  {
    id: "data-viz-python",
    domain: "viz",
    levels: [1, 2],
    title: "Python Data Analysis & Visualization Masterclass",
    instructor: "Colt Steele",
    platform: "Udemy",
    hours: "22h",
    price: "Paid (~$15)",
    free: false,
    url: "https://www.udemy.com/course/python-data-analysis-visualization/",
    why: "Highest-rated Python visualization course. Covers matplotlib, seaborn, and Plotly with real datasets. Excellent for building chart intuition.",
    covers: ["matplotlib", "seaborn", "Plotly", "chart selection", "interactive charts", "storytelling with data"],
  },
  {
    id: "storytelling-data",
    domain: "viz",
    levels: [2, 3],
    title: "Storytelling with Data (YouTube Series + Book)",
    instructor: "Cole Nussbaumer Knaflic",
    platform: "YouTube (Free)",
    hours: "Self-paced",
    price: "Free",
    free: true,
    url: "https://www.youtube.com/@storytellingwithdata",
    why: "THE resource for data communication. Teaches how to design charts that drive decisions, not just display data. Pairs with the book perfectly.",
    covers: ["chart design", "decluttering", "audience focus", "narrative", "data presentation", "executive communication"],
  },

  // ─── DATA ENGINEERING ─────────────────────────────────────────
  {
    id: "de-bootcamp",
    domain: "engineering",
    levels: [2, 3],
    title: "Data Engineering Zoomcamp",
    instructor: "DataTalks.Club",
    platform: "GitHub / YouTube (Free)",
    hours: "~60h",
    price: "Free",
    free: true,
    url: "https://github.com/DataTalksClub/data-engineering-zoomcamp",
    why: "The best free end-to-end data engineering course. Builds a complete pipeline: ingestion → cloud → dbt → Spark → orchestration. Real projects, real tools.",
    covers: ["Docker", "PostgreSQL", "BigQuery", "dbt", "Spark", "Kafka", "Airflow", "Terraform", "cloud pipelines"],
  },
  {
    id: "dbt-bootcamp",
    domain: "engineering",
    levels: [2, 3],
    title: "The Complete dbt Bootcamp: Zero to Hero",
    instructor: "Zoltan Toth",
    platform: "Udemy",
    hours: "10h",
    price: "Paid (~$15)",
    free: false,
    url: "https://www.udemy.com/course/complete-dbt-data-build-tool-bootcamp-zero-to-hero-learn-dbt/",
    why: "The top-rated dbt course. Teaches the full dbt workflow with BigQuery, from staging models to deployment. Direct pipeline to analytics engineering roles.",
    covers: ["dbt", "BigQuery", "staging models", "marts", "testing", "documentation", "dbt Cloud"],
  },
  {
    id: "de-project-course",
    domain: "engineering",
    levels: [2, 3],
    title: "Data Engineering Project (SQL, Python, Airflow, Docker)",
    instructor: "Various",
    platform: "Udemy",
    hours: "~12h",
    price: "Paid (~$15)",
    free: false,
    url: "https://www.udemy.com/course/start-your-data-engineering-journey-project-based-learning/",
    why: "Project-based: PostgreSQL + Airflow + Docker + GitHub Actions. Builds a complete real pipeline you can put on your portfolio.",
    covers: ["PostgreSQL", "Airflow DAGs", "Docker", "Python ETL", "CI/CD", "data quality (SODA)"],
  },
  {
    id: "gcp-de",
    domain: "engineering",
    levels: [3, 4],
    title: "Google Cloud Data Engineer Professional Certificate",
    instructor: "Google Cloud",
    platform: "Coursera",
    hours: "~60h",
    price: "Free audit / $49/mo",
    free: true,
    url: "https://www.coursera.org/professional-certificates/gcp-data-engineering",
    why: "Build on the world's best cloud data platform. Covers BigQuery, Dataflow, Pub/Sub, Dataproc — the full GCP data stack.",
    covers: ["BigQuery", "Dataflow", "Cloud Storage", "Pub/Sub", "Dataproc", "Vertex AI", "streaming pipelines"],
  },

  // ─── AI / LLMs ────────────────────────────────────────────────
  {
    id: "deeplearning-ai-short",
    domain: "ai",
    levels: [1, 2],
    title: "DeepLearning.AI Short Courses (ChatGPT API, Prompt Eng)",
    instructor: "Andrew Ng / OpenAI / Anthropic",
    platform: "DeepLearning.AI (Free)",
    hours: "1–2h each",
    price: "Free",
    free: true,
    url: "https://www.deeplearning.ai/short-courses/",
    why: "1–2 hour focused courses from the people who built the models. 'ChatGPT Prompt Engineering for Developers' and 'Building Systems with ChatGPT API' are must-dos.",
    covers: ["prompt engineering", "ChatGPT API", "structured outputs", "function calling", "RAG basics", "LLM system design"],
  },
  {
    id: "llm-engineering",
    domain: "ai",
    levels: [2, 3],
    title: "LLM Engineering: Master AI & Large Language Models",
    instructor: "Ed Donner",
    platform: "Udemy",
    hours: "~35h",
    price: "Paid (~$15)",
    free: false,
    url: "https://www.udemy.com/course/llm-engineering-master-ai-and-large-language-models/",
    why: "Highly practical — 20+ models, RAG, QLoRA fine-tuning, and agents in one course. Build real products including a multi-modal assistant.",
    covers: ["LLM APIs", "RAG", "ChromaDB", "HuggingFace", "fine-tuning", "agents", "LangChain", "Gradio"],
  },
  {
    id: "langchain-agents",
    domain: "ai",
    levels: [3],
    title: "Agentic AI Engineering with LangChain & LangGraph",
    instructor: "Eden Marco",
    platform: "Udemy",
    hours: "18h",
    price: "Paid (~$15)",
    free: false,
    url: "https://www.udemy.com/course/langchain/",
    why: "Re-recorded for 2026. Builds production-ready agents with LangChain v1.2+, LangGraph, and MCP. ReAct, RAG, and multi-agent orchestration.",
    covers: ["LangChain", "LangGraph", "ReAct agents", "multi-agent systems", "RAG", "tool calling", "MCP"],
  },
  {
    id: "ibm-rag-agentic",
    domain: "ai",
    levels: [3, 4],
    title: "IBM RAG and Agentic AI Professional Certificate",
    instructor: "IBM",
    platform: "Coursera",
    hours: "~80h",
    price: "Free audit / $49/mo",
    free: true,
    url: "https://www.coursera.org/professional-certificates/ibm-rag-and-agentic-ai",
    why: "The most comprehensive certificate covering RAG pipelines, multi-agent systems (CrewAI, AG2), and multimodal AI. IBM-backed, portfolio-ready.",
    covers: ["RAG pipelines", "LangChain", "LangGraph", "CrewAI", "multimodal AI", "FAISS", "agent orchestration"],
  },

  // ─── SOFTWARE ENGINEERING ─────────────────────────────────────
  {
    id: "fastapi-rest",
    domain: "software",
    levels: [2, 3],
    title: "REST APIs with Flask and Python",
    instructor: "Jose Salvatierra",
    platform: "Udemy",
    hours: "17h",
    price: "Paid (~$15)",
    free: false,
    url: "https://www.udemy.com/course/rest-api-flask-and-python/",
    why: "The best Flask/REST API course for data folks. Teaches you to turn a model or dataset into a live API — the core software engineering skill for data scientists.",
    covers: ["Flask", "REST APIs", "SQLAlchemy", "authentication", "Docker", "deployment", "testing"],
  },
  {
    id: "docker-kubernetes",
    domain: "software",
    levels: [2, 3],
    title: "Docker & Kubernetes: The Practical Guide",
    instructor: "Maximilian Schwarzmüller",
    platform: "Udemy",
    hours: "24h",
    price: "Paid (~$15)",
    free: false,
    url: "https://www.udemy.com/course/docker-kubernetes-the-practical-guide/",
    why: "The clearest Docker course for developers who aren't DevOps. Teaches containerization and orchestration — essential for deploying data pipelines and ML models.",
    covers: ["Docker", "containers", "docker-compose", "Kubernetes basics", "deployment", "networking"],
  },
  {
    id: "git-complete",
    domain: "software",
    levels: [1, 2],
    title: "The Git & GitHub Bootcamp",
    instructor: "Colt Steele",
    platform: "Udemy",
    hours: "17h",
    price: "Paid (~$15)",
    free: false,
    url: "https://www.udemy.com/course/git-and-github-bootcamp/",
    why: "Covers everything from git init to rebasing and GitHub Actions. Modern, practical, and avoids the dry textbook approach.",
    covers: ["Git", "GitHub", "branches", "merging", "rebasing", "GitHub Actions", "CI/CD basics"],
  },
  {
    id: "cs50-python",
    domain: "software",
    levels: [1],
    title: "CS50's Introduction to Programming with Python",
    instructor: "Harvard / David Malan",
    platform: "edX / CS50 (Free)",
    hours: "~20h",
    price: "Free",
    free: true,
    url: "https://cs50.harvard.edu/python/",
    why: "Harvard's Python course — rigorous, fun, and free. Builds real software engineering habits (testing, error handling, clean code) that most data courses skip.",
    covers: ["Python", "OOP", "file I/O", "regular expressions", "unit testing", "libraries", "clean code"],
  },

  // ─── BUSINESS / STRATEGY ──────────────────────────────────────
  {
    id: "business-analytics-spec",
    domain: "business",
    levels: [2, 3],
    title: "Advanced Business Analytics Specialization",
    instructor: "University of Colorado",
    platform: "Coursera",
    hours: "~40h",
    price: "Free audit / $49/mo",
    free: true,
    url: "https://www.coursera.org/specializations/data-analytics-business",
    why: "Teaches the business framing layer — how to turn data questions into decisions. Covers forecasting, optimization, and communicating to executives.",
    covers: ["business framing", "forecasting", "optimization", "decision analysis", "stakeholder communication", "metrics frameworks"],
  },
  {
    id: "product-analytics",
    domain: "business",
    levels: [2, 3],
    title: "Product Analytics by Mixpanel (Free)",
    instructor: "Mixpanel",
    platform: "Mixpanel (Free)",
    hours: "~8h",
    price: "Free",
    free: true,
    url: "https://mixpanel.com/learn/",
    why: "Real product analytics thinking from the team that built the tool. Funnel analysis, cohort retention, and feature adoption — the core skills of product analytics.",
    covers: ["funnel analysis", "cohort retention", "feature adoption", "product metrics", "event tracking", "user segmentation"],
  },
  {
    id: "sql-business",
    domain: "business",
    levels: [2],
    title: "SQL for Business Analytics (Mode Analytics)",
    instructor: "Mode Analytics",
    platform: "Mode (Free)",
    hours: "Self-paced",
    price: "Free",
    free: true,
    url: "https://mode.com/sql-tutorial/sql-business-analytics",
    why: "Teaches SQL specifically through a business lens — cohort analysis, funnel queries, retention tables, and revenue breakdowns.",
    covers: ["business SQL", "cohort analysis", "retention", "funnel queries", "revenue analysis", "customer segmentation"],
  },
  {
    id: "google-data-analytics",
    domain: "business",
    levels: [1, 2],
    title: "Google Data Analytics Professional Certificate",
    instructor: "Google",
    platform: "Coursera",
    hours: "~180h",
    price: "Free audit / $49/mo",
    free: true,
    url: "https://www.coursera.org/professional-certificates/google-data-analytics",
    why: "You already have this cert, but if you haven't done all the capstone work — it's worth going back. Strong foundation in the analyst-to-stakeholder communication loop.",
    covers: ["data lifecycle", "SQL", "R basics", "Tableau", "stakeholder communication", "case study", "data ethics"],
  },
];

const DOMAINS = [
  { id: "all", label: "All", icon: "🌐", color: "#8B949E" },
  { id: "wrangling", label: "Data Wrangling", icon: "⚙️", color: "#E8A838" },
  { id: "stats", label: "Statistics", icon: "📐", color: "#5B8FD4" },
  { id: "ml", label: "Machine Learning", icon: "🧠", color: "#7C6FCD" },
  { id: "viz", label: "Visualization", icon: "📊", color: "#3BAE7E" },
  { id: "engineering", label: "Data Engineering", icon: "🏗️", color: "#E05C5C" },
  { id: "ai", label: "AI / LLMs", icon: "🤖", color: "#B06AD4" },
  { id: "software", label: "Software Eng.", icon: "💻", color: "#4AACB8" },
  { id: "business", label: "Business", icon: "🎯", color: "#D4954A" },
];

const PLATFORM_COLORS = {
  "Udemy": { bg: "#1e1a2e", text: "#A89FD4", border: "#3a3060" },
  "Coursera": { bg: "#0d1e2e", text: "#5B8FD4", border: "#1a3a5a" },
  "DeepLearning.AI (Free)": { bg: "#0d1e0d", text: "#5DB878", border: "#1a4a1a" },
  "fast.ai (Free)": { bg: "#0d1e0d", text: "#5DB878", border: "#1a4a1a" },
  "YouTube (Free)": { bg: "#2e1a0d", text: "#E87038", border: "#5a3010" },
  "GitHub / YouTube (Free)": { bg: "#0d1e0d", text: "#5DB878", border: "#1a4a1a" },
  "Mode (Free)": { bg: "#0d1e0d", text: "#5DB878", border: "#1a4a1a" },
  "Udacity (Free)": { bg: "#0d1e0d", text: "#5DB878", border: "#1a4a1a" },
  "Free Online": { bg: "#0d1e0d", text: "#5DB878", border: "#1a4a1a" },
  "Mixpanel (Free)": { bg: "#0d1e0d", text: "#5DB878", border: "#1a4a1a" },
  "edX / CS50 (Free)": { bg: "#0d1e0d", text: "#5DB878", border: "#1a4a1a" },
};

const LEVEL_COLORS = {
  1: { bg: "#0d1422", badge: "#1A2E50", text: "#6BA3D6" },
  2: { bg: "#0d1a0d", badge: "#1A3A20", text: "#5DB878" },
  3: { bg: "#1a0d2e", badge: "#3A1A50", text: "#A87FD4" },
  4: { bg: "#2e1a0d", badge: "#503010", text: "#D4934A" },
};

const LEVEL_NAMES = { 1: "Foundation", 2: "Practitioner", 3: "Applied Scientist", 4: "Master" };

export default function CourseCatalog() {
  const [activeDomain, setActiveDomain] = useState("all");
  const [freeOnly, setFreeOnly] = useState(false);
  const [expandedId, setExpandedId] = useState(null);
  const [completed, setCompleted] = useState({});
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
  const completedCount = Object.values(completed).filter(Boolean).length;
  const domainColor = (id) => DOMAINS.find((d) => d.id === id)?.color || "#8B949E";

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0D1117",
      color: "#C9D1D9",
      fontFamily: "'DM Sans', 'Segoe UI', system-ui, sans-serif",
    }}>
      {/* Header */}
      <div style={{
        background: "#0D1117",
        borderBottom: "1px solid #21262D",
        padding: "24px 28px 0",
        position: "sticky",
        top: 0,
        zIndex: 10,
      }}>
        <div style={{ maxWidth: 1100, margin: "0 auto" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 16, flexWrap: "wrap", gap: 12 }}>
            <div>
              <div style={{ fontSize: 10, letterSpacing: "0.2em", color: "#8B949E", textTransform: "uppercase", marginBottom: 4 }}>
                Applied Data Scientist · Video Course Library
              </div>
              <h1 style={{ margin: 0, fontSize: 22, fontWeight: 700, color: "#F0F6FC", letterSpacing: "-0.3px" }}>
                {COURSES.length} Curated Courses · 8 Domains
              </h1>
              <p style={{ margin: "4px 0 0", fontSize: 12, color: "#8B949E" }}>
                {freeCount} free · {COURSES.length - freeCount} paid (~$15 on Udemy sale) · Mapped to every roadmap level
              </p>
            </div>
            <div style={{ textAlign: "right" }}>
              <div style={{ fontSize: 10, color: "#8B949E", marginBottom: 2, textTransform: "uppercase", letterSpacing: "0.1em" }}>Completed</div>
              <div style={{ fontSize: 28, fontWeight: 800, color: "#F0F6FC", lineHeight: 1 }}>
                {completedCount}<span style={{ fontSize: 14, color: "#8B949E" }}>/{COURSES.length}</span>
              </div>
            </div>
          </div>

          {/* Search + Free toggle */}
          <div style={{ display: "flex", gap: 10, marginBottom: 14, flexWrap: "wrap" }}>
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by course, skill, or tool (e.g. 'RAG', 'dbt', 'Andrew Ng')..."
              style={{
                flex: 1, minWidth: 200,
                background: "#161B22", border: "1px solid #30363D",
                borderRadius: 6, padding: "8px 12px", color: "#C9D1D9",
                fontSize: 12, fontFamily: "inherit", outline: "none",
              }}
            />
            <button
              onClick={() => setFreeOnly(!freeOnly)}
              style={{
                padding: "8px 16px", borderRadius: 6, cursor: "pointer",
                border: `1px solid ${freeOnly ? "#2a5a2a" : "#30363D"}`,
                background: freeOnly ? "#1a3a1a" : "#161B22",
                color: freeOnly ? "#5DB878" : "#8B949E",
                fontSize: 12, fontWeight: freeOnly ? 600 : 400,
                fontFamily: "inherit",
              }}
            >
              🆓 Free Only
            </button>
          </div>

          {/* Domain Tabs */}
          <div style={{ display: "flex", gap: 2, overflowX: "auto", paddingBottom: 1 }}>
            {DOMAINS.map((d) => (
              <button
                key={d.id}
                onClick={() => setActiveDomain(d.id)}
                style={{
                  padding: "6px 12px",
                  background: "transparent", border: "none",
                  borderBottom: activeDomain === d.id ? `2px solid ${d.color}` : "2px solid transparent",
                  color: activeDomain === d.id ? "#F0F6FC" : "#8B949E",
                  fontSize: 11, fontWeight: activeDomain === d.id ? 600 : 400,
                  cursor: "pointer", whiteSpace: "nowrap",
                  fontFamily: "inherit", transition: "all 0.15s",
                }}
              >
                {d.icon} {d.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div style={{ maxWidth: 1100, margin: "0 auto", padding: "20px 28px" }}>
        <div style={{ fontSize: 11, color: "#8B949E", marginBottom: 16 }}>
          {filtered.length} course{filtered.length !== 1 ? "s" : ""} shown
          {search && ` matching "${search}"`}
          {freeOnly && " (free only)"}
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {filtered.map((course) => {
            const isExpanded = expandedId === course.id;
            const dc = domainColor(course.domain);
            const isDone = !!completed[course.id];
            const domainObj = DOMAINS.find((d) => d.id === course.domain);
            const platformStyle = PLATFORM_COLORS[course.platform] || { bg: "#161B22", text: "#8B949E", border: "#21262D" };

            return (
              <div
                key={course.id}
                style={{
                  background: isDone ? "#0d1a0d" : "#161B22",
                  border: `1px solid ${isExpanded ? dc : isDone ? "#2a5a2a" : "#21262D"}`,
                  borderRadius: 8,
                  overflow: "hidden",
                  transition: "border 0.15s",
                }}
              >
                {/* Card Header */}
                <div
                  onClick={() => setExpandedId(isExpanded ? null : course.id)}
                  style={{ padding: "14px 16px", cursor: "pointer", display: "flex", gap: 14, alignItems: "flex-start" }}
                >
                  {/* Domain icon badge */}
                  <div style={{
                    width: 36, height: 36, borderRadius: 8, flexShrink: 0,
                    background: `${dc}22`, border: `1px solid ${dc}44`,
                    display: "flex", alignItems: "center", justifyContent: "center",
                    fontSize: 18,
                  }}>
                    {domainObj?.icon}
                  </div>

                  <div style={{ flex: 1, minWidth: 0 }}>
                    {/* Title row */}
                    <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap", marginBottom: 3 }}>
                      <span style={{
                        fontSize: 14, fontWeight: 600,
                        color: isDone ? "#5DB878" : "#F0F6FC",
                        textDecoration: isDone ? "line-through" : "none",
                      }}>{course.title}</span>
                      {course.free && (
                        <span style={{
                          fontSize: 9, padding: "2px 6px", borderRadius: 3,
                          background: "#1a3a1a", color: "#5DB878", fontWeight: 700,
                          letterSpacing: "0.05em",
                        }}>FREE</span>
                      )}
                    </div>

                    {/* Instructor + Platform row */}
                    <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap", marginBottom: 8 }}>
                      <span style={{ fontSize: 12, color: "#8B949E" }}>{course.instructor}</span>
                      <span style={{ color: "#30363D" }}>·</span>
                      <span style={{
                        fontSize: 10, padding: "2px 8px", borderRadius: 4,
                        background: platformStyle.bg, color: platformStyle.text,
                        border: `1px solid ${platformStyle.border}`,
                        fontWeight: 600,
                      }}>{course.platform}</span>
                      <span style={{ fontSize: 11, color: "#8B949E" }}>{course.hours}</span>
                      <span style={{ fontSize: 11, color: course.free ? "#5DB878" : "#8B949E" }}>{course.price}</span>
                    </div>

                    {/* Level tags */}
                    <div style={{ display: "flex", flexWrap: "wrap", gap: 4 }}>
                      {course.levels.map((lv) => (
                        <span key={lv} style={{
                          fontSize: 9, padding: "2px 6px", borderRadius: 3,
                          background: LEVEL_COLORS[lv].badge,
                          color: LEVEL_COLORS[lv].text, fontWeight: 600,
                        }}>
                          L{lv} {LEVEL_NAMES[lv]}
                        </span>
                      ))}
                    </div>
                  </div>

                  <span style={{ fontSize: 12, color: "#30363D", flexShrink: 0 }}>{isExpanded ? "▲" : "▼"}</span>
                </div>

                {/* Expanded */}
                {isExpanded && (
                  <div style={{
                    borderTop: "1px solid #21262D",
                    padding: "16px 16px 16px 66px",
                  }}>
                    {/* Why this course */}
                    <div style={{
                      background: `${dc}11`, border: `1px solid ${dc}33`,
                      borderRadius: 6, padding: "10px 14px", marginBottom: 14,
                    }}>
                      <div style={{ fontSize: 10, fontWeight: 600, color: dc, textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 4 }}>
                        Why This Course
                      </div>
                      <p style={{ margin: 0, fontSize: 13, color: "#C9D1D9", lineHeight: 1.6 }}>{course.why}</p>
                    </div>

                    {/* Covers + Link */}
                    <div style={{ display: "grid", gridTemplateColumns: "1fr auto", gap: 16, alignItems: "start" }}>
                      <div>
                        <div style={{ fontSize: 10, color: "#8B949E", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 6 }}>Topics Covered</div>
                        <div style={{ display: "flex", flexWrap: "wrap", gap: 4 }}>
                          {course.covers.map((t) => (
                            <span key={t} style={{
                              fontSize: 10, padding: "2px 8px", borderRadius: 20,
                              background: "#0D1117", border: "1px solid #30363D", color: "#8B949E",
                            }}>{t}</span>
                          ))}
                        </div>
                      </div>

                      <div style={{ display: "flex", flexDirection: "column", gap: 8, alignItems: "flex-end" }}>
                        <a
                          href={course.url}
                          target="_blank"
                          rel="noreferrer"
                          style={{
                            padding: "8px 16px", borderRadius: 6, textDecoration: "none",
                            background: `${dc}22`, border: `1px solid ${dc}44`,
                            color: dc, fontSize: 12, fontWeight: 600, whiteSpace: "nowrap",
                          }}
                        >
                          → Open Course
                        </a>
                        <button
                          onClick={(e) => { e.stopPropagation(); setCompleted(p => ({ ...p, [course.id]: !p[course.id] })); }}
                          style={{
                            padding: "6px 16px", borderRadius: 6, cursor: "pointer",
                            border: `1px solid ${isDone ? "#2a5a2a" : "#30363D"}`,
                            background: isDone ? "#1a3a1a" : "#161B22",
                            color: isDone ? "#5DB878" : "#8B949E",
                            fontSize: 11, fontFamily: "inherit", fontWeight: 600,
                            whiteSpace: "nowrap",
                          }}
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
          <div style={{ textAlign: "center", padding: "60px 20px", color: "#8B949E" }}>
            <div style={{ fontSize: 32, marginBottom: 12 }}>🎓</div>
            <div style={{ fontSize: 14 }}>No courses match your filters</div>
          </div>
        )}

        {/* Legend */}
        <div style={{ marginTop: 32, padding: "16px 20px", background: "#161B22", borderRadius: 8, border: "1px solid #21262D" }}>
          <div style={{ fontSize: 11, color: "#8B949E", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 10 }}>Suggested Learning Order</div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 8 }}>
            {[
              { phase: "Phase 1 (Now)", items: ["Data Wrangling L1-2", "Stats L1", "Software Eng. L1"], color: "#6BA3D6" },
              { phase: "Phase 2", items: ["Wrangling L3", "Stats L2-3", "ML L1-2", "Viz L1-2"], color: "#5DB878" },
              { phase: "Phase 3", items: ["ML L3", "Data Eng. L2-3", "AI/LLMs L1-2", "Business L2"], color: "#A87FD4" },
              { phase: "Phase 4 (Master)", items: ["ML L4", "AI/LLMs L3-4", "DE L4", "Business L3-4"], color: "#D4934A" },
            ].map((p) => (
              <div key={p.phase}>
                <div style={{ fontSize: 11, fontWeight: 700, color: p.color, marginBottom: 4 }}>{p.phase}</div>
                {p.items.map((item) => (
                  <div key={item} style={{ fontSize: 11, color: "#8B949E", marginBottom: 2 }}>→ {item}</div>
                ))}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
