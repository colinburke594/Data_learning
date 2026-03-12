"""
Synthetic Dataset Generator
Generates representative synthetic CSV/SQLite files for all Dataset Library entries.
Output: data sets/synthetic/
"""

import numpy as np
import pandas as pd
import sqlite3
import os
import random
import string
from datetime import datetime, timedelta

rng = np.random.default_rng(42)
random.seed(42)

OUT = os.path.join(os.path.dirname(__file__), "synthetic")
os.makedirs(OUT, exist_ok=True)

def save(df, name):
    path = os.path.join(OUT, name)
    df.to_csv(path, index=False)
    print(f"  saved {name} ({len(df):,} rows, {len(df.columns)} cols)")

def rand_dates(start, end, n):
    s = pd.Timestamp(start).value // 10**9
    e = pd.Timestamp(end).value // 10**9
    return pd.to_datetime(rng.integers(s, e, n), unit="s").normalize()

def rand_names_first(n):
    first = ["James","Mary","John","Patricia","Robert","Jennifer","Michael","Linda",
             "William","Barbara","David","Elizabeth","Richard","Susan","Joseph","Jessica",
             "Thomas","Sarah","Charles","Karen","Emma","Liam","Olivia","Noah","Ava","Sophia",
             "Isabella","Mia","Charlotte","Amelia","Harper","Evelyn","Abigail","Emily",
             "Madison","Sofia","Avery","Ella","Scarlett","Victoria","Aiden","Lucas","Mason",
             "Ethan","Logan","Jackson","Sebastian","Jack","Owen","Theodore","Jayden","Ryan"]
    return rng.choice(first, n)

def rand_names_last(n):
    last = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Wilson",
            "Martinez","Anderson","Taylor","Thomas","Hernandez","Moore","Martin","Jackson",
            "Thompson","White","Lopez","Lee","Gonzalez","Harris","Clark","Lewis","Robinson",
            "Walker","Perez","Hall","Young","Allen","Sanchez","Wright","King","Scott",
            "Green","Baker","Adams","Nelson","Carter","Mitchell","Perez","Roberts","Turner",
            "Phillips","Campbell","Parker","Evans","Edwards","Collins"]
    return rng.choice(last, n)

# ─── 1. TITANIC ────────────────────────────────────────────────────────────────
print("1. Titanic Passenger Data")
n = 891
pclass = rng.choice([1, 2, 3], n, p=[0.24, 0.21, 0.55])
sex = rng.choice(["male", "female"], n, p=[0.65, 0.35])
age = np.where(rng.random(n) < 0.2, np.nan,
               np.clip(rng.normal(29, 14, n), 1, 80).round(1))
sibsp = rng.choice([0,1,2,3,4,5,8], n, p=[0.68,0.23,0.05,0.02,0.01,0.005,0.005])
parch = rng.choice([0,1,2,3,4,5,6], n, p=[0.76,0.13,0.08,0.01,0.01,0.005,0.005])
fare_base = np.where(pclass==1, rng.normal(84, 78, n),
            np.where(pclass==2, rng.normal(21, 13, n),
                     rng.normal(13, 11, n)))
fare = np.clip(fare_base, 0, 512).round(4)
survived_prob = np.where(sex=="female", 0.74, 0.19)
survived_prob = np.where(pclass==1, survived_prob * 1.4, survived_prob)
survived_prob = np.clip(survived_prob, 0, 1)
survived = rng.random(n) < survived_prob

first = rand_names_first(n)
last = rand_names_last(n)
titles = np.where(sex=="female",
                  rng.choice(["Miss.", "Mrs."], n, p=[0.5, 0.5]),
                  rng.choice(["Mr.", "Dr.", "Rev."], n, p=[0.9, 0.06, 0.04]))
names = [f"{last[i]}, {titles[i]} {first[i]}" for i in range(n)]
cabin_vals = [f"{rng.choice(list('ABCDEF'))}{rng.integers(1,150)}" for _ in range(n)]
cabin = [None if rng.random() < 0.77 else cabin_vals[i] for i in range(n)]
embarked = rng.choice(["S","C","Q"], n, p=[0.72, 0.19, 0.09])
mask = rng.random(n) < 0.002
embarked = [None if mask[i] else embarked[i] for i in range(n)]

df_titanic = pd.DataFrame({
    "PassengerId": range(1, n+1),
    "Survived": survived.astype(int),
    "Pclass": pclass,
    "Name": names,
    "Sex": sex,
    "Age": age,
    "SibSp": sibsp,
    "Parch": parch,
    "Ticket": [f"{''.join(rng.choice(list(string.ascii_uppercase+string.digits), rng.integers(5,9)))}" for _ in range(n)],
    "Fare": fare,
    "Cabin": cabin,
    "Embarked": embarked
})
save(df_titanic, "titanic.csv")

# ─── 2. SUPERSTORE SALES ───────────────────────────────────────────────────────
print("2. Sample Superstore Sales")
n = 2000
categories = {"Furniture": ["Bookcases","Chairs","Furnishings","Tables"],
               "Office Supplies": ["Appliances","Art","Binders","Envelopes","Fasteners","Labels","Paper","Storage","Supplies"],
               "Technology": ["Accessories","Copiers","Machines","Phones"]}
cat_list = rng.choice(list(categories.keys()), n, p=[0.21, 0.61, 0.18])
sub_cat = [rng.choice(categories[c]) for c in cat_list]
states = ["California","New York","Texas","Pennsylvania","Washington","Illinois","Ohio","Florida","Michigan","Virginia"]
state_arr = rng.choice(states, n)
regions = {"California":"West","New York":"East","Texas":"Central","Pennsylvania":"East",
           "Washington":"West","Illinois":"Central","Ohio":"East","Florida":"South","Michigan":"Central","Virginia":"South"}
order_dates = rand_dates("2021-01-01", "2024-12-31", n)
ship_dates = order_dates + pd.to_timedelta(rng.integers(2, 8, n), unit="D")
sales_base = np.where(cat_list=="Technology", rng.lognormal(5.5, 1.2, n),
             np.where(cat_list=="Furniture", rng.lognormal(5.0, 1.1, n),
                      rng.lognormal(3.5, 1.0, n)))
discount = rng.choice([0.0, 0.1, 0.2, 0.3, 0.4, 0.5], n, p=[0.50, 0.15, 0.20, 0.08, 0.04, 0.03])
sales = (sales_base * (1 - discount)).round(2)
profit = (sales * rng.uniform(-0.1, 0.4, n)).round(2)
qty = rng.integers(1, 15, n)
first_names = rand_names_first(n)
last_names = rand_names_last(n)
customer_names = [f"{first_names[i]} {last_names[i]}" for i in range(n)]
segments = rng.choice(["Consumer","Corporate","Home Office"], n, p=[0.52, 0.31, 0.17])

df_super = pd.DataFrame({
    "Row ID": range(1, n+1),
    "Order ID": [f"CA-{d.year}-{rng.integers(100000,199999)}" for d in order_dates],
    "Order Date": order_dates.strftime("%m/%d/%Y"),
    "Ship Date": ship_dates.strftime("%m/%d/%Y"),
    "Ship Mode": rng.choice(["Second Class","Standard Class","First Class","Same Day"], n, p=[0.31,0.60,0.07,0.02]),
    "Customer ID": [f"{''.join(rng.choice(list(string.ascii_uppercase),2))}-{rng.integers(10000,99999)}" for _ in range(n)],
    "Customer Name": customer_names,
    "Segment": segments,
    "Country": "United States",
    "City": rng.choice(["Los Angeles","New York City","Philadelphia","San Francisco","Seattle","Chicago","Columbus","Miami","Detroit","Richmond"], n),
    "State": state_arr,
    "Postal Code": rng.integers(10000, 99999, n),
    "Region": [regions[s] for s in state_arr],
    "Product ID": [f"{cat_list[i][:3].upper()}-{rng.integers(100000,999999)}" for i in range(n)],
    "Category": cat_list,
    "Sub-Category": sub_cat,
    "Product Name": [f"{sub_cat[i]} Model {rng.integers(100,999)}" for i in range(n)],
    "Sales": sales,
    "Quantity": qty,
    "Discount": discount,
    "Profit": profit,
})
save(df_super, "superstore_sales.csv")

# ─── 3. IRIS ───────────────────────────────────────────────────────────────────
print("3. Iris Flower Dataset")
species_params = {
    "setosa":     {"sl": (5.0, 0.35), "sw": (3.42, 0.38), "pl": (1.46, 0.17), "pw": (0.24, 0.11)},
    "versicolor": {"sl": (5.94, 0.52), "sw": (2.77, 0.31), "pl": (4.26, 0.47), "pw": (1.33, 0.20)},
    "virginica":  {"sl": (6.59, 0.64), "sw": (2.97, 0.32), "pl": (5.55, 0.55), "pw": (2.03, 0.27)},
}
rows = []
for sp, p in species_params.items():
    for _ in range(50):
        rows.append({
            "sepal_length": round(max(4.3, rng.normal(p["sl"][0], p["sl"][1])), 1),
            "sepal_width":  round(max(2.0, rng.normal(p["sw"][0], p["sw"][1])), 1),
            "petal_length": round(max(1.0, rng.normal(p["pl"][0], p["pl"][1])), 1),
            "petal_width":  round(max(0.1, rng.normal(p["pw"][0], p["pw"][1])), 1),
            "species": sp
        })
df_iris = pd.DataFrame(rows)
save(df_iris, "iris.csv")

# ─── 4. A/B TEST ───────────────────────────────────────────────────────────────
print("4. E-Commerce A/B Test Results")
n = 5000
group = rng.choice(["control","treatment"], n)
converted = np.where(group=="control",
                     rng.random(n) < 0.121,
                     rng.random(n) < 0.127)
start_ts = pd.Timestamp("2024-01-01").value // 10**9
end_ts   = pd.Timestamp("2024-03-31").value // 10**9
timestamps = pd.to_datetime(rng.integers(start_ts, end_ts, n), unit="s")
df_ab = pd.DataFrame({
    "user_id": rng.integers(600000, 900000, n),
    "timestamp": timestamps,
    "group": group,
    "landing_page": np.where(group=="control", "old_page", "new_page"),
    "converted": converted.astype(int),
})
save(df_ab, "ab_test_results.csv")

# ─── 5. MEDICAL INSURANCE ──────────────────────────────────────────────────────
print("5. Medical Insurance Costs")
n = 1338
age_ins = rng.integers(18, 65, n)
sex_ins = rng.choice(["male","female"], n)
bmi = np.clip(rng.normal(30.7, 6.1, n), 15.5, 53.1).round(2)
children = rng.choice([0,1,2,3,4,5], n, p=[0.43,0.24,0.18,0.10,0.03,0.02])
smoker = rng.choice(["yes","no"], n, p=[0.20, 0.80])
region = rng.choice(["northeast","northwest","southeast","southwest"], n)
base_charge = 3000 + age_ins * 250 + bmi * 60 + children * 500
smoke_mult = np.where(smoker=="yes", rng.uniform(2.8, 4.2, n), 1.0)
charges = (base_charge * smoke_mult * rng.uniform(0.85, 1.15, n)).round(2)
df_ins = pd.DataFrame({
    "age": age_ins, "sex": sex_ins, "bmi": bmi, "children": children,
    "smoker": smoker, "region": region, "charges": charges
})
save(df_ins, "medical_insurance.csv")

# ─── 6. WINE QUALITY ───────────────────────────────────────────────────────────
print("6. Wine Quality Dataset")
def make_wine(n, wine_type):
    if wine_type == "red":
        fa = rng.normal(8.3, 1.7, n);  va = rng.normal(0.53, 0.18, n)
        ca = rng.normal(0.27, 0.19, n); rs = rng.normal(2.5, 1.4, n)
        cl = rng.normal(0.087, 0.047, n); fsd = rng.normal(15.9, 10.5, n)
        tsd = rng.normal(46.5, 32.9, n); dens = rng.normal(0.9967, 0.0019, n)
        ph = rng.normal(3.31, 0.15, n);  su = rng.normal(0.66, 0.17, n)
        alc = rng.normal(10.4, 1.07, n)
    else:
        fa = rng.normal(6.85, 0.84, n);  va = rng.normal(0.28, 0.10, n)
        ca = rng.normal(0.33, 0.12, n); rs = rng.normal(6.4, 5.1, n)
        cl = rng.normal(0.046, 0.022, n); fsd = rng.normal(35.3, 17.0, n)
        tsd = rng.normal(138.4, 42.5, n); dens = rng.normal(0.9940, 0.0030, n)
        ph = rng.normal(3.19, 0.15, n);  su = rng.normal(0.49, 0.11, n)
        alc = rng.normal(10.5, 1.23, n)
    quality = np.clip(np.round(rng.normal(5.8, 0.87, n)).astype(int), 3, 9)
    return pd.DataFrame({
        "fixed_acidity": fa.round(1), "volatile_acidity": va.round(2),
        "citric_acid": ca.round(2), "residual_sugar": rs.round(1),
        "chlorides": cl.round(3), "free_sulfur_dioxide": fsd.round(0).astype(int),
        "total_sulfur_dioxide": tsd.round(0).astype(int),
        "density": dens.round(4), "pH": ph.round(2), "sulphates": su.round(2),
        "alcohol": alc.round(1), "quality": quality, "type": wine_type
    })
df_wine = pd.concat([make_wine(1599, "red"), make_wine(4898, "white")], ignore_index=True)
save(df_wine, "wine_quality.csv")

# ─── 7. AMES HOUSING ───────────────────────────────────────────────────────────
print("7. Ames Housing Prices")
n = 1000
neighborhoods = ["NAmes","CollgCr","OldTown","Edwards","Somerst","Gilbert","NridgHt",
                  "Sawyer","NWAmes","SawyerW","BrkSide","Crawfor","Mitchel","NoRidge","Timber"]
nb = rng.choice(neighborhoods, n)
nb_premium = {"NridgHt": 1.4, "NoRidge": 1.35, "Timber": 1.25, "Somerst": 1.15,
              "CollgCr": 1.05, "Gilbert": 1.02, "NAmes": 1.0, "Edwards": 0.90,
              "OldTown": 0.88, "BrkSide": 0.85}
overall_qual = np.clip(rng.normal(6.1, 1.4, n), 1, 10).round(0).astype(int)
overall_cond = np.clip(rng.normal(5.6, 1.1, n), 1, 9).round(0).astype(int)
gr_liv_area = np.clip(rng.normal(1515, 525, n), 334, 5642).round(0).astype(int)
year_built = rng.integers(1872, 2010, n)
year_remod = np.maximum(year_built, rng.integers(1950, 2010, n))
lot_area = np.clip(rng.lognormal(9.1, 0.5, n), 1300, 215245).round(0).astype(int)
bedrooms = np.clip(rng.integers(1, 7, n), 1, 6)
full_bath = rng.choice([1,2,3], n, p=[0.42,0.54,0.04])
garage_cars = rng.choice([0,1,2,3], n, p=[0.06,0.22,0.64,0.08])
base_price = (overall_qual * 15000 + gr_liv_area * 75 +
              garage_cars * 8000 + full_bath * 6000 + (2010 - year_built) * -200)
price = base_price * np.array([nb_premium.get(x, 1.0) for x in nb])
price = np.clip(price * rng.uniform(0.85, 1.15, n), 34900, 755000).round(-2)
df_housing = pd.DataFrame({
    "Id": range(1, n+1), "Neighborhood": nb,
    "OverallQual": overall_qual, "OverallCond": overall_cond,
    "YearBuilt": year_built, "YearRemodAdd": year_remod,
    "GrLivArea": gr_liv_area, "LotArea": lot_area,
    "BedroomAbvGr": bedrooms, "FullBath": full_bath,
    "GarageCars": garage_cars,
    "TotalBsmtSF": np.clip(rng.normal(1057, 439, n), 0, 3000).round(0).astype(int),
    "1stFlrSF": np.clip(rng.normal(1163, 392, n), 334, 3820).round(0).astype(int),
    "MasVnrArea": np.where(rng.random(n) < 0.40, 0,
                           rng.integers(1, 1600, n)).round(0).astype(int),
    "GarageArea": (garage_cars * rng.normal(240, 60, n)).clip(0).round(0).astype(int),
    "SalePrice": price.astype(int),
})
save(df_housing, "ames_housing.csv")

# ─── 8. CREDIT CARD FRAUD ──────────────────────────────────────────────────────
print("8. Credit Card Fraud Detection")
n_legit = 1940
n_fraud = 60
def pca_features(n, fraud=False):
    if fraud:
        means = rng.uniform(-3, 3, 28)
        stds = rng.uniform(0.5, 2.5, 28)
    else:
        means = np.zeros(28)
        stds = np.ones(28)
    return rng.normal(means, stds, (n, 28))

v_legit = pca_features(n_legit, False)
v_fraud = pca_features(n_fraud, True)
amount_legit = np.clip(rng.lognormal(3.2, 1.8, n_legit), 0, 25691).round(2)
amount_fraud = np.clip(rng.lognormal(4.5, 1.5, n_fraud), 1, 5000).round(2)
time_all = np.sort(rng.uniform(0, 172792, n_legit + n_fraud))

rows_legit = {f"V{i+1}": v_legit[:, i] for i in range(28)}
rows_legit.update({"Amount": amount_legit, "Class": np.zeros(n_legit, dtype=int)})
rows_fraud = {f"V{i+1}": v_fraud[:, i] for i in range(28)}
rows_fraud.update({"Amount": amount_fraud, "Class": np.ones(n_fraud, dtype=int)})

df_legit = pd.DataFrame(rows_legit)
df_fraud_df = pd.DataFrame(rows_fraud)
df_fraud_combined = pd.concat([df_legit, df_fraud_df], ignore_index=True)
df_fraud_combined.insert(0, "Time", time_all)
for col in [f"V{i+1}" for i in range(28)]:
    df_fraud_combined[col] = df_fraud_combined[col].round(6)
df_fraud_combined = df_fraud_combined.sample(frac=1, random_state=42).reset_index(drop=True)
save(df_fraud_combined, "credit_card_fraud.csv")

# ─── 9. HOURLY ENERGY CONSUMPTION ─────────────────────────────────────────────
print("9. Hourly Energy Consumption")
dates = pd.date_range("2023-01-01", periods=8760, freq="h")
hour = dates.hour
dow = dates.dayofweek
month = dates.month

# Realistic demand: higher in summer/winter, lower in spring/fall, peak hours morning/evening
seasonal = 1 + 0.18 * np.cos((month - 1) * 2 * np.pi / 12 - np.pi)
daily = 1 + 0.12 * np.sin((hour - 6) * 2 * np.pi / 24)
peak_morning = np.exp(-0.5 * ((hour - 8.5) / 2) ** 2) * 0.08
peak_evening = np.exp(-0.5 * ((hour - 18.5) / 1.8) ** 2) * 0.12
weekend_adj = np.where(dow >= 5, 0.91, 1.0)
base_mw = 13500
mw = (base_mw * seasonal * (daily + peak_morning + peak_evening) *
      weekend_adj * rng.uniform(0.97, 1.03, 8760)).round(0)

df_energy = pd.DataFrame({"Datetime": dates.strftime("%Y-%m-%d %H:%M:%S"), "AEP_MW": mw})
save(df_energy, "hourly_energy.csv")

# ─── 10. MOVIELENS ─────────────────────────────────────────────────────────────
print("10. MovieLens Ratings")
genres_list = ["Action","Adventure","Animation","Comedy","Crime","Documentary",
               "Drama","Fantasy","Horror","Musical","Mystery","Romance",
               "Sci-Fi","Thriller","Western"]
movies = []
for mid in range(1, 501):
    genre_count = rng.integers(1, 4)
    g = "|".join(rng.choice(genres_list, genre_count, replace=False))
    year = rng.integers(1980, 2023)
    title_words = rng.choice(["The","Dark","Last","First","Lost","Hidden","Silent",
                               "Red","Blue","Night","Day","Final","Rising","Fallen",
                               "Secret","Shadow","Fire","Ice","Storm","Wild"], 2)
    movies.append({"movie_id": mid, "title": f"{' '.join(title_words)} ({year})", "genres": g})
movies_df = pd.DataFrame(movies)

n_ratings = 3000
user_ids = rng.integers(1, 201, n_ratings)
movie_ids = rng.choice(movies_df["movie_id"].values, n_ratings)
ratings = rng.choice([0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0], n_ratings,
                     p=[0.01,0.02,0.03,0.06,0.08,0.15,0.18,0.24,0.14,0.09])
ts_start = int(pd.Timestamp("2015-01-01").timestamp())
ts_end   = int(pd.Timestamp("2024-01-01").timestamp())
timestamps_ml = rng.integers(ts_start, ts_end, n_ratings)

df_ml = pd.DataFrame({"userId": user_ids, "movieId": movie_ids, "rating": ratings, "timestamp": timestamps_ml})
df_ml = df_ml.merge(movies_df, left_on="movieId", right_on="movie_id").drop("movie_id", axis=1)
save(df_ml, "movielens_ratings.csv")

# ─── 11. GAPMINDER ─────────────────────────────────────────────────────────────
print("11. Gapminder World Data")
countries_by_continent = {
    "Africa": ["Algeria","Angola","Benin","Botswana","Burkina Faso","Burundi","Cameroon",
               "Central African Republic","Chad","Congo","Egypt","Ethiopia","Ghana","Guinea",
               "Kenya","Madagascar","Malawi","Mali","Mauritania","Morocco","Mozambique",
               "Namibia","Niger","Nigeria","Rwanda","Senegal","Sierra Leone","Somalia",
               "South Africa","Sudan","Tanzania","Togo","Tunisia","Uganda","Zambia","Zimbabwe"],
    "Americas": ["Argentina","Bolivia","Brazil","Canada","Chile","Colombia","Costa Rica","Cuba",
                 "Dominican Republic","Ecuador","El Salvador","Guatemala","Haiti","Honduras",
                 "Jamaica","Mexico","Nicaragua","Panama","Paraguay","Peru","Puerto Rico",
                 "Trinidad and Tobago","United States","Uruguay","Venezuela"],
    "Asia": ["Afghanistan","Bangladesh","Cambodia","China","Hong Kong","India","Indonesia",
             "Iran","Iraq","Israel","Japan","Jordan","Korea","Kuwait","Lebanon","Malaysia",
             "Mongolia","Myanmar","Nepal","Oman","Pakistan","Philippines","Saudi Arabia",
             "Singapore","Sri Lanka","Syria","Taiwan","Thailand","Vietnam","Yemen"],
    "Europe": ["Albania","Austria","Belgium","Bosnia","Bulgaria","Croatia","Czech Republic",
               "Denmark","Finland","France","Germany","Greece","Hungary","Iceland","Ireland",
               "Italy","Netherlands","Norway","Poland","Portugal","Romania","Serbia",
               "Slovakia","Slovenia","Spain","Sweden","Switzerland","Turkey","United Kingdom"],
    "Oceania": ["Australia","New Zealand","Papua New Guinea","Fiji"]
}
years = list(range(1952, 2008, 5))
gapminder_rows = []
for continent, country_list in countries_by_continent.items():
    for country in country_list:
        if continent == "Africa":
            le0, le_gain = rng.uniform(35, 45), rng.uniform(0.4, 0.8)
            pop0 = rng.integers(500000, 20000000)
            gdp0 = rng.uniform(300, 1200)
        elif continent == "Americas":
            le0, le_gain = rng.uniform(45, 65), rng.uniform(0.2, 0.5)
            pop0 = rng.integers(1000000, 50000000)
            gdp0 = rng.uniform(1500, 8000)
        elif continent == "Asia":
            le0, le_gain = rng.uniform(40, 60), rng.uniform(0.3, 0.7)
            pop0 = rng.integers(500000, 200000000)
            gdp0 = rng.uniform(500, 5000)
        elif continent == "Europe":
            le0, le_gain = rng.uniform(60, 70), rng.uniform(0.1, 0.3)
            pop0 = rng.integers(500000, 80000000)
            gdp0 = rng.uniform(4000, 15000)
        else:
            le0, le_gain = rng.uniform(65, 72), rng.uniform(0.05, 0.2)
            pop0 = rng.integers(100000, 20000000)
            gdp0 = rng.uniform(8000, 20000)
        for i, year in enumerate(years):
            pop_growth = rng.uniform(1.01, 1.03) ** (i * 5)
            gdp_growth = rng.uniform(1.005, 1.04) ** (i * 5)
            noise = rng.uniform(0.97, 1.03)
            gapminder_rows.append({
                "country": country,
                "continent": continent,
                "year": year,
                "lifeExp": round(min(82, le0 + le_gain * i * 5 + rng.normal(0, 0.5)), 2),
                "pop": int(pop0 * pop_growth * noise),
                "gdpPercap": round(gdp0 * gdp_growth * noise, 2)
            })
df_gap = pd.DataFrame(gapminder_rows)
save(df_gap, "gapminder.csv")

# ─── 12. SPOTIFY TRACKS ────────────────────────────────────────────────────────
print("12. Spotify Tracks & Features")
n = 2000
spotify_genres = ["pop","rock","hip-hop","r&b","electronic","indie","country","jazz",
                  "classical","latin","metal","folk","soul","reggae","punk","blues"]
genre_arr = rng.choice(spotify_genres, n)
genre_audio = {
    "pop":       {"dance":0.72,"energy":0.65,"valence":0.60,"tempo":118},
    "rock":      {"dance":0.52,"energy":0.82,"valence":0.45,"tempo":128},
    "hip-hop":   {"dance":0.80,"energy":0.70,"valence":0.55,"tempo":95},
    "r&b":       {"dance":0.75,"energy":0.58,"valence":0.62,"tempo":105},
    "electronic":{"dance":0.78,"energy":0.88,"valence":0.50,"tempo":128},
    "indie":     {"dance":0.58,"energy":0.60,"valence":0.52,"tempo":112},
    "country":   {"dance":0.62,"energy":0.70,"valence":0.70,"tempo":120},
    "jazz":      {"dance":0.55,"energy":0.40,"valence":0.65,"tempo":108},
    "classical": {"dance":0.25,"energy":0.25,"valence":0.45,"tempo":95},
    "latin":     {"dance":0.80,"energy":0.75,"valence":0.75,"tempo":110},
    "metal":     {"dance":0.38,"energy":0.95,"valence":0.30,"tempo":142},
    "folk":      {"dance":0.48,"energy":0.42,"valence":0.58,"tempo":108},
    "soul":      {"dance":0.68,"energy":0.55,"valence":0.68,"tempo":100},
    "reggae":    {"dance":0.72,"energy":0.62,"valence":0.72,"tempo":95},
    "punk":      {"dance":0.55,"energy":0.90,"valence":0.40,"tempo":160},
    "blues":     {"dance":0.55,"energy":0.50,"valence":0.48,"tempo":100},
}
adj = ["Dark","Electric","Golden","Silent","Broken","Wild","Lost","Neon","Empty","Blue",
       "Midnight","Summer","Winter","Rainy","Lonely","Burning","Frozen","Falling","Rising","Velvet"]
nouns = ["Night","Heart","Fire","Rain","Dream","Soul","Road","Sky","Love","Wave",
         "Shadow","Light","Storm","Wind","Memory","Echo","Star","Moon","Sun","City"]
track_names = [f"{rng.choice(adj)} {rng.choice(nouns)}" for _ in range(n)]
artist_first = rand_names_first(n)
artist_last = rand_names_last(n)

def audio_feat(genre_arr, key, spread=0.12):
    base = np.array([genre_audio[g][key] for g in genre_arr])
    return np.clip(base + rng.normal(0, spread, len(genre_arr)), 0, 1).round(3)

df_spot = pd.DataFrame({
    "track_id": [f"{''.join(rng.choice(list(string.ascii_letters+string.digits), 22))}" for _ in range(n)],
    "track_name": track_names,
    "artist_name": [f"{artist_first[i]} {artist_last[i]}" for i in range(n)],
    "popularity": np.clip(rng.normal(42, 25, n), 0, 100).round(0).astype(int),
    "duration_ms": rng.integers(120000, 360000, n),
    "explicit": rng.choice([True, False], n, p=[0.22, 0.78]),
    "danceability": audio_feat(genre_arr, "dance"),
    "energy": audio_feat(genre_arr, "energy"),
    "key": rng.integers(0, 12, n),
    "loudness": np.clip(rng.normal(-7.5, 4.5, n), -35, 1.5).round(3),
    "mode": rng.choice([0, 1], n, p=[0.35, 0.65]),
    "speechiness": np.clip(rng.exponential(0.06, n), 0, 0.96).round(3),
    "acousticness": np.clip(rng.beta(1.5, 4, n), 0, 1).round(3),
    "instrumentalness": np.clip(rng.beta(0.5, 8, n), 0, 1).round(3),
    "liveness": np.clip(rng.normal(0.19, 0.15, n), 0, 0.98).round(3),
    "valence": audio_feat(genre_arr, "valence"),
    "tempo": np.clip(np.array([genre_audio[g]["tempo"] for g in genre_arr]) +
                     rng.normal(0, 12, n), 50, 220).round(3),
    "time_signature": rng.choice([3, 4, 5], n, p=[0.08, 0.88, 0.04]),
    "genre": genre_arr
})
save(df_spot, "spotify_tracks.csv")

# ─── 13. NYC TAXI TRIPS ────────────────────────────────────────────────────────
print("13. NYC Yellow Taxi Trips")
n = 2000
pickup_ts = rand_dates("2023-01-01", "2023-12-31", n)
duration_min = rng.lognormal(2.5, 0.8, n).clip(1, 120)
dropoff_ts = pickup_ts + pd.to_timedelta((duration_min * 60).round(0).astype(int), unit="s")

nyc_lat_range = (40.63, 40.85)
nyc_lon_range = (-74.02, -73.75)
pickup_lat = rng.uniform(*nyc_lat_range, n).round(6)
pickup_lon = rng.uniform(*nyc_lon_range, n).round(6)
dropoff_lat = (pickup_lat + rng.normal(0, 0.03, n)).clip(*nyc_lat_range).round(6)
dropoff_lon = (pickup_lon + rng.normal(0, 0.03, n)).clip(*nyc_lon_range).round(6)
trip_dist = (np.sqrt((dropoff_lat - pickup_lat)**2 + (dropoff_lon - pickup_lon)**2) * 69).round(2)
fare = (2.5 + trip_dist * 2.5 + duration_min * 0.5).round(2)
tip = np.where(rng.random(n) < 0.65, (fare * rng.uniform(0.1, 0.3, n)).round(2), 0.0)
tolls = np.where(rng.random(n) < 0.08, rng.choice([6.55, 9.0, 13.0], n), 0.0)
total = (fare + tip + tolls + 0.5 + 0.5).round(2)

df_taxi = pd.DataFrame({
    "VendorID": rng.choice([1, 2], n),
    "tpep_pickup_datetime": pickup_ts,
    "tpep_dropoff_datetime": dropoff_ts,
    "passenger_count": rng.choice([1,2,3,4,5,6], n, p=[0.70,0.15,0.06,0.04,0.03,0.02]),
    "trip_distance": trip_dist,
    "pickup_longitude": pickup_lon, "pickup_latitude": pickup_lat,
    "RatecodeID": rng.choice([1,2,3,4,5,6], n, p=[0.91,0.04,0.01,0.01,0.02,0.01]),
    "store_and_fwd_flag": rng.choice(["N","Y"], n, p=[0.99, 0.01]),
    "dropoff_longitude": dropoff_lon, "dropoff_latitude": dropoff_lat,
    "payment_type": rng.choice([1,2,3,4], n, p=[0.68,0.29,0.01,0.02]),
    "fare_amount": fare, "extra": 0.5, "mta_tax": 0.5,
    "tip_amount": tip, "tolls_amount": tolls, "total_amount": total,
})
save(df_taxi, "nyc_taxi_trips.csv")

# ─── 14. IMDB REVIEWS ─────────────────────────────────────────────────────────
print("14. IMDB Movie Reviews")
positive_phrases = [
    "A masterpiece of modern cinema.", "Absolutely brilliant performances throughout.",
    "This film left me speechless — deeply moving.", "One of the best movies I have seen in years.",
    "The direction and cinematography are stunning.", "A truly remarkable and unforgettable experience.",
    "The cast delivers career-defining work.", "Beautifully written with complex, real characters.",
    "A gripping story that keeps you invested from start to finish.",
    "I was on the edge of my seat the entire time.", "Exceptional storytelling and production design.",
    "This movie exceeded every expectation I had.", "The chemistry between the leads is electric.",
    "A perfect blend of humor and heart.", "Visually spectacular and emotionally resonant.",
    "The score perfectly complements every scene.", "Highly recommend to anyone who loves great films.",
    "Rewatchable from start to finish.", "A triumph of independent filmmaking.",
    "This director continues to push boundaries in the best possible way.",
]
negative_phrases = [
    "Completely disappointing and forgettable.", "The plot makes absolutely no sense.",
    "I walked out after the first act.", "Two hours I will never get back.",
    "The acting is painfully wooden throughout.", "A recycled story with nothing new to offer.",
    "Special effects cannot save this shallow script.", "The pacing is unbearably slow.",
    "None of the characters are remotely likable.", "A massive step down from the director's previous work.",
    "This movie is all style and zero substance.", "The dialogue is cringe-worthy and unnatural.",
    "A shameless cash grab with no creative vision.", "Disappointing on every level.",
    "The ending makes the entire viewing experience feel pointless.",
    "I expected so much more given the talent involved.", "Avoid this one at all costs.",
    "A tiresome, predictable mess from beginning to end.",
    "The script is riddled with plot holes and lazy writing.",
    "This was a chore to sit through.",
]
reviews, sentiments = [], []
for i in range(1000):
    pos = i < 500
    base_phrases = positive_phrases if pos else negative_phrases
    n_sent = rng.integers(2, 5)
    review = " ".join(rng.choice(base_phrases, n_sent, replace=True))
    reviews.append(review)
    sentiments.append("positive" if pos else "negative")

df_imdb = pd.DataFrame({"review": reviews, "sentiment": sentiments})
df_imdb = df_imdb.sample(frac=1, random_state=42).reset_index(drop=True)
save(df_imdb, "imdb_reviews.csv")

# ─── 15. ARXIV PAPERS ─────────────────────────────────────────────────────────
print("15. arXiv Papers Dataset")
arxiv_cats = {
    "cs.LG": "Machine Learning", "cs.AI": "Artificial Intelligence",
    "cs.CV": "Computer Vision", "cs.NLP": "Natural Language Processing",
    "cs.RO": "Robotics", "stat.ML": "Statistics / Machine Learning",
    "math.ST": "Statistics Theory", "econ.ML": "Econometrics",
    "physics.comp-ph": "Computational Physics", "q-bio.BM": "Biomolecules"
}
topic_words = {
    "cs.LG":  ["learning","neural","gradient","model","training","optimization","deep","graph","attention"],
    "cs.AI":  ["reasoning","planning","knowledge","agent","logic","search","representation","inference"],
    "cs.CV":  ["image","segmentation","detection","visual","feature","convolutional","recognition"],
    "cs.NLP": ["language","text","transformer","embedding","generation","translation","sentiment"],
    "cs.RO":  ["robot","manipulation","control","motion","planning","sensor","locomotion"],
    "stat.ML":["estimation","inference","Bayesian","regression","distribution","kernel","sampling"],
    "math.ST":["theorem","convergence","bound","estimator","variance","probability","distribution"],
    "econ.ML":["causal","treatment","policy","demand","market","regression","identification"],
    "physics.comp-ph":["simulation","molecular","quantum","Monte Carlo","lattice","dynamics"],
    "q-bio.BM":["protein","sequence","folding","binding","structure","genomic","molecular"]
}
cat_list_ax = list(arxiv_cats.keys())
n_ax = 500
cat_arr = rng.choice(cat_list_ax, n_ax)
arxiv_rows = []
for i, cat in enumerate(cat_arr):
    words = topic_words[cat]
    w1, w2 = rng.choice(words, 2, replace=False)
    title = f"A {rng.choice(['Novel','Robust','Scalable','Unified','Efficient','Deep','Hierarchical','Adaptive'])} Approach to {w1.title()} {rng.choice(['via','using','with','through'])} {w2.title()} {rng.choice(['Networks','Models','Methods','Frameworks','Representations','Algorithms'])}"
    year = rng.integers(2018, 2025)
    month = rng.integers(1, 13)
    abstract = (f"We propose a new method for {w1} using {w2}-based {rng.choice(['techniques','approaches','frameworks'])}. "
                f"Our approach achieves state-of-the-art results on {rng.integers(2,6)} benchmark datasets. "
                f"Experiments demonstrate a {rng.integers(2,25)}% improvement over prior methods.")
    n_authors = rng.integers(2, 7)
    authors = ", ".join([f"{rand_names_first(1)[0]} {rand_names_last(1)[0]}" for _ in range(n_authors)])
    arxiv_rows.append({
        "arxiv_id": f"{year}.{rng.integers(10000,99999):05d}",
        "title": title,
        "abstract": abstract,
        "primary_category": cat,
        "category_name": arxiv_cats[cat],
        "authors": authors,
        "published": f"{year}-{month:02d}-{rng.integers(1,29):02d}",
        "n_citations": int(rng.lognormal(2.5, 2.0))
    })
df_arxiv = pd.DataFrame(arxiv_rows)
save(df_arxiv, "arxiv_papers.csv")

# ─── 16. OLIST BRAZILIAN E-COMMERCE ───────────────────────────────────────────
print("16. Brazilian E-Commerce (Olist)")
olist_dir = os.path.join(OUT, "olist")
os.makedirs(olist_dir, exist_ok=True)

n_customers = 800
n_sellers = 100
n_orders = 1000
n_products = 200

# customers
customer_ids = [f"CUST{i:06d}" for i in range(n_customers)]
br_cities = ["São Paulo","Rio de Janeiro","Belo Horizonte","Brasília","Salvador",
             "Fortaleza","Curitiba","Manaus","Recife","Porto Alegre"]
br_states = ["SP","RJ","MG","DF","BA","CE","PR","AM","PE","RS"]
df_customers = pd.DataFrame({
    "customer_id": customer_ids,
    "customer_unique_id": [f"UNIQ{i:06d}" for i in range(n_customers)],
    "customer_zip_code_prefix": rng.integers(10000, 99999, n_customers),
    "customer_city": rng.choice(br_cities, n_customers),
    "customer_state": rng.choice(br_states, n_customers),
})
df_customers.to_csv(os.path.join(olist_dir, "olist_customers.csv"), index=False)

# sellers
seller_ids = [f"SELL{i:05d}" for i in range(n_sellers)]
df_sellers = pd.DataFrame({
    "seller_id": seller_ids,
    "seller_zip_code_prefix": rng.integers(10000, 99999, n_sellers),
    "seller_city": rng.choice(br_cities, n_sellers),
    "seller_state": rng.choice(br_states, n_sellers),
})
df_sellers.to_csv(os.path.join(olist_dir, "olist_sellers.csv"), index=False)

# products
product_cats = ["electronics","furniture","clothing","books","beauty","sports",
                "garden","toys","food","health","automotive","art"]
product_ids = [f"PROD{i:05d}" for i in range(n_products)]
df_products = pd.DataFrame({
    "product_id": product_ids,
    "product_category_name": rng.choice(product_cats, n_products),
    "product_name_length": rng.integers(20, 80, n_products),
    "product_description_length": rng.integers(100, 1000, n_products),
    "product_photos_qty": rng.integers(1, 6, n_products),
    "product_weight_g": rng.integers(100, 5000, n_products),
    "product_length_cm": rng.integers(10, 80, n_products),
    "product_height_cm": rng.integers(5, 50, n_products),
    "product_width_cm": rng.integers(10, 60, n_products),
})
df_products.to_csv(os.path.join(olist_dir, "olist_products.csv"), index=False)

# orders
order_ids = [f"ORD{i:07d}" for i in range(n_orders)]
order_dates_ol = rand_dates("2017-01-01", "2018-08-31", n_orders)
approved_dates = order_dates_ol + pd.to_timedelta(rng.integers(0, 2, n_orders), unit="D")
delivered_carrier = approved_dates + pd.to_timedelta(rng.integers(1, 5, n_orders), unit="D")
delivered_customer = delivered_carrier + pd.to_timedelta(rng.integers(3, 15, n_orders), unit="D")
estimated_delivery = order_dates_ol + pd.to_timedelta(rng.integers(10, 30, n_orders), unit="D")
order_status = rng.choice(["delivered","shipped","canceled","invoiced"], n_orders,
                           p=[0.86, 0.07, 0.04, 0.03])
df_orders = pd.DataFrame({
    "order_id": order_ids,
    "customer_id": rng.choice(customer_ids, n_orders),
    "order_status": order_status,
    "order_purchase_timestamp": order_dates_ol,
    "order_approved_at": approved_dates,
    "order_delivered_carrier_date": delivered_carrier,
    "order_delivered_customer_date": delivered_customer,
    "order_estimated_delivery_date": estimated_delivery,
})
df_orders.to_csv(os.path.join(olist_dir, "olist_orders.csv"), index=False)

# order items
n_items = int(n_orders * 1.35)
item_order_ids = rng.choice(order_ids, n_items)
df_order_items = pd.DataFrame({
    "order_id": item_order_ids,
    "order_item_id": rng.integers(1, 4, n_items),
    "product_id": rng.choice(product_ids, n_items),
    "seller_id": rng.choice(seller_ids, n_items),
    "shipping_limit_date": (rand_dates("2017-01-10", "2018-09-10", n_items)),
    "price": rng.lognormal(3.8, 0.9, n_items).round(2),
    "freight_value": rng.lognormal(2.5, 0.5, n_items).round(2),
})
df_order_items.to_csv(os.path.join(olist_dir, "olist_order_items.csv"), index=False)

# payments
df_payments = pd.DataFrame({
    "order_id": rng.choice(order_ids, n_orders),
    "payment_sequential": rng.choice([1,2], n_orders, p=[0.92,0.08]),
    "payment_type": rng.choice(["credit_card","boleto","voucher","debit_card"], n_orders,
                                p=[0.74,0.19,0.05,0.02]),
    "payment_installments": rng.choice([1,2,3,6,10,12], n_orders,
                                        p=[0.38,0.15,0.15,0.15,0.09,0.08]),
    "payment_value": rng.lognormal(4.5, 0.9, n_orders).round(2),
})
df_payments.to_csv(os.path.join(olist_dir, "olist_order_payments.csv"), index=False)

# reviews
review_texts = ["Great product!", "Very satisfied.", "Arrived on time.",
                "Exceeded expectations.", "Decent quality.", "Average product.",
                "A bit disappointing.", "Not what I expected.", "Poor quality.",
                "Would not buy again."]
df_reviews = pd.DataFrame({
    "review_id": [f"REV{i:07d}" for i in range(n_orders)],
    "order_id": order_ids,
    "review_score": rng.choice([1,2,3,4,5], n_orders, p=[0.05,0.06,0.12,0.26,0.51]),
    "review_comment_title": rng.choice(["","Great","OK","Bad","Excellent","Poor","Fine"], n_orders,
                                        p=[0.55,0.15,0.10,0.08,0.06,0.03,0.03]),
    "review_comment_message": rng.choice(review_texts + [""], n_orders),
    "review_creation_date": rand_dates("2017-01-15", "2018-09-30", n_orders),
    "review_answer_timestamp": rand_dates("2017-01-20", "2018-10-10", n_orders),
})
df_reviews.to_csv(os.path.join(olist_dir, "olist_order_reviews.csv"), index=False)

# geolocation
n_geo = 300
df_geo = pd.DataFrame({
    "geolocation_zip_code_prefix": rng.integers(10000, 99999, n_geo),
    "geolocation_lat": rng.uniform(-33.9, 5.3, n_geo).round(6),
    "geolocation_lng": rng.uniform(-73.1, -34.8, n_geo).round(6),
    "geolocation_city": rng.choice(br_cities, n_geo),
    "geolocation_state": rng.choice(br_states, n_geo),
})
df_geo.to_csv(os.path.join(olist_dir, "olist_geolocation.csv"), index=False)
print(f"  saved olist/ (7 tables)")

# ─── 17. SAAS METRICS ─────────────────────────────────────────────────────────
print("17. SaaS Revenue Metrics")
months = pd.date_range("2021-01-01", periods=48, freq="MS")
mrr = 25000.0
customers = 180
rows_saas = []
for m in months:
    growth_rate = rng.uniform(0.015, 0.055)
    churn_rate = rng.uniform(0.015, 0.045)
    new_mrr = mrr * growth_rate
    expansion_mrr = mrr * rng.uniform(0.005, 0.025)
    churn_mrr = mrr * churn_rate
    contraction_mrr = mrr * rng.uniform(0.003, 0.012)
    net_new_mrr = new_mrr + expansion_mrr - churn_mrr - contraction_mrr
    mrr = max(10000, mrr + net_new_mrr)
    new_customers = max(0, int(new_mrr / rng.uniform(80, 180)))
    churned_customers = max(0, int(churn_mrr / rng.uniform(80, 180)))
    customers = max(10, customers + new_customers - churned_customers)
    rows_saas.append({
        "month": m.strftime("%Y-%m"),
        "mrr": round(mrr, 2),
        "new_mrr": round(new_mrr, 2),
        "expansion_mrr": round(expansion_mrr, 2),
        "churned_mrr": round(churn_mrr, 2),
        "contraction_mrr": round(contraction_mrr, 2),
        "net_new_mrr": round(net_new_mrr, 2),
        "arr": round(mrr * 12, 2),
        "total_customers": customers,
        "new_customers": new_customers,
        "churned_customers": churned_customers,
        "arpa": round(mrr / max(1, customers), 2),
        "ltv_estimate": round((mrr / max(1, customers)) / max(0.001, churn_rate), 2),
        "cac_payback_months": round(rng.uniform(8, 20), 1),
        "nrr_pct": round(((mrr - churn_mrr - contraction_mrr + expansion_mrr) / max(1, mrr - net_new_mrr)) * 100, 2),
    })
df_saas_metrics = pd.DataFrame(rows_saas)
save(df_saas_metrics, "saas_metrics.csv")

# ─── 18. CHINOOK (SQLite) ─────────────────────────────────────────────────────
print("18. Chinook Music Store Database (SQLite)")
db_path = os.path.join(OUT, "chinook.db")
if os.path.exists(db_path):
    os.remove(db_path)
conn = sqlite3.connect(db_path)
cur = conn.cursor()

genres = ["Rock","Jazz","Metal","Alternative & Punk","Rock And Roll","Blues","Latin","Reggae",
          "Pop","Soundtrack","Bossa Nova","Easy Listening","Heavy Metal","R&B/Soul",
          "Electronica/Dance","World","Hip Hop/Rap","Science Fiction","TV Shows",
          "Science Fiction","Comedy","Classical","Opera"]
cur.execute("CREATE TABLE Genre (GenreId INTEGER PRIMARY KEY, Name TEXT)")
cur.executemany("INSERT INTO Genre VALUES (?,?)", [(i+1, g) for i,g in enumerate(genres)])

media_types = ["MPEG audio file","Protected AAC audio file","Protected MPEG-4 video file",
               "Purchased AAC audio file","AAC audio file"]
cur.execute("CREATE TABLE MediaType (MediaTypeId INTEGER PRIMARY KEY, Name TEXT)")
cur.executemany("INSERT INTO MediaType VALUES (?,?)", [(i+1, m) for i,m in enumerate(media_types)])

artist_names = ["AC/DC","Accept","Aerosmith","Alanis Morissette","Alice In Chains",
                "Antônio Carlos Jobim","Apocalyptica","Audioslave","BackBeat","Billy Cobham",
                "Black Label Society","Black Sabbath","Body Count","Bruce Dickinson",
                "Buddy Guy","Caetano Veloso","Chico Buarque","Chico Science",
                "Cidade Negra","Cláudio Zoli","David Bowie","Deep Purple","Def Leppard",
                "Djavan","Eric Clapton","Faith No More","Foo Fighters","Frank Zappa",
                "Gilberto Gil","Godsmack","Guns N' Roses","Incognito","Iron Maiden","James Brown",
                "Jimi Hendrix","Joe Satriani","Legião Urbana","Led Zeppelin","Los Hermanos",
                "Marillion","Metallica","Milton Nascimento","Motörhead","Nirvana","O Terço",
                "Oasis","Os Paralamas Do Sucesso","Ozzy Osbourne","Pearl Jam","Pink Floyd"]
cur.execute("CREATE TABLE Artist (ArtistId INTEGER PRIMARY KEY, Name TEXT)")
cur.executemany("INSERT INTO Artist VALUES (?,?)", [(i+1, a) for i,a in enumerate(artist_names)])

n_artists = len(artist_names)
n_albums = 150
cur.execute("CREATE TABLE Album (AlbumId INTEGER PRIMARY KEY, Title TEXT, ArtistId INTEGER, FOREIGN KEY(ArtistId) REFERENCES Artist(ArtistId))")
album_titles = [f"Album {i+1}: {rng.choice(['Greatest Hits','Live','Vol. 1','Vol. 2','Special Edition','Deluxe','Unplugged','Remastered'])}" for i in range(n_albums)]
albums = [(i+1, album_titles[i], rng.integers(1, n_artists+1)) for i in range(n_albums)]
cur.executemany("INSERT INTO Album VALUES (?,?,?)", albums)

cur.execute("""CREATE TABLE Track (
    TrackId INTEGER PRIMARY KEY, Name TEXT, AlbumId INTEGER,
    MediaTypeId INTEGER, GenreId INTEGER, Composer TEXT,
    Milliseconds INTEGER, Bytes INTEGER, UnitPrice REAL,
    FOREIGN KEY(AlbumId) REFERENCES Album(AlbumId),
    FOREIGN KEY(MediaTypeId) REFERENCES MediaType(MediaTypeId),
    FOREIGN KEY(GenreId) REFERENCES Genre(GenreId))""")
track_words = ["Fire","Rain","Night","Storm","Light","Dark","Lost","Free","Wild","Blue",
               "Love","Heart","Soul","Road","Sky","Dreams","Angels","Demons","Run","Rise"]
tracks = []
for tid in range(1, 1001):
    name = f"{rng.choice(track_words)} {rng.choice(track_words)} {rng.integers(1,100)}"
    album_id = rng.integers(1, n_albums+1)
    first_name = rand_names_first(1)[0]
    last_name = rand_names_last(1)[0]
    tracks.append((tid, name, int(album_id), rng.integers(1, 6), rng.integers(1, len(genres)+1),
                   f"{first_name} {last_name}", rng.integers(90000, 600000),
                   rng.integers(2000000, 10000000), 0.99))
cur.executemany("INSERT INTO Track VALUES (?,?,?,?,?,?,?,?,?)", tracks)

cur.execute("""CREATE TABLE Customer (
    CustomerId INTEGER PRIMARY KEY, FirstName TEXT, LastName TEXT,
    Company TEXT, Address TEXT, City TEXT, State TEXT, Country TEXT,
    PostalCode TEXT, Phone TEXT, Fax TEXT, Email TEXT, SupportRepId INTEGER)""")
countries = ["USA","Canada","Brazil","France","Germany","UK","Portugal","Czech Republic","India","Australia"]
customers_c = []
for cid in range(1, 60):
    fn = rand_names_first(1)[0]; ln = rand_names_last(1)[0]
    country = rng.choice(countries)
    customers_c.append((cid, fn, ln, None, f"{rng.integers(1,999)} Main St",
                        rng.choice(["New York","Toronto","São Paulo","Paris","Berlin"]),
                        None, country,
                        f"{rng.integers(10000,99999)}", f"+1 ({rng.integers(200,999)}) {rng.integers(100,999)}-{rng.integers(1000,9999)}",
                        None, f"{fn.lower()}.{ln.lower()}@email.com", rng.integers(3, 6)))
cur.executemany("INSERT INTO Customer VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", customers_c)

cur.execute("""CREATE TABLE Employee (
    EmployeeId INTEGER PRIMARY KEY, LastName TEXT, FirstName TEXT,
    Title TEXT, ReportsTo INTEGER, BirthDate TEXT, HireDate TEXT,
    Address TEXT, City TEXT, State TEXT, Country TEXT, PostalCode TEXT,
    Phone TEXT, Fax TEXT, Email TEXT)""")
employees = [
    (1,"Adams","Andrew","General Manager",None,"1962-02-18","2002-08-14","11120 Jasper Ave NW","Edmonton","AB","Canada","T5K 2N1","+1 (780) 428-9482","+1 (780) 428-3457","andrew@chinookcorp.com"),
    (2,"Edwards","Nancy","Sales Manager",1,"1958-12-08","2002-05-01","825 8 Ave SW","Calgary","AB","Canada","T2P 2T3","+1 (403) 262-3443","+1 (403) 262-3322","nancy@chinookcorp.com"),
    (3,"Peacock","Jane","Sales Support Agent",2,"1973-08-29","2002-04-01","1111 6 Ave SW","Calgary","AB","Canada","T2P 5M5","+1 (403) 262-3443","+1 (403) 262-6712","jane@chinookcorp.com"),
    (4,"Park","Margaret","Sales Support Agent",2,"1947-09-19","2003-05-03","683 10 St NW","Calgary","AB","Canada","T2P 5G3","+1 (403) 263-4423","+1 (403) 263-4289","margaret@chinookcorp.com"),
    (5,"Johnson","Steve","Sales Support Agent",2,"1965-03-03","2003-10-17","7727B 61 Ave","Calgary","AB","Canada","T3B 1Y7","1 (780) 836-9987","1 (780) 836-9543","steve@chinookcorp.com"),
    (6,"Mitchell","Michael","IT Manager",1,"1973-07-01","2003-10-17","5827 Bowness Road NW","Calgary","AB","Canada","T3B 0C5","+1 (403) 246-9887","+1 (403) 246-9899","michael@chinookcorp.com"),
    (7,"King","Robert","IT Staff",6,"1970-05-29","2004-01-02","590 Columbia Boulevard West","Lethbridge","AB","Canada","T1K 5N8","+1 (403) 456-9986","+1 (403) 456-8485","robert@chinookcorp.com"),
    (8,"Callahan","Laura","IT Staff",6,"1968-01-09","2004-03-04","923 7 ST NW","Lethbridge","AB","Canada","T1H 1Y8","+1 (403) 467-3351","+1 (403) 467-8772","laura@chinookcorp.com"),
]
cur.executemany("INSERT INTO Employee VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", employees)

cur.execute("""CREATE TABLE Invoice (
    InvoiceId INTEGER PRIMARY KEY, CustomerId INTEGER, InvoiceDate TEXT,
    BillingAddress TEXT, BillingCity TEXT, BillingState TEXT,
    BillingCountry TEXT, BillingPostalCode TEXT, Total REAL,
    FOREIGN KEY(CustomerId) REFERENCES Customer(CustomerId))""")
invoices = []
for iid in range(1, 401):
    cid = rng.integers(1, 60)
    date = rand_dates("2021-01-01", "2024-06-30", 1)[0].strftime("%Y-%m-%d %H:%M:%S")
    total = round(float(rng.choice([0.99,1.98,3.96,5.94,8.91,13.86,15.84,18.81,21.78], 1)[0]), 2)
    invoices.append((iid, int(cid), date, "123 Main St", "Calgary", "AB", "Canada", "T1K 2N1", total))
cur.executemany("INSERT INTO Invoice VALUES (?,?,?,?,?,?,?,?,?)", invoices)

cur.execute("""CREATE TABLE InvoiceLine (
    InvoiceLineId INTEGER PRIMARY KEY, InvoiceId INTEGER,
    TrackId INTEGER, UnitPrice REAL, Quantity INTEGER,
    FOREIGN KEY(InvoiceId) REFERENCES Invoice(InvoiceId),
    FOREIGN KEY(TrackId) REFERENCES Track(TrackId))""")
invoice_lines = []
lid = 1
for inv in invoices:
    n_lines = rng.integers(1, 8)
    for _ in range(n_lines):
        invoice_lines.append((lid, inv[0], int(rng.integers(1, 1001)), 0.99, 1))
        lid += 1
cur.executemany("INSERT INTO InvoiceLine VALUES (?,?,?,?,?)", invoice_lines)

cur.execute("""CREATE TABLE Playlist (PlaylistId INTEGER PRIMARY KEY, Name TEXT)""")
playlists = [(1,"Music"),(2,"Movies"),(3,"TV Shows"),(4,"Audiobooks"),(5,"90s Music"),
             (6,"Audiobooks"),(7,"Movies"),(8,"Music"),(9,"Music Videos"),(10,"TV Shows"),
             (11,"Brazilian Music"),(12,"Classical"),(13,"Classical 101 - Deep Cuts"),
             (14,"Classical 101 - Next Steps"),(15,"Classical 101 - The Basics"),
             (16,"Grunge"),(17,"Heavy Metal Classic"),(18,"On-The-Go 1")]
cur.executemany("INSERT INTO Playlist VALUES (?,?)", playlists)

cur.execute("""CREATE TABLE PlaylistTrack (PlaylistId INTEGER, TrackId INTEGER, PRIMARY KEY(PlaylistId, TrackId))""")
pt_pairs = set()
for tid in range(1, 1001):
    n_plists = rng.integers(1, 4)
    for pl in rng.choice(range(1, len(playlists)+1), n_plists, replace=False):
        pt_pairs.add((int(pl), tid))
cur.executemany("INSERT INTO PlaylistTrack VALUES (?,?)", list(pt_pairs))

conn.commit()
conn.close()
print(f"  saved chinook.db (11 tables, ~1000 tracks, 400 invoices)")

print("\nAll datasets generated successfully!")
print(f"Output directory: {OUT}")
