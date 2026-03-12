import { useState } from "react";

const DATASETS = [
  {
    id: "retail",
    file: "retail_sales_dirty.csv",
    emoji: "🛒",
    name: "Retail Sales",
    domain: "Wrangling L1–L2",
    domainColor: "#E8A838",
    rows: "1,230",
    cols: 11,
    nullRate: "2.8%",
    description: "Regional retail orders with products, reps, pricing, and ratings.",
    target: "Clean and aggregate: revenue by region and product category",
    issues: [
      { type: "Mixed Date Formats", severity: "high", detail: "5 different formats: YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY, 'January 01, 2023', DD/MM/YY" },
      { type: "Currency Symbols in Numeric Col", severity: "high", detail: "unit_price stored as '$14.99', 'USD 14.99', ' 14.99 ', or None" },
      { type: "Inconsistent Category Names", severity: "medium", detail: "'Electronics', 'electronics', 'ELECTRONICS' — same value, 3 forms" },
      { type: "Negative Quantities", severity: "medium", detail: "~3% of rows have negative quantity values (data entry error, not returns)" },
      { type: "Impossible Discount Values", severity: "medium", detail: "discount_pct values like 150, 175 — impossible for a percentage" },
      { type: "Duplicate Rows", severity: "high", detail: "~30 exact duplicate order rows injected" },
      { type: "Trailing Whitespace", severity: "low", detail: "region and sales_rep columns have leading/trailing spaces ('south ', ' East')" },
      { type: "Out-of-Range Ratings", severity: "low", detail: "customer_rating includes 99 and -1 alongside valid 1–5 values" },
    ],
    cleaning: [
      "pd.to_datetime(df['order_date'], infer_datetime_format=True)",
      "df['unit_price'] = df['unit_price'].str.replace(r'[$,USD\\s]','',regex=True).astype(float)",
      "df['product_name'] = df['product_name'].str.strip().str.title()",
      "df = df[df['quantity'] > 0]  # drop negative quantities",
      "df = df[df['discount_pct'].between(0, 100)]  # valid range",
      "df = df.drop_duplicates()",
      "df = df[df['customer_rating'].between(1, 5)]  # valid ratings only",
    ],
  },
  {
    id: "employee",
    file: "employee_hr_dirty.csv",
    emoji: "👥",
    name: "Employee HR",
    domain: "Statistics L1–L2",
    domainColor: "#5B8FD4",
    rows: "820",
    cols: 13,
    nullRate: "5.5%",
    description: "Company HR records with salaries, departments, titles, and performance.",
    target: "Distribution analysis: salary by dept, performance by tenure",
    issues: [
      { type: "Outlier Salaries", severity: "high", detail: "Values like $999,999, $1,200,000, $0, -$50,000, and $1.50 injected as outliers" },
      { type: "Mixed Types in Age Column", severity: "high", detail: "age stored as float (22.0) in some rows, string ('22') in others" },
      { type: "Future Date of Birth", severity: "medium", detail: "~4% of date_of_birth values are in 2026–2031 (impossible)" },
      { type: "Inconsistent Dept Names", severity: "high", detail: "'Engineering', 'engineering', 'Eng', 'ENG' — 4+ variants per department" },
      { type: "Inconsistent Employment Type", severity: "medium", detail: "'Full-Time', 'full-time', 'FT', 'Full Time', 'CONTRACTOR' — same concept, many forms" },
      { type: "Negative Tenure", severity: "medium", detail: "years_tenure can be negative (-3) for recently hired employees (calculation error)" },
      { type: "Mixed Phone Formats", severity: "low", detail: "(555) 123-4567 vs 5551234567 vs +1-555-123-4567 vs None" },
      { type: "Duplicate Rows", severity: "medium", detail: "~20 duplicate employee records injected" },
    ],
    cleaning: [
      "df['age'] = pd.to_numeric(df['age'], errors='coerce')",
      "df['dob'] = pd.to_datetime(df['date_of_birth'], errors='coerce')\ndf = df[df['dob'] < pd.Timestamp.today()]",
      "df['salary_usd'] = df['salary_usd'].clip(lower=20000, upper=500000)",
      "dept_map = {'engineering':'Engineering','eng':'Engineering','ENG':'Engineering',...}\ndf['department'] = df['department'].str.strip().str.title().map(dept_map)",
      "df['years_tenure'] = df['years_tenure'].clip(lower=0)",
      "df = df.drop_duplicates(subset=['employee_id'])",
    ],
  },
  {
    id: "ecommerce",
    file: "ecommerce_orders_dirty.csv",
    emoji: "📦",
    name: "E-Commerce Orders",
    domain: "Wrangling L2 / ML L1",
    domainColor: "#7C6FCD",
    rows: "2,050",
    cols: 13,
    nullRate: "4.1%",
    description: "Online order data with multi-currency values, boolean flags, and tag arrays.",
    target: "Build a clean orders table: standardize currency, parse tags, normalize booleans",
    issues: [
      { type: "Multi-Currency Values", severity: "high", detail: "order_value stored as '$49.99', '€49.99', '£49.99', '49.99' — need FX or flag" },
      { type: "Shipping Cost as String", severity: "high", detail: "'N/A', 'FREE', 'free', 'NULL', '' — all mean $0 but stored as non-numeric" },
      { type: "Boolean as 6 Different Types", severity: "high", detail: "is_returning_customer: True/False, 1/0, 'Y'/'N', 'Yes'/'No', 'TRUE'/'FALSE', None" },
      { type: "Product Tags as Mixed Arrays", severity: "medium", detail: "['electronics','home'] vs 'electronics|home' vs 'electronics,home' — 3 formats" },
      { type: "Inconsistent Country Codes", severity: "medium", detail: "'US','USA','United States','us','U.S.' — need ISO standardization" },
      { type: "Mixed Date Formats", severity: "medium", detail: "4 date format variants across order_date column" },
      { type: "Fractional Item Counts", severity: "low", detail: "num_items stored as 0.3, 0.7 in ~4% of rows (should be integers)" },
      { type: "Trailing Spaces in Promo Codes", severity: "low", detail: "'SAVE10 ' vs 'SAVE10' — same code, but string match fails" },
    ],
    cleaning: [
      "df['currency'] = df['order_value'].str.extract(r'([£€$])')\ndf['order_value'] = df['order_value'].str.replace(r'[£€$]','',regex=True).astype(float)",
      "df['shipping_cost'] = df['shipping_cost'].replace(['N/A','FREE','free','NULL','','None'],0).astype(float)",
      "bool_map = {True:1,False:0,1:1,0:0,'Y':1,'N':0,'Yes':1,'No':0,'TRUE':1,'FALSE':0,'yes':1,'no':0,'1':1,'0':0}\ndf['is_returning'] = df['is_returning_customer'].map(bool_map)",
      "df['tags_list'] = df['product_tags'].str.replace(r\"[\\[\\]']\", '', regex=True).str.replace('|',',').str.split(',')",
      "df['num_items'] = df['num_items'].round().astype('Int64')",
      "df['promo_code'] = df['promo_code'].str.strip().str.upper().replace({'N/A':'','':None})",
    ],
  },
  {
    id: "patient",
    file: "patient_health_dirty.csv",
    emoji: "🏥",
    name: "Patient Health Records",
    domain: "Statistics L2–L3 / ML L1–L2",
    domainColor: "#E05C5C",
    rows: "1,525",
    cols: 14,
    nullRate: "7.3%",
    description: "Clinical patient data with vitals, diagnoses, and risk factors.",
    target: "Clean physiological data for predictive modeling (readmission prediction)",
    issues: [
      { type: "Impossible Physiological Values", severity: "high", detail: "age=150, age=-5, BMI=999, BMI=0, glucose=-1 — biologically impossible" },
      { type: "Mixed Height Units", severity: "high", detail: "'175.0 cm', '68.9 in', '175.0' — all same patient height, 3 representations" },
      { type: "Blood Pressure as Combined String", severity: "high", detail: "'120/80', '120 / 80', '120' (systolic only), None, 'normal' — needs splitting" },
      { type: "Gender Stored 8+ Ways", severity: "medium", detail: "'Male','male','M','m','MALE','Female','female','F','f','FEMALE','Non-binary','NB'" },
      { type: "Condition Name Inconsistencies", severity: "medium", detail: "'Hypertension','hypertension','HTN' — same condition, 3 names" },
      { type: "Historical Visit Year Errors", severity: "medium", detail: "~4% of visit_year values are 1900–1910 (data entry error — should be 2018–2024)" },
      { type: "Boolean-ish Smoker Column", severity: "low", detail: "'Yes','No','Y','N','1','0',True,False,None — 9 representations of a binary flag" },
      { type: "Missing Diagnosis Codes", severity: "medium", detail: "~20% of rows have null diagnosis_code despite having a condition listed" },
    ],
    cleaning: [
      "df = df[(df['age']>=0) & (df['age']<=120)]\ndf = df[(df['bmi']>=10) & (df['bmi']<=70)]",
      "# Normalize height to cm\ndef parse_height(h):\n    if 'in' in str(h): return float(str(h).replace(' in',''))*2.54\n    return float(str(h).replace(' cm',''))\ndf['height_cm'] = df['height'].apply(parse_height)",
      "df[['systolic','diastolic']] = df['blood_pressure'].str.extract(r'(\\d+)\\s*/\\s*(\\d+)').astype(float)",
      "gender_map = {'male':'Male','m':'Male','MALE':'Male','female':'Female','f':'Female','F':'Female'}\ndf['gender'] = df['gender'].str.strip().map(lambda x: gender_map.get(str(x).lower(), x))",
      "df = df[df['visit_year']>=2000]  # filter historical errors",
    ],
  },
  {
    id: "marketing",
    file: "marketing_campaigns_dirty.csv",
    emoji: "📣",
    name: "Marketing Campaigns",
    domain: "Business L2–L3",
    domainColor: "#3BAE7E",
    rows: "915",
    cols: 15,
    nullRate: "6.0%",
    description: "Digital marketing campaign performance across channels with spend, reach, and ROI.",
    target: "Channel performance analysis: true ROI by channel, fixing spend and CTR formats",
    issues: [
      { type: "Spend with Comma Thousands", severity: "high", detail: "'$1,250.00', '$1,250', '1,250.00', '1250.0' — commas break float conversion" },
      { type: "CTR as Both Percent and Decimal", severity: "high", detail: "'2.5%' vs '0.025' — same value, but 100x difference if parsed blindly" },
      { type: "Start Date After End Date", severity: "high", detail: "~6% of campaigns have start_date > end_date (rows were date-swapped)" },
      { type: "Channel Name Chaos", severity: "high", detail: "30+ variants: 'Facebook','facebook','FB','fb','Meta','meta' — for 6 actual channels" },
      { type: "Zero Impressions", severity: "medium", detail: "~4% of rows have impressions=0, making CTR and engagement metrics undefined/infinite" },
      { type: "Negative Click Counts", severity: "medium", detail: "~4% of rows have negative clicks — not possible, likely sign error" },
      { type: "Mixed Date Formats", severity: "medium", detail: "start_date and end_date use different formats across rows: YYYY-MM-DD, MM/DD/YYYY, DD-Mon-YYYY" },
      { type: "Extreme Negative ROI", severity: "low", detail: "roi_pct values as low as -450% — statistical outliers to investigate" },
    ],
    cleaning: [
      "df['spend'] = df['budget_usd'].str.replace(r'[$,]','',regex=True).astype(float)",
      "# Normalize CTR to decimal\ndef norm_ctr(x):\n    if x and '%' in str(x): return float(str(x).replace('%',''))/100\n    return float(x) if x else None\ndf['ctr_decimal'] = df['ctr'].apply(norm_ctr)",
      "df['start'] = pd.to_datetime(df['start_date'],infer_datetime_format=True)\ndf['end']   = pd.to_datetime(df['end_date'],  infer_datetime_format=True)\ndf = df[df['start'] <= df['end']]  # drop impossible date pairs",
      "channel_map = {'facebook':'Facebook','fb':'Facebook','meta':'Facebook',\n               'google':'Google','google ads':'Google',\n               'instagram':'Instagram','ig':'Instagram'}\ndf['channel_clean'] = df['channel'].str.lower().str.strip().map(channel_map)",
      "df = df[df['impressions'] > 0]\ndf = df[df['clicks'] >= 0]",
    ],
  },
  {
    id: "realestate",
    file: "real_estate_listings_dirty.csv",
    emoji: "🏠",
    name: "Real Estate Listings",
    domain: "ML L2–L3",
    domainColor: "#B06AD4",
    rows: "1,840",
    cols: 18,
    nullRate: "8.8%",
    description: "Property listings with sale prices, features, and market data.",
    target: "Regression target: predict sale_price from cleaned features",
    issues: [
      { type: "Price with K Suffix", severity: "high", detail: "'$450,000', '$450K', '$450k', '450000' — K/k suffix means ×1000" },
      { type: "Sqft in Mixed Formats", severity: "high", detail: "'1,450 sq ft', '1450 sqft', '1450', '1450 SF', None — 5 representations" },
      { type: "Lot Size in Mixed Units", severity: "high", detail: "'0.25 acres', '10,890 sq ft', '0.25' — need unit detection and conversion to acres" },
      { type: "Garage as Boolean AND Integer", severity: "medium", detail: "'Y','Yes','TRUE' vs 'N','No' vs 0,1,2,3 (# of cars) vs None" },
      { type: "Future Year Built", severity: "medium", detail: "year_built values of 2030, 2045 — buildings not yet constructed" },
      { type: "Inconsistent City Names", severity: "medium", detail: "'San Jose','san jose','SAN JOSE','San José' — accents and case variations" },
      { type: "Short Zip Codes", severity: "low", detail: "~5% of zip_codes are 4-digit (missing leading zero: '9101' should be '09101')" },
      { type: "Negative Days on Market", severity: "low", detail: "~4% of rows have negative days_on_market values" },
    ],
    cleaning: [
      "def parse_price(p):\n    if p is None: return None\n    p = str(p).replace('$','').replace(',','').strip()\n    if p.upper().endswith('K'): return float(p[:-1])*1000\n    return float(p)\ndf['price'] = df['sale_price'].apply(parse_price)",
      "df['sqft_num'] = df['sqft'].str.extract(r'([\\d,]+)').replace(',','',regex=True).astype(float)",
      "def parse_lot(l):\n    if l is None: return None\n    if 'sq ft' in str(l): return float(str(l).replace('sq ft','').replace(',','').strip())/43560\n    return float(str(l).replace(' acres','').strip())\ndf['lot_acres'] = df['lot_size'].apply(parse_lot)",
      "def parse_garage(g):\n    if g in ['Y','Yes','yes','TRUE','True',1,'1']: return 1\n    if g in ['N','No','no','FALSE','False',0,'0']: return 0\n    if isinstance(g,(int,float)) and g>1: return int(g)\n    return None\ndf['garage_spaces'] = df['garage'].apply(parse_garage)",
      "df = df[df['year_built'] <= 2024]\ndf = df[df['days_on_market'] >= 0]\ndf['zip_code'] = df['zip_code'].astype(str).str.zfill(5)",
    ],
  },
  {
    id: "student",
    file: "student_performance_dirty.csv",
    emoji: "🎓",
    name: "Student Performance",
    domain: "Statistics L1 / ML L1",
    domainColor: "#4AACB8",
    rows: "1,020",
    cols: 14,
    nullRate: "15.9%",
    description: "Academic performance dataset with grades, attendance, and demographics.",
    target: "Predict pass/fail from cleaned features; analyze grade distributions",
    issues: [
      { type: "Grade as Letter OR Number OR Percent", severity: "high", detail: "'93', 'A', '93%', None — same concept, 4 representations needing normalization to 0–100" },
      { type: "Attendance as Decimal vs Percent", severity: "high", detail: "'85.0%' vs '0.85' — 100x difference if parsed without checking" },
      { type: "Age vs Birth Year Confusion", severity: "high", detail: "age column sometimes contains actual age (20) and sometimes birth year (2004)" },
      { type: "Pass/Fail as 5 Types", severity: "medium", detail: "'Pass','Fail','P','F',1,0,'Yes','No',None — 10 variants of a binary label" },
      { type: "Phantom Empty Column", severity: "medium", detail: "A column named ' ' (a single space) exists with all-null values" },
      { type: "Major Name Inconsistencies", severity: "medium", detail: "'Computer Science','computer science','CS','comp sci' — 4 variants" },
      { type: "Semester Format Variations", severity: "low", detail: "'Fall 2022','Fall2022','fall 2022','F22' — 4 ways to say the same semester" },
      { type: "Over-submitted Assignments", severity: "low", detail: "assignments_submitted stored as float (12.7, 14.3) in some rows — should be integer" },
    ],
    cleaning: [
      "letter_map={'A+':98,'A':93,'A-':90,'B+':87,'B':83,'B-':80,'C+':77,'C':73,'C-':70,'D+':67,'D':63,'F':55}\ndef parse_grade(g):\n    if g in letter_map: return letter_map[g]\n    g = str(g).replace('%','').strip()\n    return float(g) if g else None\ndf['score'] = df['final_score'].apply(parse_grade)",
      "def parse_attend(a):\n    a = str(a)\n    if '%' in a: return float(a.replace('%',''))/100\n    v = float(a)\n    return v/100 if v>1 else v\ndf['attendance'] = df['attendance_rate'].apply(parse_attend)",
      "# Age vs birth year fix\ndf['age_clean'] = df['age'].apply(lambda x: 2024-int(x) if x and int(x)>100 else x)",
      "bool_map={'Pass':1,'Fail':0,'P':1,'F':0,'1':1,'0':0,'Yes':1,'No':0,1:1,0:0}\ndf['passed_clean'] = df['passed'].map(bool_map)",
      "df = df.drop(columns=[' '])  # drop phantom column\ndf['assignments_submitted'] = df['assignments_submitted'].round().astype('Int64')",
    ],
  },
  {
    id: "saas",
    file: "saas_subscriptions_dirty.csv",
    emoji: "💼",
    name: "SaaS Subscriptions",
    domain: "Business L2–L3 / ML L2",
    domainColor: "#D4954A",
    rows: "1,635",
    cols: 16,
    nullRate: "9.8%",
    description: "B2B SaaS customer data with MRR, usage, churn labels, and contract details.",
    target: "Churn prediction: clean all features and build churn = 1/0 label",
    issues: [
      { type: "MRR with Currency and K Suffix", severity: "high", detail: "'$499.00', '$0.50K', '$499', '499.0' — K suffix and symbols in numeric column" },
      { type: "Usage Events as String with Units", severity: "high", detail: "'12,500 events', '12500', '12.5K' — 3 representations needing numeric extraction" },
      { type: "Churn Date in the Future", severity: "high", detail: "~5% of churn_dates are in 2026–2027 — impossible if analysis date is 2024" },
      { type: "Churned Column as 6 Types", severity: "high", detail: "1/0, 'Yes'/'No', 'TRUE'/'FALSE', 'churned', None — binary label in 6 forms" },
      { type: "Plan Names Wildly Inconsistent", severity: "medium", detail: "'Professional','professional','Pro','PRO','pro','Prof' — 6 variants for one plan" },
      { type: "Negative Account Age", severity: "medium", detail: "~5% of account_age_days are negative — impossible, likely calculation error" },
      { type: "NPS Score Out of Range", severity: "medium", detail: "nps_score includes -5, 15, 100 — valid NPS is 0–10" },
      { type: "Inconsistent Region Names", severity: "low", detail: "'NA','North America','US','Americas','EMEA','Europe','EU','emea','APAC','apac'" },
    ],
    cleaning: [
      "def parse_mrr(m):\n    if m is None: return None\n    m = str(m).replace('$','').replace(',','').strip()\n    if m.upper().endswith('K'): return float(m[:-1])*1000\n    return float(m)\ndf['mrr'] = df['mrr_usd'].apply(parse_mrr)",
      "def parse_usage(u):\n    if u is None: return None\n    u = str(u).replace(',','').replace(' events','').strip()\n    if u.upper().endswith('K'): return float(u[:-1])*1000\n    return float(u)\ndf['usage_num'] = df['usage_events'].apply(parse_usage)",
      "# Flag impossible churn dates\nanalysis_date = pd.Timestamp('2024-06-01')\ndf.loc[pd.to_datetime(df['churn_date'],errors='coerce') > analysis_date, 'churn_date'] = None",
      "churn_map={1:1,0:0,'Yes':1,'No':0,'TRUE':1,'FALSE':0,'churned':1,'1':1,'0':0}\ndf['churned_clean'] = df['churned'].map(churn_map)",
      "plan_map={'starter':'Starter','STARTER':'Starter','starter plan':'Starter','start':'Starter',\n          'professional':'Pro','pro':'Pro','PRO':'Pro','prof':'Pro',\n          'enterprise':'Enterprise','ent':'Enterprise','ENT':'Enterprise'}\ndf['plan_clean'] = df['plan'].str.strip().str.lower().map(plan_map)",
      "df = df[df['account_age_days'] >= 0]\ndf = df[df['nps_score'].between(0,10)]",
    ],
  },
];

const SEVERITY_COLORS = {
  high:   { bg: "#2e0d0d", text: "#E05C5C", border: "#5a1a1a" },
  medium: { bg: "#2e2000", text: "#E8A838", border: "#5a3a00" },
  low:    { bg: "#0d1e2e", text: "#5B8FD4", border: "#1a3a5a" },
};

export default function DirtyDatasetGuide() {
  const [activeId, setActiveId] = useState("retail");
  const [tab, setTab] = useState("issues"); // issues | cleaning
  const [copied, setCopied] = useState(null);

  const ds = DATASETS.find(d => d.id === activeId);

  const copy = (text, key) => {
    navigator.clipboard?.writeText(text).then(() => {
      setCopied(key);
      setTimeout(() => setCopied(null), 1500);
    });
  };

  return (
    <div style={{ minHeight:"100vh", background:"#0D1117", color:"#C9D1D9",
      fontFamily:"'DM Mono','Fira Code','Courier New',monospace", display:"flex", flexDirection:"column" }}>

      {/* Header */}
      <div style={{ background:"#0D1117", borderBottom:"1px solid #21262D", padding:"20px 24px" }}>
        <div style={{ maxWidth:1100, margin:"0 auto" }}>
          <div style={{ fontSize:10, letterSpacing:"0.2em", color:"#8B949E", textTransform:"uppercase", marginBottom:4 }}>
            Synthetic Dirty Dataset Library
          </div>
          <h1 style={{ margin:0, fontSize:20, fontWeight:700, color:"#F0F6FC",
            fontFamily:"'DM Sans',system-ui", letterSpacing:"-0.3px" }}>
            8 Dirty Datasets · Real Data Quality Problems · Python Cleaning Solutions
          </h1>
          <p style={{ margin:"6px 0 0", fontSize:12, color:"#8B949E", fontFamily:"'DM Sans',system-ui" }}>
            Every dataset is synthetic &amp; original · intentionally messy · maps to your roadmap levels
          </p>
        </div>
      </div>

      <div style={{ display:"flex", flex:1, maxWidth:1100, margin:"0 auto", width:"100%" }}>
        {/* Sidebar */}
        <div style={{ width:210, flexShrink:0, borderRight:"1px solid #21262D", padding:"16px 0",
          position:"sticky", top:0, alignSelf:"flex-start", maxHeight:"calc(100vh - 90px)", overflowY:"auto" }}>
          {DATASETS.map(d => {
            const active = activeId === d.id;
            return (
              <button key={d.id} onClick={() => { setActiveId(d.id); setTab("issues"); }}
                style={{ width:"100%", display:"flex", alignItems:"center", gap:10, padding:"10px 14px",
                  background:active?"#161B22":"transparent", border:"none",
                  borderLeft:active?`3px solid ${d.domainColor}`:"3px solid transparent",
                  cursor:"pointer", textAlign:"left", transition:"all 0.15s" }}>
                <span style={{ fontSize:18, flexShrink:0 }}>{d.emoji}</span>
                <div style={{ flex:1, minWidth:0 }}>
                  <div style={{ fontSize:11, fontWeight:active?600:400, color:active?"#F0F6FC":"#8B949E",
                    whiteSpace:"nowrap", overflow:"hidden", textOverflow:"ellipsis" }}>{d.name}</div>
                  <div style={{ fontSize:9, color:d.domainColor, marginTop:2 }}>{d.domain}</div>
                  <div style={{ fontSize:9, color:"#8B949E", marginTop:1 }}>{d.rows} rows · {d.nullRate} null</div>
                </div>
              </button>
            );
          })}
        </div>

        {/* Main */}
        <div style={{ flex:1, padding:"20px 24px", minWidth:0 }}>
          {ds && (
            <>
              {/* Dataset header */}
              <div style={{ marginBottom:20 }}>
                <div style={{ display:"flex", alignItems:"center", gap:12, marginBottom:6 }}>
                  <span style={{ fontSize:28 }}>{ds.emoji}</span>
                  <div>
                    <h2 style={{ margin:0, fontSize:18, fontWeight:700, color:"#F0F6FC",
                      fontFamily:"'DM Sans',system-ui" }}>{ds.name}</h2>
                    <p style={{ margin:0, fontSize:12, color:"#8B949E", fontFamily:"'DM Sans',system-ui" }}>{ds.description}</p>
                  </div>
                </div>

                {/* Stats row */}
                <div style={{ display:"flex", gap:8, flexWrap:"wrap", marginBottom:12 }}>
                  {[
                    { label:"File", val:ds.file },
                    { label:"Rows", val:ds.rows },
                    { label:"Cols", val:ds.cols },
                    { label:"Null Rate", val:ds.nullRate },
                    { label:"Domain", val:ds.domain },
                  ].map(s => (
                    <div key={s.label} style={{ background:"#161B22", border:"1px solid #21262D",
                      borderRadius:6, padding:"6px 10px" }}>
                      <div style={{ fontSize:9, color:"#8B949E", textTransform:"uppercase", letterSpacing:"0.08em" }}>{s.label}</div>
                      <div style={{ fontSize:11, color:"#F0F6FC", fontWeight:600, marginTop:2 }}>{s.val}</div>
                    </div>
                  ))}
                </div>

                {/* Target */}
                <div style={{ background:`${ds.domainColor}11`, border:`1px solid ${ds.domainColor}33`,
                  borderRadius:6, padding:"8px 12px" }}>
                  <span style={{ fontSize:10, fontWeight:700, color:ds.domainColor,
                    textTransform:"uppercase", letterSpacing:"0.1em" }}>🎯 Practice Goal: </span>
                  <span style={{ fontSize:12, color:"#C9D1D9", fontFamily:"'DM Sans',system-ui" }}>{ds.target}</span>
                </div>
              </div>

              {/* Tabs */}
              <div style={{ display:"flex", gap:4, marginBottom:16 }}>
                {["issues","cleaning"].map(t => (
                  <button key={t} onClick={() => setTab(t)} style={{
                    padding:"6px 16px", borderRadius:20, border:`1px solid ${tab===t ? ds.domainColor : "#21262D"}`,
                    background:tab===t?`${ds.domainColor}22`:"transparent",
                    color:tab===t?ds.domainColor:"#8B949E", fontSize:11, fontWeight:tab===t?600:400,
                    cursor:"pointer", fontFamily:"'DM Sans',system-ui", textTransform:"capitalize",
                  }}>
                    {t==="issues"?"🔍 Dirty Issues":"🧹 Python Cleaning Code"}
                  </button>
                ))}
              </div>

              {/* Issues Tab */}
              {tab==="issues" && (
                <div style={{ display:"flex", flexDirection:"column", gap:8 }}>
                  {ds.issues.map((issue, i) => {
                    const sc = SEVERITY_COLORS[issue.severity];
                    return (
                      <div key={i} style={{ background:"#161B22", border:`1px solid #21262D`,
                        borderRadius:8, padding:"12px 14px", display:"flex", gap:12, alignItems:"flex-start" }}>
                        <div style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:4, flexShrink:0 }}>
                          <div style={{ width:8, height:8, borderRadius:"50%", background:sc.text, marginTop:4 }}/>
                          <span style={{ fontSize:8, color:sc.text, fontWeight:700, textTransform:"uppercase",
                            letterSpacing:"0.05em", writingMode:"vertical-rl", transform:"rotate(180deg)",
                            marginTop:2 }}>{issue.severity}</span>
                        </div>
                        <div style={{ flex:1 }}>
                          <div style={{ fontSize:12, fontWeight:600, color:"#F0F6FC",
                            fontFamily:"'DM Sans',system-ui", marginBottom:4 }}>{issue.type}</div>
                          <div style={{ fontSize:11, color:"#8B949E", lineHeight:1.6,
                            fontFamily:"'DM Sans',system-ui" }}>{issue.detail}</div>
                        </div>
                        <div style={{ background:sc.bg, border:`1px solid ${sc.border}`,
                          borderRadius:4, padding:"2px 8px", flexShrink:0 }}>
                          <span style={{ fontSize:9, color:sc.text, fontWeight:700, textTransform:"uppercase" }}>
                            {issue.severity}
                          </span>
                        </div>
                      </div>
                    );
                  })}
                  <div style={{ marginTop:8, padding:"10px 14px", background:"#161B22",
                    border:"1px solid #21262D", borderRadius:8, fontSize:11, color:"#8B949E",
                    fontFamily:"'DM Sans',system-ui" }}>
                    💡 <strong style={{ color:"#F0F6FC" }}>How to use:</strong> Load the CSV raw with pandas, run{" "}
                    <code style={{ background:"#0D1117", padding:"1px 4px", borderRadius:3, color:"#5B8FD4" }}>df.info()</code> and{" "}
                    <code style={{ background:"#0D1117", padding:"1px 4px", borderRadius:3, color:"#5B8FD4" }}>df.describe()</code>,
                    then try to identify each issue before looking at the Cleaning Code tab.
                  </div>
                </div>
              )}

              {/* Cleaning Tab */}
              {tab==="cleaning" && (
                <div style={{ display:"flex", flexDirection:"column", gap:10 }}>
                  {ds.cleaning.map((snippet, i) => (
                    <div key={i} style={{ position:"relative" }}>
                      <div style={{ background:"#0D1117", border:`1px solid ${ds.domainColor}33`,
                        borderRadius:8, overflow:"hidden" }}>
                        <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center",
                          padding:"6px 12px", borderBottom:`1px solid ${ds.domainColor}22`,
                          background:`${ds.domainColor}0a` }}>
                          <span style={{ fontSize:10, color:ds.domainColor, fontWeight:600 }}>
                            Fix #{i+1}
                          </span>
                          <button onClick={() => copy(snippet, `${ds.id}-${i}`)} style={{
                            background:"transparent", border:"none", color:copied===`${ds.id}-${i}`?"#5DB878":"#8B949E",
                            fontSize:10, cursor:"pointer", fontFamily:"inherit",
                          }}>
                            {copied===`${ds.id}-${i}`?"✓ copied":"copy"}
                          </button>
                        </div>
                        <pre style={{ margin:0, padding:"12px 14px", fontSize:11, lineHeight:1.7,
                          color:"#C9D1D9", overflowX:"auto", whiteSpace:"pre-wrap" }}>
                          <code>{snippet}</code>
                        </pre>
                      </div>
                    </div>
                  ))}
                  <div style={{ padding:"10px 14px", background:"#161B22", border:"1px solid #21262D",
                    borderRadius:8, fontSize:11, color:"#8B949E", fontFamily:"'DM Sans',system-ui" }}>
                    ⚠️ <strong style={{ color:"#F0F6FC" }}>Challenge mode:</strong> Don't look at these until
                    you've tried to write the cleaning code yourself. The goal is to identify the issues first,
                    then write your own solution, then compare.
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
