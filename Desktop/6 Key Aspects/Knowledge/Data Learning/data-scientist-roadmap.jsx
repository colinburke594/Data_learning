import { useState } from "react";

const DOMAINS = [
  {
    id: "wrangling",
    icon: "⚙️",
    title: "Data Wrangling & Analysis",
    subtitle: "The engine room — where raw data becomes usable",
    color: "#E8A838",
    levels: [
      {
        level: 1,
        label: "Foundation",
        tag: "Can follow along",
        learn: [
          "Python basics: variables, loops, functions, conditionals",
          "pandas: read CSV/Excel, filter rows, select columns, sort, groupby basics",
          "SQL: SELECT, WHERE, GROUP BY, JOIN (INNER, LEFT), ORDER BY, LIMIT",
          "Excel: VLOOKUP/XLOOKUP, pivot tables, basic formulas (SUM, IF, COUNTIF)",
          "Understand data types: strings, integers, floats, datetimes, booleans",
          "Identify and handle nulls/missing values (dropna, fillna)",
        ],
        ready: [
          "You can load a messy CSV and produce a clean summary table without Googling every step",
          "You can answer 'top 5 products by revenue last quarter' in both Python AND SQL",
          "You can build a pivot table in Excel from scratch in under 5 minutes",
          "You can explain what a NULL value is and 3 ways to handle it",
        ],
      },
      {
        level: 2,
        label: "Practitioner",
        tag: "Can do it independently",
        learn: [
          "pandas: merge/join DataFrames, apply(), lambda, pivot_table, melt/stack",
          "String manipulation, regex basics, datetime parsing and arithmetic",
          "SQL: window functions (ROW_NUMBER, RANK, LAG/LEAD, SUM OVER), CTEs, subqueries",
          "Data type conversion, encoding categorical variables",
          "Detecting & handling outliers (IQR, z-score methods)",
          "Working with multiple data sources simultaneously",
          "Excel: INDEX/MATCH, dynamic arrays, SUMIFS, data validation",
        ],
        ready: [
          "You can join 3+ tables in SQL with window functions to build a cohort analysis",
          "You can take a raw dataset with mixed types, inconsistencies, and duplicates and fully clean it in pandas without help",
          "You can write a reusable Python function that processes a new month of data with one call",
          "You can explain the difference between a CTE and a subquery and when to use each",
        ],
      },
      {
        level: 3,
        label: "Applied Scientist",
        tag: "Can design and lead it",
        learn: [
          "Build automated data cleaning pipelines (parameterized, reusable)",
          "Profiling libraries: ydata-profiling, great_expectations for data quality checks",
          "Advanced pandas: chunking large files, memory optimization, vectorization",
          "SQLAlchemy for Python-DB integration; writing and calling stored procedures",
          "Handling JSON/nested data, API response parsing",
          "Time series data manipulation: resampling, rolling windows, lag features",
        ],
        ready: [
          "You can design a data pipeline from scratch given a business problem and source data",
          "You can set up automated data quality checks that alert when data breaks assumptions",
          "You can optimize a slow pandas script by 5–10x using vectorization",
          "You can ingest data from a REST API, clean it, and load it into a database in one script",
        ],
      },
      {
        level: 4,
        label: "Master",
        tag: "End-to-end ownership",
        learn: [
          "Design scalable data models (star schema, data vault concepts)",
          "Orchestrate pipelines: Airflow/Prefect basics, cron scheduling",
          "Implement data contracts and SLAs between teams",
          "Build self-healing pipelines with error handling, retries, logging",
          "Profile and optimize queries for large-scale datasets (millions of rows+)",
        ],
        ready: [
          "You can architect the full data layer of a business solution — from ingestion to clean tables — and hand it off to someone else to maintain",
          "You can diagnose a broken pipeline, find the root cause, and add guardrails so it doesn't happen again",
          "You can explain your data model to both a data engineer and a business stakeholder",
        ],
      },
    ],
  },
  {
    id: "stats",
    icon: "📐",
    title: "Statistics & Mathematics",
    subtitle: "The reasoning layer — making sure your conclusions are real",
    color: "#5B8FD4",
    levels: [
      {
        level: 1,
        label: "Foundation",
        tag: "Can follow along",
        learn: [
          "Descriptive stats: mean, median, mode, variance, standard deviation",
          "Distributions: normal, uniform, skewed — what they look like and why it matters",
          "Correlation vs. causation — the most important distinction in data",
          "Basic probability: P(A), P(A and B), P(A or B), conditional probability",
          "Percentiles and quartiles (the IQR concept)",
        ],
        ready: [
          "You can look at a distribution and describe it accurately (shape, center, spread, outliers)",
          "You can explain why correlation ≠ causation with a real example",
          "You can calculate mean, median, std from scratch without a library",
          "You can explain what a p-value is to a non-technical person",
        ],
      },
      {
        level: 2,
        label: "Practitioner",
        tag: "Can do it independently",
        learn: [
          "Hypothesis testing: t-test, chi-square, ANOVA — when to use each",
          "Confidence intervals and what they actually mean",
          "A/B testing fundamentals: sample size, statistical power, significance",
          "Linear regression: assumptions, coefficients, R², residuals",
          "Bayes' theorem and Bayesian thinking basics",
          "Central Limit Theorem and why it matters for inference",
        ],
        ready: [
          "You can design and evaluate an A/B test end-to-end, including choosing sample size before running it",
          "You can run a linear regression, interpret every output number, and explain the assumptions being violated",
          "You can decide which statistical test to use given a business question and data type",
          "You can explain Type I vs Type II error using a business example",
        ],
      },
      {
        level: 3,
        label: "Applied Scientist",
        tag: "Can design and lead it",
        learn: [
          "Multivariate regression, interaction terms, polynomial features",
          "Logistic regression: log-odds, probabilities, decision boundaries",
          "Resampling methods: bootstrap, cross-validation, permutation tests",
          "Bayesian inference: priors, posteriors, credible intervals",
          "Multiple testing correction: Bonferroni, FDR (Benjamini-Hochberg)",
          "Causal inference basics: DiD, regression discontinuity, instrumental variables",
        ],
        ready: [
          "You can run a causal analysis (not just correlation) to answer 'did this intervention work?'",
          "You can identify and correct for multiple testing problems in an experiment suite",
          "You can explain when frequentist vs. Bayesian approaches are preferable for a business decision",
          "You can set up and interpret a logistic regression for a classification business problem",
        ],
      },
      {
        level: 4,
        label: "Master",
        tag: "End-to-end ownership",
        learn: [
          "Design experiment platforms and measurement frameworks for organizations",
          "Bayesian hierarchical models for complex business data",
          "Sensitivity analysis and robustness checks for statistical claims",
          "Communicate statistical uncertainty to executives without oversimplifying",
        ],
        ready: [
          "You can design the statistics infrastructure for how a company runs experiments",
          "You can defend your statistical methodology to a skeptical senior data scientist",
          "You can translate statistical findings into business risk and dollar impact",
        ],
      },
    ],
  },
  {
    id: "ml",
    icon: "🧠",
    title: "Machine Learning",
    subtitle: "The prediction engine — turning patterns into decisions",
    color: "#7C6FCD",
    levels: [
      {
        level: 1,
        label: "Foundation",
        tag: "Can follow along",
        learn: [
          "Supervised vs. unsupervised vs. reinforcement learning — the big picture",
          "Train/validation/test split and why leakage is dangerous",
          "Scikit-learn workflow: fit, predict, score",
          "Linear/logistic regression as ML models (not just stats tools)",
          "Decision trees: how they split, overfitting, depth control",
          "Evaluation metrics: accuracy, precision, recall, F1, RMSE, MAE",
        ],
        ready: [
          "You can build a working classification model in scikit-learn from raw data to predictions",
          "You can explain why you'd use precision vs. recall depending on the business context",
          "You can identify data leakage in a pipeline and explain why it makes results meaningless",
          "You can explain the bias-variance tradeoff using a non-technical analogy",
        ],
      },
      {
        level: 2,
        label: "Practitioner",
        tag: "Can do it independently",
        learn: [
          "Feature engineering: encoding, scaling, interaction features, feature selection",
          "Cross-validation: k-fold, stratified k-fold, time-series CV",
          "Ensemble methods: Random Forest, Gradient Boosting (XGBoost, LightGBM)",
          "Hyperparameter tuning: GridSearchCV, RandomizedSearchCV, Optuna",
          "Handling class imbalance: SMOTE, class weights, threshold tuning",
          "Clustering: K-means, DBSCAN, hierarchical — choosing and evaluating",
          "Dimensionality reduction: PCA, UMAP",
        ],
        ready: [
          "You can take a business problem, frame it as an ML problem, build a model, and beat a baseline",
          "You can tune an XGBoost model and explain what each hyperparameter does",
          "You can handle a dataset with 95/5 class imbalance and still get a meaningful model",
          "You can choose the right algorithm for a given dataset size, type, and business goal",
        ],
      },
      {
        level: 3,
        label: "Applied Scientist",
        tag: "Can design and lead it",
        learn: [
          "Model interpretability: SHAP values, LIME, partial dependence plots",
          "Neural networks: feedforward, activation functions, backprop intuition, PyTorch/Keras basics",
          "Time series forecasting: ARIMA, Prophet, LSTM",
          "Recommendation systems: collaborative filtering, content-based",
          "MLflow or similar: experiment tracking, model registry",
          "Model monitoring: drift detection, performance degradation",
        ],
        ready: [
          "You can explain any model's prediction to a business stakeholder using SHAP",
          "You can build a time series forecast for a business metric with confidence intervals",
          "You can track experiments systematically and reproduce any past result",
          "You can detect when a deployed model starts degrading and know what to do",
        ],
      },
      {
        level: 4,
        label: "Master",
        tag: "End-to-end ownership",
        learn: [
          "Full ML system design: from problem framing to monitoring in production",
          "Custom loss functions and evaluation metrics aligned to business outcomes",
          "AutoML tools and when they're appropriate vs. custom work",
          "Multi-model architectures: stacking, blending, cascade classifiers",
          "Cost-sensitive learning: tying model decisions to real business value",
        ],
        ready: [
          "You can scope, build, deploy, and maintain an ML system that improves a business KPI",
          "You can present the ROI of a model to a CFO (not just the accuracy score)",
          "You can design the retraining and monitoring strategy for a production ML system",
        ],
      },
    ],
  },
  {
    id: "viz",
    icon: "📊",
    title: "Visualization & Communication",
    subtitle: "The translation layer — making data mean something to anyone",
    color: "#3BAE7E",
    levels: [
      {
        level: 1,
        label: "Foundation",
        tag: "Can follow along",
        learn: [
          "Chart selection: when to use bar, line, scatter, histogram, pie (and when NOT to)",
          "matplotlib/seaborn basics: labels, titles, colors, gridlines",
          "Tableau or Power BI: connect data source, build a bar/line chart, add filters",
          "Storytelling rule: one chart = one message",
          "Color theory basics: avoid rainbow palettes, use colorblind-safe options",
        ],
        ready: [
          "You can look at a chart and immediately spot what's wrong with it (misleading axes, wrong chart type, no title)",
          "You can build a clean, publication-ready chart in Python from scratch",
          "You can connect a dataset in Tableau and build a basic dashboard in under an hour",
          "You can explain why a pie chart with 8 slices is almost always the wrong choice",
        ],
      },
      {
        level: 2,
        label: "Practitioner",
        tag: "Can do it independently",
        learn: [
          "Plotly/Altair for interactive charts",
          "Dashboard design principles: layout, hierarchy, progressive disclosure",
          "Tableau: calculated fields, LOD expressions, dashboard actions",
          "Data storytelling: hook → tension → resolution narrative structure",
          "Presenting to non-technical audiences: lead with the 'so what'",
          "Executive-level slide design: one insight per slide, no clutter",
        ],
        ready: [
          "You can build an interactive dashboard that a non-analyst can explore on their own",
          "You can present a data analysis to a senior leader in 5 minutes and get a decision",
          "You can take a complex finding and write a one-paragraph summary that a CEO would act on",
          "Someone can look at your dashboard and understand the main insight in under 10 seconds",
        ],
      },
      {
        level: 3,
        label: "Applied Scientist",
        tag: "Can design and lead it",
        learn: [
          "Build custom visualization components (D3.js basics or Plotly Dash apps)",
          "Design BI reporting systems that self-serve for business teams",
          "Advanced Tableau: performance optimization, extract vs. live, embedding",
          "Metrics frameworks: choosing the right KPIs, north star metrics, leading vs. lagging",
          "Communicating uncertainty: confidence intervals, scenarios in charts",
        ],
        ready: [
          "You can design the analytics reporting structure for a department or product",
          "You can build a live Plotly Dash or Streamlit app that a business team uses daily",
          "You can facilitate a metrics workshop with stakeholders to define what 'good' looks like",
          "You can show uncertainty ranges in your charts without confusing your audience",
        ],
      },
      {
        level: 4,
        label: "Master",
        tag: "End-to-end ownership",
        learn: [
          "Design the data storytelling and reporting culture for an organization",
          "Build custom data products that democratize analytics access",
          "Connect visualization strategy to decision-making frameworks (OKRs, KPIs, experiments)",
        ],
        ready: [
          "Business leaders actively use dashboards you built to make weekly decisions",
          "You can teach others your visualization framework and they improve immediately",
          "You can influence the metrics culture of an organization, not just report numbers",
        ],
      },
    ],
  },
  {
    id: "engineering",
    icon: "🏗️",
    title: "Data Engineering & Pipelines",
    subtitle: "The infrastructure layer — making data reliable at scale",
    color: "#E05C5C",
    levels: [
      {
        level: 1,
        label: "Foundation",
        tag: "Can follow along",
        learn: [
          "Understand ETL vs. ELT and when each is used",
          "Database basics: relational DBs (PostgreSQL, SQLite), primary keys, foreign keys, indexes",
          "File formats: CSV, JSON, Parquet — tradeoffs",
          "APIs: what they are, how to call a REST API with Python (requests library)",
          "Version control: Git basics — commit, push, pull, branch, merge",
        ],
        ready: [
          "You can call a public REST API, parse the JSON response, and save it to a database",
          "You can explain the difference between a fact table and a dimension table",
          "You can use Git for version control on a solo project without losing work",
          "You can write a Python script that reads from one source and writes to another",
        ],
      },
      {
        level: 2,
        label: "Practitioner",
        tag: "Can do it independently",
        learn: [
          "Cloud basics: AWS S3 / GCP BigQuery / Azure Blob — read/write data",
          "dbt (data build tool): transformations as SQL models, testing, documentation",
          "Data warehousing concepts: star schema, slowly changing dimensions",
          "Environment management: .env files, virtual environments, requirements.txt",
          "Docker basics: containerize a Python script",
          "Scheduling scripts: cron jobs, task scheduling",
        ],
        ready: [
          "You can build an ELT pipeline that pulls from an API, loads to cloud storage, transforms with dbt, and outputs a clean table",
          "You can set up a working dbt project with models, tests, and documentation",
          "You can containerize a data script with Docker so anyone can run it",
          "You can explain the difference between a data warehouse and a data lake",
        ],
      },
      {
        level: 3,
        label: "Applied Scientist",
        tag: "Can design and lead it",
        learn: [
          "Orchestration: Airflow or Prefect — DAGs, dependencies, retries, alerts",
          "Streaming data basics: Kafka or Kinesis concepts, when batch vs. stream",
          "Data quality frameworks: great_expectations or Soda checks in pipelines",
          "CI/CD for data pipelines: GitHub Actions basics",
          "Columnar storage and query optimization for BigQuery/Snowflake/Redshift",
        ],
        ready: [
          "You can build an orchestrated pipeline with dependencies, error handling, and alerting",
          "You can explain when to use streaming vs. batch and architect accordingly",
          "You can implement automated data quality tests that block bad data from flowing downstream",
          "You can optimize a slow BigQuery query by 10x using partitioning and clustering",
        ],
      },
      {
        level: 4,
        label: "Master",
        tag: "End-to-end ownership",
        learn: [
          "Design modern data stack architecture for a company (ingestion → warehouse → BI layer)",
          "Data mesh / data lakehouse concepts",
          "Cost optimization for cloud data infrastructure",
          "Data governance, lineage, and access control",
        ],
        ready: [
          "You can recommend and implement the right data stack for a company of any size",
          "You can onboard a data team onto infrastructure you designed",
          "Engineering and business teams trust your data — it's known to be reliable",
        ],
      },
    ],
  },
  {
    id: "ai",
    icon: "🤖",
    title: "AI / GenAI & LLMs",
    subtitle: "The frontier layer — building with the most powerful tools in tech",
    color: "#B06AD4",
    levels: [
      {
        level: 1,
        label: "Foundation",
        tag: "Can follow along",
        learn: [
          "How LLMs work at a high level: tokens, context windows, temperature",
          "Prompt engineering: clear instructions, role-setting, few-shot examples",
          "Using the Anthropic / OpenAI API: send a message, parse a response",
          "Embeddings: what they are, why similarity search works",
          "LLM limitations: hallucinations, knowledge cutoffs, reasoning failures",
        ],
        ready: [
          "You can call an LLM API from Python and build a simple Q&A tool",
          "You can write a prompt that reliably gets structured JSON output from an LLM",
          "You can explain what a hallucination is and two strategies to reduce it",
          "You can explain embeddings using an analogy a non-technical person would get",
        ],
      },
      {
        level: 2,
        label: "Practitioner",
        tag: "Can do it independently",
        learn: [
          "RAG (Retrieval-Augmented Generation): vector DBs (Chroma, Pinecone), chunking strategies",
          "LangChain or LlamaIndex basics for building LLM workflows",
          "Function calling / tool use in LLM APIs",
          "Evaluation: how to measure LLM output quality (LLM-as-judge, human eval frameworks)",
          "Fine-tuning concepts: when it's worth it vs. just better prompting",
          "Structured outputs and JSON mode",
        ],
        ready: [
          "You can build a working RAG system over a document corpus from scratch",
          "You can use function calling to build an LLM that takes real actions",
          "You can evaluate an LLM pipeline's quality with a reproducible framework",
          "You can decide when RAG is the right solution vs. fine-tuning vs. prompt engineering",
        ],
      },
      {
        level: 3,
        label: "Applied Scientist",
        tag: "Can design and lead it",
        learn: [
          "Agentic AI: multi-step reasoning, tool-calling agents, ReAct pattern",
          "Multi-agent frameworks: CrewAI, AutoGen concepts",
          "Advanced RAG: re-ranking, hybrid search, multi-hop retrieval",
          "Guardrails and safety layers for production AI applications",
          "LLM observability: tracing, logging, latency, cost tracking (LangSmith, etc.)",
          "Multimodal models: vision + text, document processing",
        ],
        ready: [
          "You can build a multi-step AI agent that completes a business workflow end-to-end",
          "You can design the safety and reliability layer for a production LLM application",
          "You can debug an LLM pipeline and identify where it fails using tracing tools",
          "You can architect a RAG system that actually works well, not just technically correct",
        ],
      },
      {
        level: 4,
        label: "Master",
        tag: "End-to-end ownership",
        learn: [
          "Design AI product strategy: when/where AI adds real business value vs. hype",
          "Build production-grade AI applications with cost, latency, and reliability SLAs",
          "Contribute to AI evaluation frameworks at an organizational level",
          "Stay current with frontier model capabilities and apply them strategically",
        ],
        ready: [
          "You can pitch, build, and launch an AI-powered product that solves a real business problem",
          "You can advise a leadership team on AI strategy with concrete ROI framing",
          "Your AI applications are in production, being used, and measured",
        ],
      },
    ],
  },
  {
    id: "software",
    icon: "💻",
    title: "Software Engineering & Deployment",
    subtitle: "The production layer — making your work survive the real world",
    color: "#4AACB8",
    levels: [
      {
        level: 1,
        label: "Foundation",
        tag: "Can follow along",
        learn: [
          "Python: functions, classes, modules, imports, virtual environments (venv/conda)",
          "Git: branches, commits, pull requests, resolving merge conflicts",
          "Command line: navigate directories, run scripts, pipe commands, manage files",
          "Code quality: readable variable names, docstrings, basic linting (pylint/flake8)",
          "Reading and writing JSON, CSV, YAML files",
        ],
        ready: [
          "You can write a Python script that someone else can read and run without asking you questions",
          "You can use Git for a project with branches and pull requests",
          "You can navigate the terminal comfortably for data work",
          "Your code passes a linter with no major errors",
        ],
      },
      {
        level: 2,
        label: "Practitioner",
        tag: "Can do it independently",
        learn: [
          "Unit testing: pytest basics, writing test cases, test coverage",
          "REST APIs: build a simple Flask or FastAPI endpoint",
          "Environment variables and secrets management",
          "Error handling: try/except, logging, meaningful error messages",
          "Package structure: build a reusable Python package",
          "Streamlit: build and share a data app in hours",
        ],
        ready: [
          "You can build a working REST API that returns data from a model or database",
          "You can write unit tests for your own functions and achieve >80% coverage",
          "You can deploy a Streamlit app that someone else can use in a browser",
          "You handle errors gracefully — your scripts don't silently fail",
        ],
      },
      {
        level: 3,
        label: "Applied Scientist",
        tag: "Can design and lead it",
        learn: [
          "Docker: build images, docker-compose for multi-container apps",
          "Cloud deployment: deploy to AWS/GCP/Azure (EC2, Cloud Run, Lambda)",
          "CI/CD: GitHub Actions for automated testing and deployment",
          "Database connections from code: SQLAlchemy, connection pooling",
          "Authentication basics: API keys, OAuth concepts",
          "Next.js or React basics: enough to build data-driven web apps",
        ],
        ready: [
          "You can take a model or analysis and deploy it as a live web application",
          "You can set up CI/CD so that tests run automatically on every code push",
          "You can deploy containerized applications to the cloud",
          "Your deployed apps have proper logging, error tracking, and can be debugged remotely",
        ],
      },
      {
        level: 4,
        label: "Master",
        tag: "End-to-end ownership",
        learn: [
          "System design: design scalable architectures for data products",
          "Performance optimization: profiling, caching, async programming",
          "Security fundamentals for data applications",
          "Infrastructure as code: Terraform basics",
        ],
        ready: [
          "You can architect and deploy an end-to-end data product that's production-ready",
          "A DevOps engineer can review your deployment and not have concerns",
          "Your applications can scale without you manually intervening",
        ],
      },
    ],
  },
  {
    id: "business",
    icon: "🎯",
    title: "Business Strategy & Product Thinking",
    subtitle: "The impact layer — the skill that makes everything else matter",
    color: "#D4954A",
    levels: [
      {
        level: 1,
        label: "Foundation",
        tag: "Can follow along",
        learn: [
          "Business fundamentals: revenue, margin, churn, LTV, CAC — what these mean and how data touches them",
          "Problem framing: translate a vague business question into a specific data question",
          "Stakeholder communication: adapting your message for technical vs. non-technical audiences",
          "Requirements gathering: asking the right clarifying questions before starting work",
          "Understanding the difference between a metric, a KPI, and a goal",
        ],
        ready: [
          "You can reframe 'we need more data' into a specific, answerable question",
          "You can explain LTV:CAC to a data person AND to a sales leader",
          "You can write a one-page summary of an analysis that gets to the point in the first sentence",
          "You can ask 5 clarifying questions before starting any analysis that prevent wasted work",
        ],
      },
      {
        level: 2,
        label: "Practitioner",
        tag: "Can do it independently",
        learn: [
          "Product analytics: funnel analysis, cohort retention, feature adoption",
          "Prioritization frameworks: ICE, RICE, opportunity scoring",
          "Root cause analysis: structured frameworks (5 Whys, Fishbone)",
          "OKRs and metrics trees: connecting strategy to measurement",
          "Building business cases: ROI framing for data projects",
          "Working with cross-functional teams: PM, engineering, marketing, finance",
        ],
        ready: [
          "You can analyze a conversion funnel and identify the highest-leverage drop-off point",
          "You can build a business case for a data project that gets leadership buy-in",
          "You can run a root cause analysis on a metric drop and present findings within 48 hours",
          "You can scope a data project by difficulty, impact, and time — and be right most of the time",
        ],
      },
      {
        level: 3,
        label: "Applied Scientist",
        tag: "Can design and lead it",
        learn: [
          "Strategic analysis: market sizing, competitive benchmarking, scenario modeling",
          "Data product management: define requirements, user stories for data products",
          "Executive communication: board-level storytelling with data",
          "Building analytics culture: documentation, self-serve frameworks, training",
          "Connecting ML/AI capabilities to P&L impact",
        ],
        ready: [
          "You can present a data-driven recommendation to a C-suite and drive a decision",
          "You can define the metrics and measurement framework for a new product launch",
          "You can translate a model's output into dollar impact without hand-waving",
          "Stakeholders come to YOU with business questions before making decisions",
        ],
      },
      {
        level: 4,
        label: "Master",
        tag: "End-to-end ownership",
        learn: [
          "Design the data strategy for an organization: what to measure, build, and invest in",
          "Thought leadership: articulate where AI/data is going and what it means for the business",
          "Build data-literate cultures across organizations",
          "Lead cross-functional initiatives where data is the connective tissue",
        ],
        ready: [
          "You're the person leadership calls when they need to think through a data-driven strategy",
          "You can build an end-to-end solution that creates measurable business value — and prove it",
          "Other analysts learn from how you work, not just what you produce",
        ],
      },
    ],
  },
];

const LEVEL_COLORS = {
  1: { bg: "#1a2332", border: "#2a3d5a", badge: "#2A4A7F", text: "#6BA3D6" },
  2: { bg: "#1a2a1e", border: "#2a4a2e", badge: "#2A6040", text: "#5DB878" },
  3: { bg: "#2a1e2e", border: "#4a2a5a", badge: "#5A2A80", text: "#A87FD4" },
  4: { bg: "#2e1e14", border: "#5a3a1e", badge: "#7A4A10", text: "#D4934A" },
};

const LEVEL_LABELS = ["Foundation", "Practitioner", "Applied Scientist", "Master"];

export default function Roadmap() {
  const [activeDomain, setActiveDomain] = useState("wrangling");
  const [activeLevel, setActiveLevel] = useState(1);
  const [checked, setChecked] = useState({});

  const domain = DOMAINS.find((d) => d.id === activeDomain);
  const levelData = domain?.levels.find((l) => l.level === activeLevel);
  const lc = LEVEL_COLORS[activeLevel];

  const toggleCheck = (key) => {
    setChecked((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const getProgress = (domainId) => {
    const dom = DOMAINS.find((d) => d.id === domainId);
    let total = 0, done = 0;
    dom.levels.forEach((lv) => {
      lv.ready.forEach((_, i) => {
        total++;
        if (checked[`${domainId}-${lv.level}-r${i}`]) done++;
      });
    });
    return total === 0 ? 0 : Math.round((done / total) * 100);
  };

  const overallProgress = () => {
    let total = 0, done = 0;
    DOMAINS.forEach((dom) => {
      dom.levels.forEach((lv) => {
        lv.ready.forEach((_, i) => {
          total++;
          if (checked[`${dom.id}-${lv.level}-r${i}`]) done++;
        });
      });
    });
    return total === 0 ? 0 : Math.round((done / total) * 100);
  };

  const overall = overallProgress();

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0D1117",
      color: "#C9D1D9",
      fontFamily: "'DM Sans', 'Segoe UI', system-ui, sans-serif",
      display: "flex",
      flexDirection: "column",
    }}>
      {/* Header */}
      <div style={{
        background: "linear-gradient(135deg, #0D1117 0%, #161B22 100%)",
        borderBottom: "1px solid #21262D",
        padding: "28px 32px 24px",
      }}>
        <div style={{ maxWidth: 1200, margin: "0 auto" }}>
          <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", flexWrap: "wrap", gap: 16 }}>
            <div>
              <div style={{ fontSize: 11, letterSpacing: "0.15em", color: "#8B949E", textTransform: "uppercase", marginBottom: 6 }}>
                Applied Data Scientist · Master Roadmap
              </div>
              <h1 style={{ margin: 0, fontSize: 28, fontWeight: 700, color: "#F0F6FC", letterSpacing: "-0.5px" }}>
                Data → Insight → Impact
              </h1>
              <p style={{ margin: "6px 0 0", color: "#8B949E", fontSize: 14 }}>
                8 domains · 4 levels each · from raw data to end-to-end business solutions
              </p>
            </div>
            <div style={{ textAlign: "right" }}>
              <div style={{ fontSize: 11, color: "#8B949E", marginBottom: 4, textTransform: "uppercase", letterSpacing: "0.1em" }}>Overall</div>
              <div style={{ fontSize: 36, fontWeight: 800, color: "#F0F6FC", lineHeight: 1 }}>{overall}%</div>
              <div style={{
                width: 120, height: 4, background: "#21262D", borderRadius: 2, marginTop: 8,
              }}>
                <div style={{ width: `${overall}%`, height: "100%", background: "linear-gradient(90deg, #E8A838, #E05C5C)", borderRadius: 2, transition: "width 0.4s" }} />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div style={{ display: "flex", flex: 1, maxWidth: 1200, margin: "0 auto", width: "100%", gap: 0 }}>
        {/* Sidebar */}
        <div style={{
          width: 220,
          flexShrink: 0,
          borderRight: "1px solid #21262D",
          padding: "20px 0",
          position: "sticky",
          top: 0,
          alignSelf: "flex-start",
          maxHeight: "calc(100vh - 120px)",
          overflowY: "auto",
        }}>
          {DOMAINS.map((d) => {
            const prog = getProgress(d.id);
            const active = activeDomain === d.id;
            return (
              <button
                key={d.id}
                onClick={() => setActiveDomain(d.id)}
                style={{
                  width: "100%",
                  display: "flex",
                  alignItems: "center",
                  gap: 10,
                  padding: "10px 16px",
                  background: active ? "#161B22" : "transparent",
                  border: "none",
                  borderLeft: active ? `3px solid ${d.color}` : "3px solid transparent",
                  cursor: "pointer",
                  textAlign: "left",
                  transition: "all 0.15s",
                }}
              >
                <span style={{ fontSize: 18, flexShrink: 0 }}>{d.icon}</span>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{
                    fontSize: 12, fontWeight: active ? 600 : 400,
                    color: active ? "#F0F6FC" : "#8B949E",
                    lineHeight: 1.3,
                    whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis"
                  }}>
                    {d.title}
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: 4, marginTop: 4 }}>
                    <div style={{ flex: 1, height: 2, background: "#21262D", borderRadius: 1 }}>
                      <div style={{ width: `${prog}%`, height: "100%", background: d.color, borderRadius: 1, transition: "width 0.3s" }} />
                    </div>
                    <span style={{ fontSize: 9, color: "#8B949E", flexShrink: 0 }}>{prog}%</span>
                  </div>
                </div>
              </button>
            );
          })}
        </div>

        {/* Main Content */}
        <div style={{ flex: 1, padding: "24px 28px", minWidth: 0 }}>
          {/* Domain Header */}
          <div style={{ marginBottom: 24 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 6 }}>
              <span style={{ fontSize: 28 }}>{domain.icon}</span>
              <div>
                <h2 style={{ margin: 0, fontSize: 20, fontWeight: 700, color: "#F0F6FC" }}>{domain.title}</h2>
                <p style={{ margin: 0, fontSize: 13, color: "#8B949E" }}>{domain.subtitle}</p>
              </div>
            </div>

            {/* Level Tabs */}
            <div style={{ display: "flex", gap: 6, marginTop: 16, flexWrap: "wrap" }}>
              {LEVEL_LABELS.map((label, i) => {
                const lv = i + 1;
                const active = activeLevel === lv;
                const lcolor = LEVEL_COLORS[lv];
                return (
                  <button
                    key={lv}
                    onClick={() => setActiveLevel(lv)}
                    style={{
                      padding: "6px 16px",
                      borderRadius: 20,
                      border: `1px solid ${active ? lcolor.text : "#21262D"}`,
                      background: active ? lcolor.badge : "transparent",
                      color: active ? lcolor.text : "#8B949E",
                      fontSize: 12,
                      fontWeight: active ? 600 : 400,
                      cursor: "pointer",
                      transition: "all 0.15s",
                    }}
                  >
                    L{lv} · {label}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Level Content */}
          {levelData && (
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
              {/* Learn Column */}
              <div style={{
                background: lc.bg,
                border: `1px solid ${lc.border}`,
                borderRadius: 10,
                padding: 20,
              }}>
                <div style={{
                  fontSize: 11, fontWeight: 600, letterSpacing: "0.12em",
                  textTransform: "uppercase", color: lc.text, marginBottom: 14
                }}>
                  📚 What to Learn
                </div>
                <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                  {levelData.learn.map((item, i) => (
                    <div key={i} style={{ display: "flex", gap: 8, alignItems: "flex-start" }}>
                      <span style={{ color: lc.text, fontSize: 14, flexShrink: 0, marginTop: 1 }}>→</span>
                      <span style={{ fontSize: 13, color: "#C9D1D9", lineHeight: 1.5 }}>{item}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Ready Column */}
              <div style={{
                background: "#0D1117",
                border: `1px solid ${lc.border}`,
                borderRadius: 10,
                padding: 20,
              }}>
                <div style={{
                  fontSize: 11, fontWeight: 600, letterSpacing: "0.12em",
                  textTransform: "uppercase", color: lc.text, marginBottom: 6
                }}>
                  ✅ You're Ready When...
                </div>
                <div style={{ fontSize: 11, color: "#8B949E", marginBottom: 14 }}>
                  Check these off as you can do them without help
                </div>
                <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                  {levelData.ready.map((item, i) => {
                    const key = `${activeDomain}-${activeLevel}-r${i}`;
                    const done = !!checked[key];
                    return (
                      <div
                        key={i}
                        onClick={() => toggleCheck(key)}
                        style={{
                          display: "flex", gap: 10, alignItems: "flex-start",
                          cursor: "pointer", padding: "8px 10px", borderRadius: 6,
                          background: done ? `${lc.badge}44` : "transparent",
                          border: `1px solid ${done ? lc.border : "transparent"}`,
                          transition: "all 0.15s",
                        }}
                      >
                        <div style={{
                          width: 18, height: 18, borderRadius: 4, flexShrink: 0, marginTop: 1,
                          border: `2px solid ${done ? lc.text : "#30363D"}`,
                          background: done ? lc.text : "transparent",
                          display: "flex", alignItems: "center", justifyContent: "center",
                          transition: "all 0.15s",
                        }}>
                          {done && <span style={{ fontSize: 11, color: "#0D1117", fontWeight: 800 }}>✓</span>}
                        </div>
                        <span style={{
                          fontSize: 13, lineHeight: 1.5,
                          color: done ? "#8B949E" : "#C9D1D9",
                          textDecoration: done ? "line-through" : "none",
                        }}>{item}</span>
                      </div>
                    );
                  })}
                </div>

                {/* Level Complete Check */}
                {(() => {
                  const allDone = levelData.ready.every((_, i) => checked[`${activeDomain}-${activeLevel}-r${i}`]);
                  if (!allDone) return null;
                  return (
                    <div style={{
                      marginTop: 16, padding: "10px 14px", borderRadius: 8,
                      background: `${lc.badge}66`, border: `1px solid ${lc.text}`,
                      fontSize: 12, color: lc.text, fontWeight: 600, textAlign: "center"
                    }}>
                      🎉 Level {activeLevel} Complete — Move to {LEVEL_LABELS[activeLevel] || "the next domain"}!
                    </div>
                  );
                })()}
              </div>
            </div>
          )}

          {/* All Levels Overview */}
          <div style={{ marginTop: 20 }}>
            <div style={{ fontSize: 11, color: "#8B949E", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 12 }}>
              Domain Progress
            </div>
            <div style={{ display: "flex", gap: 8 }}>
              {domain.levels.map((lv) => {
                const total = lv.ready.length;
                const done = lv.ready.filter((_, i) => checked[`${activeDomain}-${lv.level}-r${i}`]).length;
                const pct = Math.round((done / total) * 100);
                const lcolor = LEVEL_COLORS[lv.level];
                return (
                  <div
                    key={lv.level}
                    onClick={() => setActiveLevel(lv.level)}
                    style={{
                      flex: 1, background: "#161B22", border: `1px solid ${activeLevel === lv.level ? lcolor.text : "#21262D"}`,
                      borderRadius: 8, padding: "12px 14px", cursor: "pointer", transition: "all 0.15s"
                    }}
                  >
                    <div style={{ fontSize: 10, color: "#8B949E", marginBottom: 4 }}>L{lv.level}</div>
                    <div style={{ fontSize: 12, fontWeight: 600, color: lcolor.text, marginBottom: 8 }}>{lv.label}</div>
                    <div style={{ height: 3, background: "#21262D", borderRadius: 2 }}>
                      <div style={{ width: `${pct}%`, height: "100%", background: lcolor.text, borderRadius: 2, transition: "width 0.3s" }} />
                    </div>
                    <div style={{ fontSize: 10, color: "#8B949E", marginTop: 4 }}>{done}/{total} ready</div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      <div style={{
        borderTop: "1px solid #21262D", padding: "12px 32px", textAlign: "center",
        fontSize: 11, color: "#8B949E"
      }}>
        Check off milestones as you hit them · All 4 levels across all 8 domains = Full Applied Data Scientist
      </div>
    </div>
  );
}
