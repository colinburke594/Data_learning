"""
Generate 15 new dirty synthetic datasets for the Dataset Library.
Each dataset has intentional data quality issues matching the card descriptions.
"""
import numpy as np
import pandas as pd
import os, random, string, json
from datetime import datetime, timedelta

rng = np.random.default_rng(42)
random.seed(42)
OUT = os.path.dirname(__file__)

def save_csv(df, name):
    path = os.path.join(OUT, name)
    df.to_csv(path, index=False)
    print(f"  ✓ {name}  ({len(df):,} rows × {len(df.columns)} cols)")

def save_json(records, name):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        json.dump(records, f, indent=2, default=str)
    print(f"  ✓ {name}  ({len(records):,} records)")

def rand_dates(start, end, n):
    s = pd.Timestamp(start).value // 10**9
    e = pd.Timestamp(end).value // 10**9
    return pd.to_datetime(rng.integers(s, e, n), unit="s").normalize()

FIRST = ["James","Mary","John","Patricia","Robert","Jennifer","Michael","Linda",
         "William","Barbara","David","Elizabeth","Richard","Susan","Joseph","Jessica",
         "Thomas","Sarah","Charles","Karen","Emma","Liam","Olivia","Noah","Ava","Sophia"]
LAST  = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Wilson",
         "Martinez","Anderson","Taylor","Thomas","Hernandez","Moore","Martin","Jackson",
         "Thompson","White","Lopez","Lee","Gonzalez","Harris","Clark","Lewis","Robinson"]

# ── 1. CLIMATE & WEATHER ──────────────────────────────────────────────────────
print("1. Climate & Weather")
n = 5000
stations = [f"STN{str(i).zfill(4)}" for i in range(1, 51)]
station_arr = rng.choice(stations, n)
dates_cw = rand_dates("2020-01-01", "2024-12-31", n)

# Base temps in Fahrenheit
tmax_f = rng.normal(65, 22, n).round(1)
tmin_f = (tmax_f - rng.uniform(8, 22, n)).round(1)

# DIRTY: mix ~15% of tmax into Celsius (same number, different scale)
celsius_mask = rng.random(n) < 0.15
tmax_dirty = tmax_f.copy().astype(object)
tmax_dirty[celsius_mask] = ((tmax_f[celsius_mask] - 32) * 5 / 9).round(1)

# DIRTY: ~3% null station IDs
station_dirty = station_arr.astype(object)
station_dirty[rng.choice(n, int(n*0.03), replace=False)] = None

# DIRTY: impossible wind (negative & 999)
wind = rng.exponential(12, n).round(1)
bad_wind = rng.random(n) < 0.02
wind_dirty = wind.astype(object)
wind_dirty[bad_wind & (rng.random(n) < 0.5)] = -10
wind_dirty[bad_wind & (rng.random(n) >= 0.5)] = 999

# DIRTY: humidity > 100
humidity = np.clip(rng.normal(62, 18, n), 10, 100).round(1)
humidity_dirty = humidity.astype(object)
hum_bad_idx = rng.choice(n, int(n*0.04), replace=False)
humidity_dirty[hum_bad_idx] = rng.choice([102, 107, 112, 115], int(n*0.04))

# DIRTY: "T" or "trace" for precip
precip = np.clip(rng.exponential(0.12, n), 0, 4.5).round(2)
precip_dirty = precip.astype(object)
trace_mask = rng.random(n) < 0.05
precip_dirty[trace_mask] = rng.choice(["T", "trace", "Trace"], trace_mask.sum())

# DIRTY: ~200 duplicate date-station pairs
dup_idx = rng.choice(n, 200, replace=False)
dup_dates = dates_cw[dup_idx]
dup_stations = station_dirty[dup_idx]

df_cw = pd.DataFrame({
    "station_id": np.append(station_dirty, dup_stations),
    "date": np.append(dates_cw.astype(str), dup_dates.astype(str)),
    "tmax": np.append(tmax_dirty, tmax_dirty[dup_idx]),
    "tmin_f": np.append(tmin_f, tmin_f[dup_idx]),
    "precip_in": np.append(precip_dirty, precip_dirty[dup_idx]),
    "wind_speed_kmh": np.append(wind_dirty, wind_dirty[dup_idx]),
    "humidity_pct": np.append(humidity_dirty, humidity_dirty[dup_idx]),
    "visibility_mi": np.append(np.clip(rng.normal(9, 3, n), 0, 15).round(1), rng.normal(9, 3, 200).round(1)),
    "snow_in": np.append(np.where(rng.random(n) < 0.1, rng.exponential(0.5, n).round(1), 0.0),
                         np.zeros(200)),
    "weather_event": np.append(rng.choice(["Clear","Rain","Snow","Fog","Thunderstorm","Hail","None"], n+200),
                               rng.choice(["Clear","Rain"], 0)),
    "station_city": np.append(rng.choice(["Atlanta","Denver","Chicago","Miami","Seattle",
                                           "Phoenix","Boston","Dallas","Portland","Minneapolis"], n),
                               rng.choice(["Atlanta","Denver"], 200)),
    "data_source": np.append(rng.choice(["NOAA","WMO","Regional","Estimated"], n),
                              rng.choice(["NOAA"], 200)),
})
save_csv(df_cw, "climate_weather_dirty.csv")

# ── 2. SOCIAL MEDIA ANALYTICS ────────────────────────────────────────────────
print("2. Social Media Analytics")
n = 3400
# DIRTY: platform naming variants
platform_variants = rng.choice(
    ["Instagram","IG","instagram","INSTA","Twitter","X","twitter","TW"],
    n, p=[0.30,0.07,0.07,0.03,0.30,0.09,0.07,0.07]
)
content_types = rng.choice(["Reel","Story","Post","Carousel","Tweet","Thread","Poll"], n)
post_dates_sm = rand_dates("2023-01-01", "2024-12-31", n)

impressions = rng.integers(100, 500000, n)
reach_base = (impressions * rng.uniform(0.5, 0.95, n)).astype(int)

# DIRTY: ~5% reach > impressions (impossible)
bad_reach_mask = rng.random(n) < 0.05
reach_dirty = reach_base.copy()
reach_dirty[bad_reach_mask] = (impressions[bad_reach_mask] * rng.uniform(1.01, 1.5, bad_reach_mask.sum())).astype(int)

likes = (reach_dirty * rng.uniform(0.02, 0.12, n)).astype(int)
comments = (likes * rng.uniform(0.03, 0.15, n)).astype(int)
shares = (likes * rng.uniform(0.01, 0.08, n)).astype(int)

# DIRTY: engagement_rate as % and decimal mixed
eng_rate_raw = ((likes + comments + shares) / np.maximum(impressions, 1) * 100).round(4)
eng_dirty = eng_rate_raw.astype(object)
eng_mask = rng.random(n) < 0.45
eng_dirty[eng_mask] = (eng_rate_raw[eng_mask] / 100).round(6)

# DIRTY: hashtags in 3 formats
def rand_hashtag():
    tags = rng.choice(["#data","#ai","#tech","#marketing","#growth","#analytics",
                        "#business","#startup","#content","#socialmedia"], rng.integers(1, 5), replace=False)
    fmt = rng.integers(0, 3)
    if fmt == 0: return " ".join(tags)
    elif fmt == 1: return str(list(t.lstrip("#") for t in tags))
    else: return ",".join(t.lstrip("#") for t in tags)

hashtags = [rand_hashtag() for _ in range(n)]

# DIRTY: follower_count outliers (0, 1, billions)
follower_count = rng.integers(100, 500000, n).astype(object)
fc_zero_idx = rng.choice(n, int(n*0.01), replace=False)
fc_one_idx  = rng.choice(n, int(n*0.01), replace=False)
fc_big_idx  = rng.choice(n, int(n*0.005), replace=False)
follower_count[fc_zero_idx] = 0
follower_count[fc_one_idx] = 1
follower_count[fc_big_idx] = rng.choice([1200000000, 2400000000, 890000000], int(n*0.005))

# DIRTY: duplicate post IDs
base_post_ids = [f"POST_{i:06d}" for i in range(n)]
dup_post_idx = rng.choice(n, 40, replace=False)
post_ids_arr = base_post_ids.copy()
for idx in dup_post_idx[:20]:
    post_ids_arr[idx] = post_ids_arr[dup_post_idx[20]]

# DIRTY: sentiment free text
sentiment_dirty = rng.choice(["positive","pos","good","great","+",1,"negative","neg","bad","-",0, None], n,
    p=[0.16,0.06,0.06,0.06,0.04,0.05,0.16,0.06,0.06,0.04,0.05,0.20])

df_sm = pd.DataFrame({
    "post_id": post_ids_arr,
    "platform": platform_variants,
    "account": [f"@{rng.choice(FIRST).lower()}_{rng.choice(LAST).lower()}" for _ in range(n)],
    "post_date": post_dates_sm.astype(str),
    "content_type": content_types,
    "impressions": impressions,
    "reach": reach_dirty,
    "likes": likes,
    "comments": comments,
    "shares": shares,
    "saves": (likes * rng.uniform(0.02, 0.10, n)).astype(int),
    "clicks": (reach_dirty * rng.uniform(0.01, 0.06, n)).astype(int),
    "hashtags": hashtags,
    "engagement_rate": eng_dirty,
    "follower_count": follower_count,
    "sentiment": sentiment_dirty,
})
save_csv(df_sm, "social_media_analytics_dirty.csv")

# ── 3. SUPPLY CHAIN LOGISTICS ────────────────────────────────────────────────
print("3. Supply Chain Logistics")
n = 4200
order_dates_sc = rand_dates("2022-01-01", "2024-06-30", n)
ship_dates_sc  = order_dates_sc + pd.to_timedelta(rng.integers(1, 5, n), unit="D")
delivery_days  = rng.integers(3, 21, n)
delivery_dates_sc = ship_dates_sc + pd.to_timedelta(delivery_days, unit="D")

# DIRTY: ~6% delivered before shipped
bad_del = rng.random(n) < 0.06
delivery_list = list(delivery_dates_sc.astype(str))
ship_list     = list(ship_dates_sc.astype(str))
for i in range(n):
    if bad_del[i]:
        delivery_list[i] = str((ship_dates_sc[i] - pd.Timedelta(days=int(rng.integers(1, 5)))).date())
delivery_dirty = np.array(delivery_list, dtype=object)

# DIRTY: weight in kg and lbs mixed (no unit indicator)
weight_kg = rng.uniform(0.5, 500, n).round(2)
weight_dirty = weight_kg.astype(object).copy()
lbs_mask = rng.random(n) < 0.40
weight_dirty[lbs_mask] = (weight_kg[lbs_mask] * 2.20462).round(2)  # convert to lbs, no label

# DIRTY: delivery status variants
status_map = rng.choice(
    ["Delivered","delivered","DELIVERED","Del.","D",
     "In Transit","in_transit","TRANSIT","Pending","PENDING","Returned","returned"],
    n, p=[0.30,0.08,0.05,0.03,0.02,0.20,0.06,0.04,0.10,0.04,0.04,0.04]
)

# DIRTY: carrier naming variants
carrier_dirty = rng.choice(
    ["UPS","ups","United Parcel Service",
     "FedEx","fedex","Federal Express",
     "DHL","dhl","USPS","usps"],
    n, p=[0.18,0.06,0.05,0.18,0.06,0.05,0.14,0.06,0.14,0.08]
)

# DIRTY: shipping cost mixed USD and EUR
cost_usd = rng.uniform(5, 800, n).round(2)
cost_dirty = cost_usd.astype(object).copy()
eur_mask = rng.random(n) < 0.25
cost_dirty[eur_mask] = (cost_usd[eur_mask] * 0.92).round(2)  # EUR values, no label

# DIRTY: ~12% null tracking numbers despite Delivered status
tracking = [f"1Z{rng.integers(1000000000,9999999999)}" for _ in range(n)]
tracking_dirty = list(tracking)
null_track_idx = rng.choice(np.where(status_map == "Delivered")[0],
                              size=min(int(n*0.12), (status_map=="Delivered").sum()), replace=False)
for i in null_track_idx:
    tracking_dirty[i] = None

df_sc = pd.DataFrame({
    "shipment_id": [f"SHP-{rng.integers(100000,999999)}" for _ in range(n)],
    "order_date": order_dates_sc.astype(str),
    "ship_date": ship_dates_sc.astype(str),
    "delivery_date": delivery_dirty,
    "carrier": carrier_dirty,
    "origin_city": rng.choice(["Los Angeles","Chicago","Dallas","Houston","New York","Phoenix","Miami","Atlanta"], n),
    "destination_city": rng.choice(["Seattle","Boston","Denver","Las Vegas","Detroit","Minneapolis","Portland","Austin"], n),
    "product_id": [f"SKU-{rng.integers(10000,99999)}" for _ in range(n)],
    "product_category": rng.choice(["Electronics","Clothing","Furniture","Food","Industrial","Medical","Auto"], n),
    "weight": weight_dirty,
    "quantity": rng.integers(1, 100, n),
    "shipping_cost": cost_dirty,
    "delivery_status": status_map,
    "days_in_transit": delivery_days,
    "on_time": rng.choice(["Yes","No","yes","no","Y","N",1,0], n),
    "damage_reported": rng.choice([True, False, "True", "False", 1, 0, None], n,
                                    p=[0.08,0.80,0.02,0.02,0.02,0.02,0.04]),
    "tracking_number": tracking_dirty,
    "customer_id": [f"CUST-{rng.integers(10000,99999)}" for _ in range(n)],
    "region": rng.choice(["West","Midwest","South","Northeast","Southwest"], n),
    "priority": rng.choice(["High","Medium","Low","URGENT","Standard","standard"], n),
})
save_csv(df_sc, "supply_chain_logistics_dirty.csv")

# ── 4. STOCK PRICE HISTORY ───────────────────────────────────────────────────
print("4. Stock Price History")
tickers = ["AAPL","MSFT","AMZN","GOOGL","META","TSLA","NVDA","JPM","JNJ","V",
           "WMT","UNH","PG","HD","MA","DIS","PYPL","BAC","NFLX","INTC",
           "CSCO","PFE","T","VZ","KO","MRK","PEP","ABT","CVX","NKE",
           "ORCL","LLY","TMO","ACN","AVGO","QCOM","TXN","MDT","HON","LIN",
           "NEE","COP","SBUX","IBM","GE","CAT","BA","MMM","AXP","USB"]
n_per_stock = 100
stock_rows = []
for ticker in tickers:
    price = rng.uniform(20, 800)
    vol_base = rng.uniform(1000000, 50000000)
    dates_s = pd.bdate_range("2024-01-01", periods=n_per_stock)
    for i, d in enumerate(dates_s):
        pct_chg = rng.normal(0.0003, 0.015)
        price = max(1, price * (1 + pct_chg))
        daily_range = price * rng.uniform(0.005, 0.025)
        high = round(price + daily_range * rng.uniform(0.3, 1.0), 2)
        low  = round(price - daily_range * rng.uniform(0.3, 1.0), 2)
        open_p = round(price * rng.uniform(0.995, 1.005), 2)
        close = round(price, 2)
        volume = int(vol_base * rng.uniform(0.5, 2.5))
        stock_rows.append({"ticker": ticker, "date": d.strftime("%Y-%m-%d"),
                           "open": open_p, "high": high, "low": low,
                           "close": close, "volume": volume,
                           "adj_close": round(close * rng.uniform(0.98, 1.0), 2),
                           "dividend": round(rng.choice([0.0, 0.0, 0.0, rng.uniform(0.1, 2.0)]), 2)})

df_stock = pd.DataFrame(stock_rows)

# DIRTY: high < low on ~80 rows
bad_idx = rng.choice(len(df_stock), 80, replace=False)
df_stock.loc[bad_idx, ["high","low"]] = df_stock.loc[bad_idx, ["low","high"]].values

# DIRTY: ~200 zero-volume rows
zero_vol_idx = rng.choice(len(df_stock), 200, replace=False)
df_stock.loc[zero_vol_idx, "volume"] = 0

# DIRTY: ~30 duplicate date-ticker pairs
dup_stock_idx = rng.choice(len(df_stock), 30, replace=False)
df_stock_dup = df_stock.iloc[dup_stock_idx].copy()
df_stock_dup["close"] = df_stock_dup["close"] * rng.uniform(0.98, 1.02, 30)
df_stock = pd.concat([df_stock, df_stock_dup], ignore_index=True)

# DIRTY: ~5 future dates
future_rows = df_stock.sample(5, random_state=1).copy()
future_rows["date"] = pd.date_range("2026-01-01", periods=5).strftime("%Y-%m-%d")
df_stock = pd.concat([df_stock, future_rows], ignore_index=True)

# DIRTY: 2 stocks with prices in cents (100x)
cent_tickers = rng.choice(tickers, 2, replace=False)
cent_mask = df_stock["ticker"].isin(cent_tickers)
df_stock.loc[cent_mask, ["open","high","low","close","adj_close"]] *= 100

# DIRTY: weekend date injected
weekend_row = df_stock.sample(1, random_state=5).copy()
weekend_row["date"] = "2024-01-06"  # Saturday
df_stock = pd.concat([df_stock, weekend_row], ignore_index=True)

save_csv(df_stock, "stock_price_history_dirty.csv")

# ── 5. CUSTOMER REVIEWS NLP ──────────────────────────────────────────────────
print("5. Customer Reviews NLP")
n = 2000
products = ["Wireless Headphones","Laptop Stand","USB-C Hub","Bluetooth Speaker","Phone Case",
            "Running Shoes","Yoga Mat","Coffee Maker","Air Fryer","Smart Watch",
            "Desk Lamp","Keyboard","Mouse","Monitor","Backpack","Water Bottle",
            "Fitness Tracker","Power Bank","Earbuds","Tablet Stand"]
pos_phrases = ["Great product!", "Works perfectly.", "Very happy with this purchase.",
               "Excellent quality!", "Highly recommend.", "Fast shipping and great quality.",
               "Love it! Works as described.", "Best purchase I've made in a while.",
               "Solid build quality.", "Does exactly what it says."]
neg_phrases = ["Terrible quality.", "Broke after one week.", "Complete waste of money.",
               "Does not work as advertised.", "Very disappointed.", "Returned immediately.",
               "Cheap materials.", "Stopped working after 3 days.", "Don't buy this.",
               "Absolute garbage."]
neutral_phrases = ["It's okay.", "Does the job.", "Average product.", "Nothing special.",
                   "Met my expectations.", "Decent for the price.", "Works fine."]

ratings = rng.choice([1,2,3,4,5], n, p=[0.06,0.09,0.15,0.35,0.35])
sentiments_base = np.where(ratings >= 4, "positive", np.where(ratings <= 2, "negative", "neutral"))

reviews = []
for i in range(n):
    if sentiments_base[i] == "positive":
        text = rng.choice(pos_phrases)
    elif sentiments_base[i] == "negative":
        text = rng.choice(neg_phrases)
    else:
        text = rng.choice(neutral_phrases)
    reviews.append(text)

# DIRTY: HTML entities in ~10% of reviews
html_idx = rng.choice(n, int(n*0.10), replace=False)
for i in html_idx:
    reviews[i] = reviews[i].replace("!", " &amp; great price!").replace(".", " &lt;quality&gt; is good.")

# DIRTY: rating-sentiment contradiction ~8%
contradict_idx = rng.choice(n, int(n*0.08), replace=False)
for i in contradict_idx:
    if ratings[i] == 5:
        reviews[i] = rng.choice(["terrible quality, hate it", "broken on arrival, very bad", "worst product ever"])

# DIRTY: non-English reviews ~4%
foreign_idx = rng.choice(n, int(n*0.04), replace=False)
foreign = ["Excelente producto, muy recomendado!", "Muy buena calidad y precio.",
           "Très bon produit, je recommande.", "Produit de qualité, livraison rapide.",
           "Sehr gutes Produkt, bin sehr zufrieden.", "Gute Qualität, schnelle Lieferung."]
for i in foreign_idx:
    reviews[i] = rng.choice(foreign)

# DIRTY: emoji-only reviews ~2%
emoji_idx = rng.choice(n, int(n*0.02), replace=False)
emoji_reviews = ["⭐⭐⭐⭐⭐", "👍👍👍", "❤️🔥💯", "😍✨🎉", "👎👎", "😭💔"]
for i in emoji_idx:
    reviews[i] = rng.choice(emoji_reviews)

# DIRTY: some ratings out of 1-5 range
bad_rating_idx = rng.choice(n, 30, replace=False)
ratings_dirty = ratings.astype(object).copy()
for i in bad_rating_idx:
    ratings_dirty[i] = rng.choice([0, 6, 10])

# DIRTY: ~120 duplicate reviews
dup_review_idx = rng.choice(n, 120, replace=False)
for i in dup_review_idx[:60]:
    reviews[i] = reviews[dup_review_idx[60]]

product_ids = rng.choice([f"PROD_{str(i).zfill(4)}" for i in range(1, 201)], n)
product_names_arr = rng.choice(products, n)
product_launch_dates = {pid: rand_dates("2020-01-01", "2023-01-01", 1)[0]
                        for pid in np.unique(product_ids)}
review_dates_nlp = rand_dates("2022-01-01", "2024-12-31", n)

# DIRTY: ~30 reviews before product launch date
early_idx = rng.choice(n, 30, replace=False)
review_dates_list = list(review_dates_nlp.strftime("%Y-%m-%d"))
for i in early_idx:
    launch = product_launch_dates[product_ids[i]]
    review_dates_list[i] = (launch - pd.Timedelta(days=int(rng.integers(10, 365)))).strftime("%Y-%m-%d")
review_dates_dirty = np.array(review_dates_list, dtype=object)

verified = rng.choice(["Y","Yes","TRUE","1",True,None], n,
                        p=[0.20,0.15,0.15,0.15,0.25,0.10])
helpful_votes = rng.integers(0, 150, n)

df_nlp = pd.DataFrame({
    "review_id": [f"REV_{i:07d}" for i in range(n)],
    "product_id": product_ids,
    "product_name": product_names_arr,
    "rating": ratings_dirty,
    "title": [r[:40] + "..." if len(r) > 40 else r for r in reviews],
    "review_text": reviews,
    "reviewer_name": [f"{rng.choice(FIRST)} {rng.choice(LAST)}" for _ in range(n)],
    "verified_purchase": verified,
    "helpful_votes": helpful_votes,
    "review_date": review_dates_dirty,
    "category": rng.choice(["Electronics","Sports","Kitchen","Accessories","Computing"], n),
})
save_csv(df_nlp, "customer_reviews_nlp_dirty.csv")

# ── 6. CENSUS DEMOGRAPHICS ───────────────────────────────────────────────────
print("6. Census Demographics")
n = 5000
occupations = ["Tech-support","Craft-repair","Other-service","Sales","Exec-managerial",
                "Prof-specialty","Handlers-cleaners","Machine-op-inspct","Adm-clerical",
                "Farming-fishing","Transport-moving","Priv-house-serv","Protective-serv","Armed-Forces"]
education_levels = ["Bachelors","Some-college","11th","HS-grad","Prof-school",
                     "Assoc-acdm","Assoc-voc","9th","7th-8th","12th","Masters","1st-4th",
                     "10th","Doctorate","5th-6th","Preschool"]
# DIRTY: income mixed categorical and numeric
age_c = rng.integers(17, 90, n)
income_threshold = 50000
actual_income = np.where(age_c > 25,
                          rng.lognormal(10.5, 0.8, n),
                          rng.lognormal(9.8, 0.6, n)).round(0).astype(int)
income_dirty = actual_income.astype(object).copy()
cat_mask = rng.random(n) < 0.50
income_dirty[cat_mask & (actual_income > 50000)] = ">50K"
income_dirty[cat_mask & (actual_income <= 50000)] = "<=50K"

# DIRTY: age=99 used as unknown code
age_dirty = age_c.astype(object).copy()
age_dirty[rng.choice(n, int(n*0.04), replace=False)] = 99

# DIRTY: education inconsistency
edu_base = rng.choice(education_levels, n)
edu_dirty = edu_base.astype(object).copy()
edu_variants = {
    "Bachelors": ["Bachelor","BS","B.S.","4yr degree","bachelors","BACHELORS"],
    "Masters": ["Master","MS","M.S.","Graduate","masters","MASTERS"],
    "Doctorate": ["PhD","Ph.D.","Doctor","doctorate"],
    "HS-grad": ["High School","HS","H.S.","GED","high school grad"],
}
for i in range(n):
    if edu_base[i] in edu_variants and rng.random() < 0.35:
        edu_dirty[i] = rng.choice(edu_variants[edu_base[i]])

# DIRTY: hours_per_week includes 99 and >100
hours_pw = rng.integers(1, 65, n).astype(object)
hours_pw[rng.choice(n, int(n*0.04), replace=False)] = 99
hours_pw[rng.choice(n, int(n*0.02), replace=False)] = rng.choice([80, 90, 100, 110, 120], int(n*0.02))

# DIRTY: marital status two encoding systems
marital_full = rng.choice(["Married-civ-spouse","Never-married","Divorced",
                             "Separated","Widowed","Married-AF-spouse"], n,
                            p=[0.45,0.33,0.13,0.04,0.03,0.02])
marital_dirty = marital_full.astype(object).copy()
abbrev_map = {"Married-civ-spouse": ["M","Married"],
              "Never-married": ["S","Single"],
              "Divorced": ["D","Div."],
              "Separated": ["Sep","Sep."],
              "Widowed": ["W","Wid."]}
for i in range(n):
    if marital_full[i] in abbrev_map and rng.random() < 0.30:
        marital_dirty[i] = rng.choice(abbrev_map[marital_full[i]])

# DIRTY: null occupation for employed
occ_arr = rng.choice(occupations, n).astype(object)
workclass = rng.choice(["Private","Self-emp-not-inc","Self-emp-inc","Federal-gov",
                          "Local-gov","State-gov","Without-pay","Never-worked"], n,
                         p=[0.70,0.08,0.05,0.04,0.05,0.04,0.02,0.02])
null_occ_mask = (workclass == "Private") & (rng.random(n) < 0.08)
occ_arr[null_occ_mask] = None

# DIRTY: FIPS codes missing leading zeros
fips_full = [f"{rng.integers(1,57):02d}{rng.integers(1,840):03d}" for _ in range(n)]
fips_dirty = []
for f in fips_full:
    if rng.random() < 0.15 and f.startswith("0"):
        fips_dirty.append(f.lstrip("0") or "0")
    else:
        fips_dirty.append(f)

df_census = pd.DataFrame({
    "id": range(1, n+1),
    "age": age_dirty,
    "workclass": workclass,
    "education": edu_dirty,
    "marital_status": marital_dirty,
    "occupation": occ_arr,
    "relationship": rng.choice(["Wife","Own-child","Husband","Not-in-family","Other-relative","Unmarried"], n),
    "race": rng.choice(["White","Black","Asian-Pac-Islander","Amer-Indian-Eskimo","Other"], n,
                         p=[0.86,0.10,0.02,0.01,0.01]),
    "sex": rng.choice(["Male","Female"], n, p=[0.67,0.33]),
    "capital_gain": np.where(rng.random(n) < 0.08, rng.integers(1, 99999, n), 0),
    "capital_loss": np.where(rng.random(n) < 0.05, rng.integers(1, 4000, n), 0),
    "hours_per_week": hours_pw,
    "native_country": rng.choice(["United-States","Mexico","Philippines","Germany","Canada",
                                    "Puerto-Rico","El-Salvador","India","Cuba","South"], n,
                                   p=[0.90,0.02,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01]),
    "income": income_dirty,
    "housing": rng.choice(["Own","Rent","Mortgage","Other"], n, p=[0.35,0.30,0.30,0.05]),
    "n_household_members": rng.integers(1, 8, n),
    "savings_usd": np.where(rng.random(n) < 0.30, 0,
                             rng.lognormal(8, 1.5, n).clip(0, 500000).round(0)).astype(int),
    "broadband_access": rng.choice(["Yes","No","yes","no","Y","N"], n),
    "employment_status": rng.choice(["Employed","Unemployed","Self-employed","Retired","Student"], n),
    "commute_time_min": rng.integers(0, 120, n),
    "county_fips": fips_dirty,
    "rent_usd": np.where(rng.random(n) < 0.55, 0, rng.integers(400, 4000, n)),
})
save_csv(df_census, "census_demographics_dirty.csv")

# ── 7. ENERGY CONSUMPTION ────────────────────────────────────────────────────
print("7. Energy Consumption")
n_buildings = 20
n_hours = 250  # 250 hours per building = 5000 total rows
energy_rows = []
building_ids_raw = [f"BLDG{str(i).zfill(3)}" for i in range(1, n_buildings+1)]

for bldg_i, bldg in enumerate(building_ids_raw):
    base_kwh = rng.uniform(50, 800)
    # DIRTY: building ID format variants
    id_variants = [bldg, bldg.lower(), f"Building {bldg_i+1}", f"B{bldg_i+1:03d}"]
    bldg_id_used = rng.choice(id_variants)

    hours = pd.date_range("2023-01-01", periods=n_hours, freq="h")
    for h_i, ts in enumerate(hours):
        hour = ts.hour
        dow = ts.dayofweek
        seasonal = 1 + 0.15 * np.cos((ts.month - 1) * 2 * np.pi / 12 - np.pi)
        daily = 0.8 + 0.4 * np.sin((hour - 6) * np.pi / 12)
        weekend = 0.85 if dow >= 5 else 1.0
        kwh = base_kwh * seasonal * daily * weekend * rng.uniform(0.92, 1.08)

        energy_rows.append({
            "building_id": bldg_id_used,
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "kwh_consumed": round(kwh, 3),
            "peak_demand_kw": round(kwh * rng.uniform(1.0, 1.4), 2),
            "outdoor_temp_f": round(rng.normal(65, 22), 1),
            "occupancy_pct": round(max(0, rng.normal(0.6 if dow < 5 and 8 <= hour <= 18 else 0.15, 0.15)), 2),
            "floor_area_sqft": int(rng.uniform(2000, 50000)),
            "building_type": rng.choice(["Office","Retail","Warehouse","Hospital","School","Hotel"]),
            "meter_id": f"MTR-{rng.integers(1000,9999)}",
            "data_quality_flag": rng.choice(["OK","OK","OK","OK","ESTIMATED","ERROR"], p=[0.85,0.0,0.0,0.0,0.10,0.05])
        })

df_energy = pd.DataFrame(energy_rows)

# DIRTY: negative consumption ~0.5%
neg_idx = rng.choice(len(df_energy), int(len(df_energy)*0.005), replace=False)
df_energy.loc[neg_idx, "kwh_consumed"] = -df_energy.loc[neg_idx, "kwh_consumed"]

# DIRTY: unit mix — 2 buildings report in MWh (1000x smaller)
mwh_bldgs = rng.choice(df_energy["building_id"].unique(), 2, replace=False)
mwh_mask = df_energy["building_id"].isin(mwh_bldgs)
df_energy.loc[mwh_mask, "kwh_consumed"] = (df_energy.loc[mwh_mask, "kwh_consumed"] / 1000).round(6)

# DIRTY: ~3% missing hours (drop rows entirely — user will see gaps)
drop_idx = rng.choice(len(df_energy), int(len(df_energy)*0.03), replace=False)
df_energy = df_energy.drop(drop_idx).reset_index(drop=True)

# DIRTY: meter rollover — cause some apparent huge drops
rollover_idx = rng.choice(len(df_energy), 5, replace=False)
df_energy.loc[rollover_idx, "kwh_consumed"] = 9999.9 - df_energy.loc[rollover_idx, "kwh_consumed"]

save_csv(df_energy, "energy_consumption_dirty.csv")

# ── 8. CLINICAL GENOMICS ─────────────────────────────────────────────────────
print("8. Clinical Genomics")
n = 450
gene_names = [f"GENE_{g}" for g in ["TP53","BRCA1","BRCA2","EGFR","KRAS","MYC","RB1","PTEN",
                "APC","VHL","MLH1","CDKN2A","CDH1","ATM","CHEK2","PALB2","RAD51","ERBB2",
                "PIK3CA","SMAD4","FBXW7","NOTCH1","IDH1","IDH2","FLT3","NPM1","DNMT3A",
                "RUNX1","ASXL1","TET2","JAK2","CALR","SF3B1","U2AF1","SRSF2"]]
# Add more generic gene probes to reach ~50 feature columns
for i in range(15):
    gene_names.append(f"PROBE_{i+1}_A")
    gene_names.append(f"PROBE_{i+1}_B")  # DIRTY: duplicate probes for same gene

# Clinical metadata
cancer_types = rng.choice(["Breast","Lung","Colon","Leukemia","Lymphoma","Pancreatic"], n,
                            p=[0.25,0.20,0.18,0.15,0.12,0.10])
stages = rng.choice(["I","II","III","IV"], n, p=[0.25,0.30,0.28,0.17])
treatments = rng.choice(["Chemotherapy","Immunotherapy","Radiation","Surgery","Combined"], n)
response = rng.choice(["Complete","Partial","Stable","Progressive"], n, p=[0.28,0.32,0.22,0.18])
survival_days = np.where(response == "Progressive",
                          rng.integers(60, 800, n),
                          rng.integers(180, 3000, n))
# DIRTY: censoring flag separate (should be combined)
censored = rng.choice([0, 1], n, p=[0.55, 0.45])

gene_data = {}
batch = rng.choice([1, 2, 3], n, p=[0.35, 0.35, 0.30])

for gene in gene_names:
    # Base expression
    expr_raw = rng.lognormal(4.5, 1.8, n)
    # DIRTY: batch effects — systematic shift by batch
    batch_effect = np.where(batch == 1, 1.0, np.where(batch == 2, 1.35, 0.72))
    expr = expr_raw * batch_effect
    # DIRTY: some columns are log2 normalized, others raw
    if rng.random() < 0.45:
        expr = np.log2(expr + 1).round(4)
    else:
        expr = expr.round(2)
    # DIRTY: MNAR — very high/low values have more missings
    miss_prob = np.where((expr > np.percentile(expr, 90)) | (expr < np.percentile(expr, 10)), 0.25, 0.05)
    expr_dirty = expr.astype(object)
    for i in range(n):
        if rng.random() < miss_prob[i]:
            expr_dirty[i] = None
    gene_data[gene] = expr_dirty

df_genomics = pd.DataFrame({"patient_id": [f"PAT_{i:04d}" for i in range(n)],
                              "age": rng.integers(25, 80, n),
                              "sex": rng.choice(["Male","Female"], n),
                              "cancer_type": cancer_types,
                              "stage": stages,
                              "treatment": treatments,
                              "response": response,
                              "survival_days": survival_days,
                              "censored": censored,
                              "batch": batch})
for g, vals in gene_data.items():
    df_genomics[g] = vals

# DIRTY: ~2% sex-marker inconsistency (clinical sex != genomic sex markers)
sex_err_idx = rng.choice(n, int(n*0.02), replace=False)
df_genomics.loc[sex_err_idx, "sex"] = np.where(
    df_genomics.loc[sex_err_idx, "sex"] == "Male", "Female", "Male")

save_csv(df_genomics, "clinical_genomics_dirty.csv")

# ── 9. FINANCIAL FRAUD DETECTION ────────────────────────────────────────────
print("9. Financial Fraud Detection")
n_legit = 4915
n_fraud = 85  # ~1.7%
def make_pca(n, is_fraud):
    data = {}
    for i in range(1, 29):
        if is_fraud:
            mean = rng.uniform(-2.5, 2.5)
            std = rng.uniform(0.8, 3.0)
        else:
            mean, std = 0.0, 1.0
        data[f"V{i}"] = rng.normal(mean, std, n).round(6)
    return data

v_leg = make_pca(n_legit, False)
v_fr  = make_pca(n_fraud, True)
amt_leg  = np.clip(rng.lognormal(3.5, 1.9, n_legit), 0, 25000).round(2)
amt_fr   = np.clip(rng.lognormal(5.0, 1.4, n_fraud), 1, 8000).round(2)

df_leg = pd.DataFrame(v_leg); df_leg["Amount"] = amt_leg; df_leg["Class"] = 0
df_fr  = pd.DataFrame(v_fr);  df_fr["Amount"]  = amt_fr;  df_fr["Class"]  = 1
df_ff = pd.concat([df_leg, df_fr], ignore_index=True)

total = len(df_ff)
time_arr = np.sort(rng.uniform(0, 172792, total)).round(1)
df_ff.insert(0, "Time", time_arr)

# DIRTY: Amount has currency symbols on ~3% of rows
amt_dirty = df_ff["Amount"].astype(object).copy()
sym_idx = rng.choice(total, int(total*0.03), replace=False)
for i in sym_idx:
    amt_dirty.iloc[i] = f"${df_ff['Amount'].iloc[i]:.2f}"
df_ff["Amount"] = amt_dirty

# DIRTY: zero-amount transactions
zero_amt_idx = rng.choice(total, 100, replace=False)
df_ff.loc[zero_amt_idx, "Amount"] = 0

# DIRTY: duplicate transactions
dup_ff_idx = rng.choice(total, 30, replace=False)
df_ff = pd.concat([df_ff, df_ff.iloc[dup_ff_idx]], ignore_index=True)

df_ff = df_ff.sample(frac=1, random_state=42).reset_index(drop=True)
save_csv(df_ff, "financial_fraud_dirty.csv")

# ── 10. IoT SENSOR TELEMETRY ────────────────────────────────────────────────
print("10. IoT Sensor Telemetry")
n = 5000
devices = [f"dev_{str(i).zfill(3)}" for i in range(1, 51)]
device_arr = rng.choice(devices, n)

base_ts = pd.Timestamp("2024-01-01")
seconds_offsets = np.sort(rng.integers(0, 30*24*3600, n))
timestamps_iot = [(base_ts + pd.Timedelta(seconds=int(s))).strftime("%Y-%m-%d %H:%M:%S")
                   for s in seconds_offsets]

# DIRTY: device ID format change after a cutoff
cutoff = int(n * 0.55)
device_dirty = device_arr.astype(object).copy()
for i in range(cutoff, n):
    # After cutoff: format changes from dev_001 to DEV-001
    device_dirty[i] = device_arr[i].replace("dev_", "DEV-")

# DIRTY: out-of-order timestamps (~2%)
oot_idx = rng.choice(n, int(n*0.02), replace=False)
for i in oot_idx:
    j = rng.integers(0, n)
    timestamps_iot[i], timestamps_iot[j] = timestamps_iot[j], timestamps_iot[i]

temp_c = rng.normal(22, 8, n).round(2)
humidity_iot = np.clip(rng.normal(55, 15, n), 10, 95).round(1)
pressure = rng.normal(1013.25, 10, n).round(2)
vibration = rng.exponential(2.5, n).round(4)

# DIRTY: precision upgrade mid-stream
temp_dirty = temp_c.astype(object).copy()
for i in range(int(n*0.40)):
    temp_dirty[i] = int(round(temp_c[i]))  # early rows: integer precision

# DIRTY: impossible combinations (temp > max but status=normal)
machine_status = rng.choice(["normal","warning","error","maintenance"], n,
                               p=[0.88, 0.07, 0.03, 0.02])
temp_dirty2 = np.array(temp_dirty, dtype=object)
impossible_idx = rng.choice(n, int(n*0.001), replace=False)
for i in impossible_idx:
    temp_dirty2[i] = 9999
    machine_status[i] = "normal"

# DIRTY: null burst periods (reboot simulation)
reboot_start = rng.integers(0, n-300, 5)
for rs in reboot_start:
    burst_len = rng.integers(60, 200)
    for bi in range(rs, min(rs + burst_len, n)):
        temp_dirty2[bi] = None
        humidity_iot[bi] = None
        vibration[bi] = None

# DIRTY: ~3 future timestamps
future_ts_idx = rng.choice(n, 3, replace=False)
for i in future_ts_idx:
    timestamps_iot[i] = f"2027-{rng.integers(1,12):02d}-{rng.integers(1,28):02d} 12:00:00"

battery = np.clip(rng.normal(75, 20, n), 0, 100).round(1)
firmware = rng.choice(["v1.2.1","v1.2.1","v1.2.1","v1.3.0","v1.3.0","v2.0.0"], n)

df_iot = pd.DataFrame({
    "device_id": device_dirty,
    "timestamp": timestamps_iot,
    "sensor_type": rng.choice(["temperature","humidity","vibration","pressure","combined"], n),
    "temperature_c": temp_dirty2,
    "humidity_pct": humidity_iot,
    "pressure_hpa": pressure,
    "vibration_ms2": vibration,
    "machine_status": machine_status,
    "battery_pct": battery,
    "firmware_version": firmware,
})
save_csv(df_iot, "iot_sensor_telemetry_dirty.csv")

# ── 11. EMPLOYEE ENGAGEMENT SURVEY ──────────────────────────────────────────
print("11. Employee Engagement Survey")
n = 2800
departments = ["Engineering","Sales","Marketing","HR","Finance","Operations","Legal","Product"]
dept_arr = rng.choice(departments, n)

def likert(n, scale_max, mean, std):
    vals = np.clip(np.round(rng.normal(mean, std, n)), 1, scale_max).astype(int)
    return vals

# DIRTY: mixed scales — some questions 1-5, some 1-7, one 0-10
q_scales = {"1-5": range(1, 11), "1-7": range(11, 21), "0-10": range(21, 25), "1-5b": range(25, 36)}
data = {"employee_id": [f"EMP_{i:05d}" for i in range(n)]}

for q in range(1, 11):   # 1-5 engagement questions
    vals = likert(n, 5, 3.6, 1.1).astype(object)
    # DIRTY: free text in numeric cols
    text_idx = rng.choice(n, int(n*0.05), replace=False)
    for i in text_idx:
        vals[i] = rng.choice(["N/A","Don't know","n/a","NA","?"])
    # DIRTY: out of range
    oob_idx = rng.choice(n, int(n*0.02), replace=False)
    for i in oob_idx:
        vals[i] = rng.choice([6, 7, 0])
    data[f"q{q:02d}_engagement"] = vals

for q in range(1, 11):   # 1-7 satisfaction questions
    vals = likert(n, 7, 4.5, 1.6).astype(object)
    text_idx = rng.choice(n, int(n*0.08), replace=False)
    for i in text_idx:
        vals[i] = None  # MNAR - high-level mgrs skip these
    data[f"q{q:02d}_satisfaction"] = vals

for q in range(1, 6):   # 0-10 NPS-style
    vals = np.clip(np.round(rng.normal(6.5, 2.5, n)), 0, 10).astype(int)
    data[f"q{q:02d}_mgr_effectiveness"] = vals

for q in range(1, 11):  # 1-5 more questions
    data[f"q{q:02d}_additional"] = likert(n, 5, 3.4, 1.2)

data["would_recommend"] = rng.choice(["Yes","No","Maybe","1","0","yes","no"], n)
data["likely_to_stay"] = rng.choice([1,2,3,4,5,6,7], n)

# DIRTY: ~8% straight-liners
straightline_idx = rng.choice(n, int(n*0.08), replace=False)
for i in straightline_idx:
    fill_val = rng.choice([3, 4])
    for col in data:
        if col.startswith("q") and isinstance(data[col][i], (int, np.integer)):
            data[col][i] = fill_val

# DIRTY: duplicate respondent IDs
emp_ids = list(data["employee_id"])
dup_emp_idx = rng.choice(n, 60, replace=False)
for i in dup_emp_idx[:30]:
    emp_ids[i] = emp_ids[dup_emp_idx[30 + rng.integers(0, 30)]]
data["employee_id"] = emp_ids

survey_dates = rand_dates("2024-01-01", "2024-02-28", n)
# DIRTY: 40% of responses in 2-hour window
cluster_mask = rng.random(n) < 0.40
survey_dates_list = []
for i in range(n):
    if cluster_mask[i]:
        survey_dates_list.append("2024-01-15 10:00:00")
    else:
        survey_dates_list.append(str(survey_dates[i])[:10])
survey_dates_dirty = np.array(survey_dates_list, dtype=object)

data["department"] = dept_arr
data["tenure_years"] = np.clip(rng.exponential(4, n), 0, 35).round(1)
data["age_group"] = rng.choice(["18-24","25-34","35-44","45-54","55+"], n)
data["work_location"] = rng.choice(["Remote","Hybrid","On-site"], n, p=[0.35,0.40,0.25])
data["survey_date"] = survey_dates_dirty

df_survey = pd.DataFrame(data)
save_csv(df_survey, "employee_engagement_survey_dirty.csv")

# ── 12. GEOSPATIAL LOCATION DATA ─────────────────────────────────────────────
print("12. Geospatial Location Data")
n = 5000
# NYC bounding box roughly: lat 40.48–40.92, lon -74.26–-73.68
lat_pickup  = rng.uniform(40.48, 40.92, n)
lon_pickup  = rng.uniform(-74.26, -73.68, n)
lat_dropoff = lat_pickup + rng.normal(0, 0.05, n)
lon_dropoff = lon_pickup + rng.normal(0, 0.05, n)

# DIRTY: ~2% null island (0,0) or ocean coords
null_island_idx = rng.choice(n, int(n*0.02), replace=False)
lat_pickup[null_island_idx] = rng.choice([0.0, 51.5, -33.9], len(null_island_idx))
lon_pickup[null_island_idx] = rng.choice([0.0, -0.12, 151.2], len(null_island_idx))

# DIRTY: ~150 lat/lon swapped
swap_idx = rng.choice(n, 150, replace=False)
lat_pickup[swap_idx], lon_pickup[swap_idx] = lon_pickup[swap_idx].copy(), lat_pickup[swap_idx].copy()

distance_mi = np.clip(rng.exponential(3.5, n), 0.1, 40).round(2)
duration_min = (distance_mi * rng.uniform(3, 8, n) + rng.uniform(2, 10, n)).clip(1, 120).round(1)

# DIRTY: ~4% fare < $2.50 (NYC base rate)
base_fare = 2.50 + distance_mi * 1.75 + duration_min * 0.35
fare_dirty = base_fare.copy().astype(object)
bad_fare_idx = rng.choice(n, int(n*0.04), replace=False)
for i in bad_fare_idx:
    fare_dirty[i] = round(rng.uniform(0.01, 2.49), 2)

# DIRTY: ~300 trips with distance=0 but duration>10
zero_dist_idx = rng.choice(n, 300, replace=False)
distance_dirty = distance_mi.copy().astype(object)
for i in zero_dist_idx:
    distance_dirty[i] = 0
    duration_min[i] = rng.uniform(10, 45)

# DIRTY: speed > 200 mph
speed_idx = rng.choice(n, int(n*0.005), replace=False)
distance_dirty2 = np.array(distance_dirty, dtype=object)
for i in speed_idx:
    distance_dirty2[i] = float(distance_dirty2[i] if distance_dirty2[i] else 0) * 50

# DIRTY: ~50 duplicate trip IDs
trip_ids = [f"TRIP_{i:07d}" for i in range(n)]
dup_trip_idx = rng.choice(n, 50, replace=False)
for i in dup_trip_idx[:25]:
    trip_ids[i] = trip_ids[dup_trip_idx[25 + rng.integers(0, 25)]]

# DIRTY: ~20 future pickup times
pickup_ts = rand_dates("2024-01-01", "2024-06-30", n)
pickup_list = list(pickup_ts.strftime("%Y-%m-%d"))
future_pickup_idx = rng.choice(n, 20, replace=False)
for i in future_pickup_idx:
    pickup_list[i] = f"2027-{int(rng.integers(1,12)):02d}-{int(rng.integers(1,28)):02d}"
pickup_dirty = np.array(pickup_list, dtype=object)

dropoff_ts = pickup_ts + pd.to_timedelta(duration_min.astype(float), unit="m")

df_geo = pd.DataFrame({
    "trip_id": trip_ids,
    "pickup_datetime": pickup_dirty,
    "dropoff_datetime": dropoff_ts.astype(str),
    "pickup_lat": lat_pickup.round(6),
    "pickup_lng": lon_pickup.round(6),
    "dropoff_lat": lat_dropoff.clip(40.2, 41.2).round(6),
    "dropoff_lng": lon_dropoff.clip(-74.5, -73.4).round(6),
    "distance_mi": distance_dirty2,
    "duration_min": duration_min,
    "fare_usd": fare_dirty,
    "driver_rating": np.where(rng.random(n) < 0.08, None,
                               np.clip(rng.normal(4.7, 0.4, n), 1, 5).round(1)),
    "payment_method": rng.choice(["credit_card","cash","app_pay","venmo"], n, p=[0.55,0.25,0.15,0.05]),
    "surge_multiplier": rng.choice([1.0,1.25,1.5,1.75,2.0,2.5], n, p=[0.65,0.12,0.10,0.06,0.04,0.03]),
    "city": rng.choice(["New York","Newark","Jersey City","Brooklyn","Queens"], n),
})
save_csv(df_geo, "geospatial_location_dirty.csv")

# ── 13. A/B TEST RESULTS ─────────────────────────────────────────────────────
print("13. A/B Test Results")
# DIRTY: Sample Ratio Mismatch — 5200 control, 4200 treatment (not 50/50)
n_control = 5200
n_treatment = 4200
n_total = n_control + n_treatment

user_ids_ab = list(range(1000000, 1000000 + n_total))
groups_ab = ["control"] * n_control + ["treatment"] * n_treatment
conv_control = rng.random(n_control) < 0.105
conv_treatment = rng.random(n_treatment) < 0.118
converted_ab = np.concatenate([conv_control, conv_treatment])

session_starts = rand_dates("2024-03-01", "2024-04-30", n_total)
session_dur = rng.integers(30, 3600, n_total)
session_ends = session_starts + pd.to_timedelta(session_dur, unit="s")

revenue = np.where(converted_ab,
                    rng.lognormal(3.5, 1.2, n_total).round(2),
                    0.0)

# DIRTY: ~40 non-converters with revenue > 0
non_conv_idx = np.where(~converted_ab)[0]
bad_rev_idx = rng.choice(non_conv_idx, 40, replace=False)
revenue_dirty = revenue.astype(object).copy()
for i in bad_rev_idx:
    revenue_dirty[i] = round(rng.uniform(1, 100), 2)

# DIRTY: ~150 users in both groups (bucketing collision)
collision_user_ids = rng.choice(user_ids_ab[:n_control], 150, replace=False)
collision_rows = pd.DataFrame({
    "user_id": collision_user_ids,
    "experiment_id": "EXP_2024_03",
    "variant": "treatment",
    "device_type": rng.choice(["mobile","desktop","tablet"], 150),
    "country": rng.choice(["US","CA","GB","AU","DE"], 150),
    "session_start": rng.choice(session_starts, 150).astype(str),
    "session_end": rng.choice(session_ends, 150).astype(str),
    "page_views": rng.integers(1, 15, 150),
    "clicks": rng.integers(0, 10, 150),
    "converted": rng.integers(0, 2, 150),
    "revenue_usd": rng.uniform(0, 100, 150).round(2),
    "days_since_signup": rng.integers(0, 365, 150),
    "is_new_user": rng.choice([True, False], 150),
    "channel": rng.choice(["organic","paid","email","referral"], 150),
    "browser": rng.choice(["Chrome","Safari","Firefox","Edge"], 150),
})

# DIRTY: ~300 pre-experiment contaminated users
exp_start = pd.Timestamp("2024-03-01")
pre_exp_idx = rng.choice(n_total, 300, replace=False)
session_starts_list = list(session_starts.strftime("%Y-%m-%d"))
for i in pre_exp_idx:
    session_starts_list[i] = (exp_start - pd.Timedelta(days=int(rng.integers(1, 14)))).strftime("%Y-%m-%d")
session_starts_dirty = np.array(session_starts_list, dtype=object)

# DIRTY: ~80 conversion events after session end
conv_idx = np.where(converted_ab)[0]
post_session_idx = rng.choice(conv_idx, min(80, len(conv_idx)), replace=False)
session_ends_list = list(session_ends.strftime("%Y-%m-%d %H:%M:%S"))
for i in post_session_idx:
    session_ends_list[i] = (session_starts[i] - pd.Timedelta(seconds=int(rng.integers(1, 600)))).strftime("%Y-%m-%d %H:%M:%S")

# DIRTY: ~200 bots (conversion in <3 seconds)
bot_idx = rng.choice(n_total, 200, replace=False)
for i in bot_idx:
    session_ends_list[i] = (session_starts[i] + pd.Timedelta(seconds=int(rng.integers(1, 3)))).strftime("%Y-%m-%d %H:%M:%S")
session_ends_dirty = np.array(session_ends_list, dtype=object)

df_ab_main = pd.DataFrame({
    "user_id": user_ids_ab,
    "experiment_id": "EXP_2024_03",
    "variant": groups_ab,
    "device_type": rng.choice(["mobile","desktop","tablet"], n_total, p=[0.55,0.38,0.07]),
    "country": rng.choice(["US","CA","GB","AU","DE"], n_total, p=[0.75,0.08,0.07,0.05,0.05]),
    "session_start": session_starts_dirty,
    "session_end": session_ends_dirty,
    "page_views": rng.integers(1, 20, n_total),
    "clicks": rng.integers(0, 15, n_total),
    "converted": converted_ab.astype(int),
    "revenue_usd": revenue_dirty,
    "days_since_signup": rng.integers(0, 730, n_total),
    "is_new_user": rng.choice([True, False, "True", "False"], n_total, p=[0.35,0.35,0.15,0.15]),
    "channel": rng.choice(["organic","paid_search","paid_social","email","referral","direct"], n_total),
    "browser": rng.choice(["Chrome","Safari","Firefox","Edge","Other"], n_total),
})
df_ab_final = pd.concat([df_ab_main, collision_rows], ignore_index=True)
save_csv(df_ab_final, "ab_test_results_dirty.csv")

# ── 14. MOVIE RATINGS (RecSys) ───────────────────────────────────────────────
print("14. Movie Ratings (RecSys)")
n = 5000
movie_genres = ["Action","Adventure","Animation","Children","Comedy","Crime",
                 "Documentary","Drama","Fantasy","Film-Noir","Horror","Musical",
                 "Mystery","Romance","Sci-Fi","Thriller","War","Western"]
movies_rec = []
for mid in range(1, 1001):
    g_count = rng.integers(1, 5)
    genres_str = "|".join(rng.choice(movie_genres, g_count, replace=False))
    year = rng.integers(1970, 2024)
    movies_rec.append({"movieId": mid,
                        "title": f"Movie Title {mid} ({year})",
                        "genres": genres_str})
movies_rec_df = pd.DataFrame(movies_rec)

user_ids_rec = rng.integers(1, 611, n)
movie_ids_rec = rng.choice(movies_rec_df["movieId"].values, n)

# DIRTY: rating scale inconsistency — some users only whole numbers
user_whole_number = set(rng.choice(610, 200, replace=False))
ratings_rec = []
for u in user_ids_rec:
    if u in user_whole_number:
        ratings_rec.append(float(rng.choice([1, 2, 3, 4, 5])))
    else:
        ratings_rec.append(rng.choice([0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0]))
ratings_rec = np.array(ratings_rec)

# DIRTY: some ratings out of range
oob_rating_idx = rng.choice(n, 30, replace=False)
ratings_dirty_rec = ratings_rec.astype(object).copy()
for i in oob_rating_idx:
    ratings_dirty_rec[i] = rng.choice([0, 5.5, 6, 10])

# DIRTY: Unix epoch timestamps — old ones mixed with newer
ts_old  = rng.integers(789000000, 1000000000, int(n*0.3))   # 1995-2001
ts_new  = rng.integers(1400000000, 1700000000, n - int(n*0.3))  # 2014-2023
timestamps_rec = np.concatenate([ts_old, ts_new])
rng.shuffle(timestamps_rec)

# DIRTY: duplicate ratings (same user, same movie, different score)
df_rec_base = pd.DataFrame({
    "userId": user_ids_rec,
    "movieId": movie_ids_rec,
    "rating": ratings_dirty_rec,
    "timestamp": timestamps_rec,
})
df_rec_base = df_rec_base.merge(movies_rec_df, on="movieId")
dup_rec_idx = rng.choice(len(df_rec_base), 50, replace=False)
dup_rows = df_rec_base.iloc[dup_rec_idx].copy()
dup_rows["rating"] = rng.choice([1.0,2.0,3.0,4.0,5.0], 50)
df_rec = pd.concat([df_rec_base, dup_rows], ignore_index=True)
save_csv(df_rec, "movie_ratings_dirty.csv")

# ── 15. SERVER LOG FILES ────────────────────────────────────────────────────
print("15. Server Log Files")
n = 5000
endpoints = ["/","/api/users","/api/products","/api/orders","/search",
              "/login","/logout","/dashboard","/api/analytics","/health",
              "/api/v2/data","/static/main.css","/favicon.ico","/robots.txt",
              "/api/auth/token","/api/search","/profile","/settings",
              "/api/metrics","/api/reports"]
methods = rng.choice(["GET","POST","PUT","DELETE","PATCH"], n, p=[0.65,0.20,0.08,0.05,0.02])
status_codes_base = rng.choice([200,201,301,302,400,401,403,404,500,503], n,
                               p=[0.55,0.08,0.05,0.03,0.05,0.05,0.02,0.10,0.05,0.02])
endpoints_arr = rng.choice(endpoints, n)

# Realistic IPv4
def rand_ip4():
    return f"{rng.integers(1,255)}.{rng.integers(0,255)}.{rng.integers(0,255)}.{rng.integers(1,255)}"
ipv4_addrs = [rand_ip4() for _ in range(n)]

# DIRTY: mixed IPv4 and IPv6
ip_dirty = list(ipv4_addrs)
ipv6_idx = rng.choice(n, int(n*0.15), replace=False)
ipv6_examples = ["::1","2001:db8::1","::ffff:192.0.2.1","fe80::1%eth0","2001:db8:85a3::8a2e:370:7334"]
for i in ipv6_idx:
    ip_dirty[i] = rng.choice(ipv6_examples)

# DIRTY: internal IPs (~8%)
internal_idx = rng.choice(n, int(n*0.08), replace=False)
for i in internal_idx:
    ip_dirty[i] = rng.choice([
        f"10.{rng.integers(0,255)}.{rng.integers(0,255)}.{rng.integers(1,255)}",
        f"192.168.{rng.integers(0,255)}.{rng.integers(1,255)}",
        f"172.{rng.integers(16,31)}.{rng.integers(0,255)}.{rng.integers(1,255)}"
    ])

# Apache combined log format timestamps
log_start = pd.Timestamp("2024-01-01")
log_ts = [(log_start + pd.Timedelta(seconds=int(i * 17.28))).strftime("%d/%b/%Y:%H:%M:%S +0000")
           for i in range(n)]

# DIRTY: response_time in microseconds for ~30%, ms for ~70%
response_us = rng.lognormal(8, 1.5, n).round(0).astype(int)  # microseconds
response_dirty = response_us.astype(object).copy()
ms_idx = rng.choice(n, int(n*0.70), replace=False)
for i in ms_idx:
    response_dirty[i] = round(response_us[i] / 1000, 2)  # convert to ms, no label

# DIRTY: response_size = 0 for 200 responses on ~5%
resp_size = rng.integers(100, 50000, n).astype(object)
zero_size_idx = rng.choice(np.where(status_codes_base == 200)[0],
                             size=int(n*0.05), replace=False)
for i in zero_size_idx:
    resp_size[i] = 0

# DIRTY: status codes as strings (mix of int and string)
sc_dirty = status_codes_base.astype(object).copy()
str_sc_idx = rng.choice(n, int(n*0.30), replace=False)
for i in str_sc_idx:
    sc_dirty[i] = str(status_codes_base[i])

# DIRTY: URL-encoded paths
url_encode_idx = rng.choice(n, int(n*0.10), replace=False)
endpoints_dirty = list(endpoints_arr)
for i in url_encode_idx:
    endpoints_dirty[i] = endpoints_dirty[i].replace("/", "%2F").replace("api", "api%20")

user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) Safari/605",
                "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko Firefox/121.0",
                "curl/7.88.1","python-requests/2.31.0",
                "Googlebot/2.1 (+http://www.google.com/bot.html)",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0) Mobile Safari/604",
                "PostmanRuntime/7.36.1","Scrapy/2.11.0 (+http://scrapy.org)"]

df_logs = pd.DataFrame({
    "ip_address": ip_dirty,
    "timestamp": log_ts,
    "method": methods,
    "endpoint": endpoints_dirty,
    "status_code": sc_dirty,
    "response_size_bytes": resp_size,
    "referrer": np.where(rng.random(n) < 0.35,
                          rng.choice(["https://google.com","https://bing.com","-",""], n),
                          "-"),
    "user_agent": rng.choice(user_agents, n),
    "response_time": response_dirty,
})
save_csv(df_logs, "server_logs_dirty.csv")

print("\n✅ All 15 new dirty datasets generated!")
