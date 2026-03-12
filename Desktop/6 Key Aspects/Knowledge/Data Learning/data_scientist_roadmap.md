# 🧑‍💻 Data Scientist Master Roadmap

> A complete, level-by-level roadmap across 8 domains to become a full-stack applied data scientist. Check off milestones as you complete them.

---

## ⚙️ Data Wrangling & Analysis

### L1: Foundation

**What to Learn**
- Python basics: variables, loops, functions
- pandas: read CSV, filter, groupby basics
- SQL: SELECT, WHERE, GROUP BY, JOIN, ORDER BY
- Excel: VLOOKUP/XLOOKUP, pivot tables
- Identify and handle nulls (dropna, fillna)

**You're Ready When...**
- [ ] Load a messy CSV and produce a clean summary table without Googling
- [ ] Answer "top 5 products by revenue last quarter" in both Python AND SQL
- [ ] Build a pivot table in Excel from scratch in under 5 minutes
- [ ] Explain what a NULL value is and 3 ways to handle it

---

### L2: Practitioner

**What to Learn**
- pandas: merge/join DataFrames, apply(), pivot_table, melt
- String manipulation, regex basics, datetime arithmetic
- SQL: window functions (ROW_NUMBER, LAG/LEAD), CTEs, subqueries
- Detecting & handling outliers (IQR, z-score)
- Excel: INDEX/MATCH, dynamic arrays, SUMIFS

**You're Ready When...**
- [ ] Join 3+ tables in SQL with window functions for a cohort analysis
- [ ] Take a raw dataset with mixed types and fully clean it in pandas without help
- [ ] Write a reusable Python function that processes a new month of data with one call
- [ ] Explain the difference between a CTE and a subquery and when to use each

---

### L3: Applied Scientist

**What to Learn**
- Build automated data cleaning pipelines
- Data profiling: ydata-profiling, great_expectations
- Advanced pandas: chunking large files, memory optimization, vectorization
- SQLAlchemy for Python-DB integration
- Time series data manipulation: resampling, rolling windows

**You're Ready When...**
- [ ] Design a data pipeline from scratch given a business problem
- [ ] Set up automated data quality checks that alert when data breaks
- [ ] Optimize a slow pandas script by 5-10x using vectorization
- [ ] Ingest data from a REST API, clean it, and load it into a database in one script

---

### L4: Master

**What to Learn**
- Design scalable data models (star schema, data vault)
- Orchestrate pipelines: Airflow/Prefect basics, cron scheduling
- Implement data contracts and SLAs between teams
- Build self-healing pipelines with error handling, retries, logging

**You're Ready When...**
- [ ] Architect the full data layer of a business solution end-to-end
- [ ] Diagnose a broken pipeline, find root cause, add guardrails so it doesn't recur
- [ ] Explain your data model to both a data engineer and a business stakeholder

---

## 📐 Statistics & Mathematics

### L1: Foundation

**What to Learn**
- Descriptive stats: mean, median, mode, variance, std dev
- Distributions: normal, uniform, skewed
- Correlation vs. causation — the most important distinction
- Basic probability: P(A), conditional probability
- Percentiles and quartiles (IQR)

**You're Ready When...**
- [ ] Look at a distribution and describe it accurately (shape, center, spread, outliers)
- [ ] Explain why correlation ≠ causation with a real example
- [ ] Calculate mean, median, std from scratch without a library
- [ ] Explain what a p-value is to a non-technical person

---

### L2: Practitioner

**What to Learn**
- Hypothesis testing: t-test, chi-square, ANOVA
- Confidence intervals and what they actually mean
- A/B testing: sample size, statistical power, significance
- Linear regression: assumptions, coefficients, R²
- Central Limit Theorem and why it matters

**You're Ready When...**
- [ ] Design and evaluate an A/B test end-to-end including choosing sample size upfront
- [ ] Run a linear regression, interpret every output number, and explain assumption violations
- [ ] Decide which statistical test to use given a business question and data type
- [ ] Explain Type I vs Type II error using a business example

---

### L3: Applied Scientist

**What to Learn**
- Multivariate regression, interaction terms
- Logistic regression: log-odds, decision boundaries
- Bootstrap, cross-validation, permutation tests
- Multiple testing correction: Bonferroni, FDR
- Causal inference: DiD, regression discontinuity, IV

**You're Ready When...**
- [ ] Run a causal analysis (not just correlation) to answer "did this intervention work?"
- [ ] Identify and correct for multiple testing problems in an experiment suite
- [ ] Explain when frequentist vs. Bayesian is preferable for a business decision
- [ ] Set up and interpret a logistic regression for a classification business problem

---

### L4: Master

**What to Learn**
- Design experiment platforms for organizations
- Bayesian hierarchical models
- Sensitivity analysis and robustness checks
- Communicate statistical uncertainty to executives

**You're Ready When...**
- [ ] Design the statistics infrastructure for how a company runs experiments
- [ ] Defend your statistical methodology to a skeptical senior data scientist
- [ ] Translate statistical findings into business risk and dollar impact

---

## 🧠 Machine Learning

### L1: Foundation

**What to Learn**
- Supervised vs unsupervised vs reinforcement learning
- Train/validation/test split and why leakage is dangerous
- Scikit-learn workflow: fit, predict, score
- Decision trees: how they split, overfitting, depth control
- Evaluation: accuracy, precision, recall, F1, RMSE, MAE

**You're Ready When...**
- [ ] Build a working classification model in scikit-learn from raw data to predictions
- [ ] Explain why you'd use precision vs. recall depending on business context
- [ ] Identify data leakage in a pipeline and explain why it makes results meaningless
- [ ] Explain the bias-variance tradeoff using a non-technical analogy

---

### L2: Practitioner

**What to Learn**
- Feature engineering: encoding, scaling, feature selection
- Cross-validation: k-fold, stratified k-fold, time-series CV
- Ensemble methods: Random Forest, XGBoost, LightGBM
- Hyperparameter tuning: GridSearchCV, Optuna
- Handling class imbalance: SMOTE, class weights, threshold tuning

**You're Ready When...**
- [ ] Take a business problem, frame it as ML, build a model, beat a baseline
- [ ] Tune an XGBoost model and explain what each hyperparameter does
- [ ] Handle a 95/5 class imbalance dataset and still get a meaningful model
- [ ] Choose the right algorithm for a given dataset size, type, and business goal

---

### L3: Applied Scientist

**What to Learn**
- Model interpretability: SHAP values, LIME, partial dependence plots
- Neural networks: feedforward, PyTorch/Keras basics
- Time series forecasting: ARIMA, Prophet, LSTM
- Recommendation systems: collaborative filtering
- MLflow: experiment tracking, model registry
- Model monitoring: drift detection, performance degradation

**You're Ready When...**
- [ ] Explain any model's prediction to a business stakeholder using SHAP
- [ ] Build a time series forecast for a business metric with confidence intervals
- [ ] Track experiments systematically and reproduce any past result
- [ ] Detect when a deployed model starts degrading and know what to do

---

### L4: Master

**What to Learn**
- Full ML system design: problem framing to monitoring
- Custom loss functions aligned to business outcomes
- Multi-model architectures: stacking, blending
- Cost-sensitive learning: tying decisions to real business value

**You're Ready When...**
- [ ] Scope, build, deploy, and maintain an ML system that improves a business KPI
- [ ] Present the ROI of a model to a CFO (not just the accuracy score)
- [ ] Design the retraining and monitoring strategy for a production ML system

---

## 📊 Visualization & Communication

### L1: Foundation

**What to Learn**
- Chart selection: when to use bar, line, scatter, histogram
- matplotlib/seaborn basics: labels, titles, colors
- Tableau/Power BI: connect data source, build basic charts
- Storytelling rule: one chart = one message
- Color theory: avoid rainbow palettes, use colorblind-safe options

**You're Ready When...**
- [ ] Spot what's wrong with a misleading chart immediately
- [ ] Build a clean, publication-ready chart in Python from scratch
- [ ] Connect a dataset in Tableau and build a basic dashboard in under an hour
- [ ] Explain why a pie chart with 8 slices is almost always wrong

---

### L2: Practitioner

**What to Learn**
- Plotly/Altair for interactive charts
- Dashboard design: layout, hierarchy, progressive disclosure
- Tableau: calculated fields, LOD expressions, dashboard actions
- Data storytelling: hook → tension → resolution narrative
- Executive-level slide design: one insight per slide

**You're Ready When...**
- [ ] Build an interactive dashboard a non-analyst can explore on their own
- [ ] Present a data analysis to a senior leader in 5 minutes and get a decision
- [ ] Take a complex finding and write a one-paragraph summary a CEO would act on
- [ ] Someone can understand the main insight in your dashboard in under 10 seconds

---

### L3: Applied Scientist

**What to Learn**
- Build custom visualization components (D3.js or Plotly Dash)
- Design BI reporting systems for business teams
- Advanced Tableau: performance optimization, embedding
- Metrics frameworks: choosing KPIs, north star metrics
- Communicating uncertainty: confidence intervals in charts

**You're Ready When...**
- [ ] Design the analytics reporting structure for a department or product
- [ ] Build a live Plotly Dash or Streamlit app that a business team uses daily
- [ ] Facilitate a metrics workshop with stakeholders to define what "good" looks like
- [ ] Show uncertainty ranges in your charts without confusing your audience

---

### L4: Master

**What to Learn**
- Design data storytelling culture for an organization
- Build custom data products that democratize analytics access
- Connect visualization strategy to decision-making frameworks

**You're Ready When...**
- [ ] Business leaders actively use dashboards you built to make weekly decisions
- [ ] You can teach others your visualization framework and they improve immediately
- [ ] You can influence the metrics culture of an organization, not just report numbers

---

## 🏗️ Data Engineering & Pipelines

### L1: Foundation

**What to Learn**
- ETL vs. ELT and when each is used
- Database basics: relational DBs, primary keys, indexes
- File formats: CSV, JSON, Parquet — tradeoffs
- APIs: call a REST API with Python (requests)
- Git basics — commit, push, pull, branch, merge

**You're Ready When...**
- [ ] Call a public REST API, parse JSON, and save it to a database
- [ ] Explain the difference between a fact table and a dimension table
- [ ] Use Git for version control on a solo project without losing work
- [ ] Write a Python script that reads from one source and writes to another

---

### L2: Practitioner

**What to Learn**
- Cloud basics: AWS S3 / GCP BigQuery / Azure Blob
- dbt: transformations as SQL models, testing, documentation
- Data warehousing concepts: star schema, slowly changing dimensions
- Docker basics: containerize a Python script
- Scheduling scripts: cron jobs, task scheduling

**You're Ready When...**
- [ ] Build an ELT pipeline: API → cloud storage → dbt → clean table
- [ ] Set up a working dbt project with models, tests, and documentation
- [ ] Containerize a data script with Docker so anyone can run it
- [ ] Explain the difference between a data warehouse and a data lake

---

### L3: Applied Scientist

**What to Learn**
- Orchestration: Airflow or Prefect — DAGs, dependencies, retries
- Streaming data basics: Kafka or Kinesis concepts
- Data quality frameworks: great_expectations in pipelines
- CI/CD for data pipelines: GitHub Actions basics
- Columnar storage and query optimization for BigQuery/Snowflake

**You're Ready When...**
- [ ] Build an orchestrated pipeline with dependencies, error handling, and alerting
- [ ] Explain when to use streaming vs. batch and architect accordingly
- [ ] Implement automated data quality tests that block bad data downstream
- [ ] Optimize a slow BigQuery query by 10x using partitioning and clustering

---

### L4: Master

**What to Learn**
- Design modern data stack architecture for a company
- Data mesh / data lakehouse concepts
- Cost optimization for cloud data infrastructure
- Data governance, lineage, and access control

**You're Ready When...**
- [ ] Recommend and implement the right data stack for a company of any size
- [ ] Onboard a data team onto infrastructure you designed
- [ ] Engineering and business teams trust your data — it's known to be reliable

---

## 🤖 AI / GenAI & LLMs

### L1: Foundation

**What to Learn**
- How LLMs work: tokens, context windows, temperature
- Prompt engineering: clear instructions, role-setting, few-shot examples
- Using the Anthropic/OpenAI API: send a message, parse a response
- Embeddings: what they are, why similarity search works
- LLM limitations: hallucinations, knowledge cutoffs, reasoning failures

**You're Ready When...**
- [ ] Call an LLM API from Python and build a simple Q&A tool
- [ ] Write a prompt that reliably gets structured JSON output from an LLM
- [ ] Explain what a hallucination is and two strategies to reduce it
- [ ] Explain embeddings using an analogy a non-technical person would get

---

### L2: Practitioner

**What to Learn**
- RAG: vector DBs (Chroma, Pinecone), chunking strategies
- LangChain or LlamaIndex basics for LLM workflows
- Function calling / tool use in LLM APIs
- Evaluation: LLM-as-judge, human eval frameworks
- Fine-tuning concepts: when it's worth it vs. better prompting

**You're Ready When...**
- [ ] Build a working RAG system over a document corpus from scratch
- [ ] Use function calling to build an LLM that takes real actions
- [ ] Evaluate an LLM pipeline's quality with a reproducible framework
- [ ] Decide when RAG is the right solution vs. fine-tuning vs. prompt engineering

---

### L3: Applied Scientist

**What to Learn**
- Agentic AI: multi-step reasoning, tool-calling agents, ReAct pattern
- Multi-agent frameworks: CrewAI, AutoGen concepts
- Advanced RAG: re-ranking, hybrid search, multi-hop retrieval
- Guardrails and safety layers for production AI applications
- LLM observability: tracing, logging, latency, cost tracking

**You're Ready When...**
- [ ] Build a multi-step AI agent that completes a business workflow end-to-end
- [ ] Design the safety and reliability layer for a production LLM application
- [ ] Debug an LLM pipeline and identify where it fails using tracing tools
- [ ] Architect a RAG system that actually works well, not just technically correct

---

### L4: Master

**What to Learn**
- Design AI product strategy: where AI adds real business value
- Build production-grade AI applications with cost, latency, and reliability SLAs
- Contribute to AI evaluation frameworks at an organizational level
- Stay current with frontier model capabilities and apply them strategically

**You're Ready When...**
- [ ] Pitch, build, and launch an AI-powered product that solves a real business problem
- [ ] Advise a leadership team on AI strategy with concrete ROI framing
- [ ] Your AI applications are in production, being used, and measured

---

## 💻 Software Engineering & Deployment

### L1: Foundation

**What to Learn**
- Python: functions, classes, modules, virtual environments
- Git: branches, commits, pull requests, merge conflicts
- Command line: navigate, run scripts, pipe commands
- Code quality: readable names, docstrings, linting (pylint/flake8)
- Reading and writing JSON, CSV, YAML files

**You're Ready When...**
- [ ] Write a Python script someone else can read and run without asking you questions
- [ ] Use Git for a project with branches and pull requests
- [ ] Navigate the terminal comfortably for data work
- [ ] Your code passes a linter with no major errors

---

### L2: Practitioner

**What to Learn**
- Unit testing: pytest basics, writing test cases, test coverage
- REST APIs: build a simple Flask or FastAPI endpoint
- Environment variables and secrets management
- Error handling: try/except, logging, meaningful error messages
- Streamlit: build and share a data app in hours

**You're Ready When...**
- [ ] Build a working REST API that returns data from a model or database
- [ ] Write unit tests for your own functions and achieve >80% coverage
- [ ] Deploy a Streamlit app that someone else can use in a browser
- [ ] Handle errors gracefully — your scripts don't silently fail

---

### L3: Applied Scientist

**What to Learn**
- Docker: build images, docker-compose for multi-container apps
- Cloud deployment: AWS/GCP/Azure (EC2, Cloud Run, Lambda)
- CI/CD: GitHub Actions for automated testing and deployment
- Database connections from code: SQLAlchemy, connection pooling
- Next.js or React basics: enough to build data-driven web apps

**You're Ready When...**
- [ ] Take a model or analysis and deploy it as a live web application
- [ ] Set up CI/CD so tests run automatically on every code push
- [ ] Deploy containerized applications to the cloud
- [ ] Your deployed apps have proper logging, error tracking, and can be debugged remotely

---

### L4: Master

**What to Learn**
- System design: design scalable architectures for data products
- Performance optimization: profiling, caching, async programming
- Security fundamentals for data applications
- Infrastructure as code: Terraform basics

**You're Ready When...**
- [ ] Architect and deploy an end-to-end data product that's production-ready
- [ ] A DevOps engineer can review your deployment and not have concerns
- [ ] Your applications can scale without you manually intervening

---

## 🎯 Business Strategy & Product Thinking

### L1: Foundation

**What to Learn**
- Business fundamentals: revenue, margin, churn, LTV, CAC
- Problem framing: translate vague question into specific data question
- Stakeholder communication: technical vs. non-technical audiences
- Requirements gathering: asking the right clarifying questions
- Difference between a metric, a KPI, and a goal

**You're Ready When...**
- [ ] Reframe "we need more data" into a specific, answerable question
- [ ] Explain LTV:CAC to a data person AND to a sales leader
- [ ] Write a one-page summary of an analysis that gets to the point in sentence one
- [ ] Ask 5 clarifying questions before starting any analysis to prevent wasted work

---

### L2: Practitioner

**What to Learn**
- Product analytics: funnel analysis, cohort retention, feature adoption
- Prioritization frameworks: ICE, RICE, opportunity scoring
- Root cause analysis: 5 Whys, Fishbone
- OKRs and metrics trees: connecting strategy to measurement
- Building business cases: ROI framing for data projects

**You're Ready When...**
- [ ] Analyze a conversion funnel and identify the highest-leverage drop-off point
- [ ] Build a business case for a data project that gets leadership buy-in
- [ ] Run a root cause analysis on a metric drop and present findings within 48 hours
- [ ] Scope a data project by difficulty, impact, and time — and be right most of the time

---

### L3: Applied Scientist

**What to Learn**
- Strategic analysis: market sizing, competitive benchmarking
- Data product management: requirements, user stories
- Executive communication: board-level storytelling with data
- Connecting ML/AI capabilities to P&L impact

**You're Ready When...**
- [ ] Present a data-driven recommendation to C-suite and drive a decision
- [ ] Define the metrics and measurement framework for a new product launch
- [ ] Translate a model's output into dollar impact without hand-waving
- [ ] Stakeholders come to YOU with business questions before making decisions

---

### L4: Master

**What to Learn**
- Design the data strategy for an organization
- Thought leadership: articulate where AI/data is going
- Build data-literate cultures across organizations
- Lead cross-functional initiatives where data is the connective tissue

**You're Ready When...**
- [ ] You're the person leadership calls when they need data-driven strategy
- [ ] Build an end-to-end solution that creates measurable business value — and prove it
- [ ] Other analysts learn from how you work, not just what you produce
