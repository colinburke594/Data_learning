#!/usr/bin/env python3
"""Generate 23 synthetic CLEAN CSV datasets for the Data Scientist Hub."""

import csv
import random
import math
import os
from datetime import datetime, timedelta

random.seed(42)
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

def write_csv(filename, headers, rows):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)
    print(f"  {filename}: {len(rows)} rows x {len(headers)} cols")

def rand_date(start, end):
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

def rand_datetime(start, end):
    delta = int((end - start).total_seconds())
    return start + timedelta(seconds=random.randint(0, delta))

def rand_phone():
    return f"({random.randint(200,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}"

def gauss_clamp(mu, sigma, lo, hi):
    return max(lo, min(hi, round(random.gauss(mu, sigma), 2)))

def rand_name():
    firsts = ["James","Mary","Robert","Patricia","John","Jennifer","Michael","Linda","David","Elizabeth",
              "William","Barbara","Richard","Susan","Joseph","Jessica","Thomas","Sarah","Christopher","Karen",
              "Charles","Lisa","Daniel","Nancy","Matthew","Betty","Anthony","Margaret","Mark","Sandra",
              "Steven","Ashley","Paul","Kimberly","Andrew","Emily","Joshua","Donna","Kenneth","Michelle",
              "Kevin","Carol","Brian","Amanda","George","Dorothy","Timothy","Melissa","Ronald","Deborah",
              "Jason","Stephanie","Edward","Rebecca","Ryan","Sharon","Jacob","Laura","Gary","Cynthia",
              "Nicholas","Kathleen","Eric","Amy","Jonathan","Angela","Stephen","Shirley","Larry","Brenda"]
    lasts = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez",
             "Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin",
             "Lee","Perez","Thompson","White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson",
             "Walker","Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores",
             "Green","Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell","Carter","Roberts"]
    return random.choice(firsts), random.choice(lasts)

STATES = ["CA","TX","NY","FL","IL","PA","OH","GA","NC","MI","NJ","VA","WA","AZ","MA",
          "TN","IN","MO","MD","WI","CO","MN","SC","AL","LA","KY","OR","OK","CT","UT"]
CITIES = {"CA":["Los Angeles","San Francisco","San Diego","Sacramento","San Jose"],
          "TX":["Houston","Dallas","Austin","San Antonio","Fort Worth"],
          "NY":["New York","Buffalo","Rochester","Albany","Syracuse"],
          "FL":["Miami","Orlando","Tampa","Jacksonville","Fort Lauderdale"],
          "IL":["Chicago","Springfield","Naperville","Peoria","Rockford"],
          "PA":["Philadelphia","Pittsburgh","Allentown","Erie","Reading"],
          "OH":["Columbus","Cleveland","Cincinnati","Toledo","Akron"],
          "GA":["Atlanta","Savannah","Augusta","Athens","Macon"],
          "NC":["Charlotte","Raleigh","Durham","Greensboro","Wilmington"],
          "WA":["Seattle","Tacoma","Spokane","Vancouver","Bellevue"],
          "CO":["Denver","Boulder","Colorado Springs","Fort Collins","Aurora"],
          "MA":["Boston","Cambridge","Worcester","Springfield","Lowell"]}
for s in STATES:
    if s not in CITIES:
        CITIES[s] = [f"{s} City","Springfield","Riverside","Fairview","Madison"]

COUNTRIES = ["US","UK","CA","DE","FR","AU","JP","BR","IN","MX","ES","IT","NL","SE","KR","SG","NZ","IE","NO","DK"]


# ─── 1. retail_sales_clean.csv ───
def gen_retail_sales():
    print("1/23 retail_sales_clean.csv")
    regions = ["Northeast","Southeast","Midwest","West","Southwest"]
    categories = ["Electronics","Clothing","Home & Garden","Sports","Books","Beauty","Toys","Food & Beverage"]
    products = {
        "Electronics": ["Wireless Headphones","Bluetooth Speaker","USB-C Hub","Laptop Stand","Webcam","Smart Watch","Phone Case","Portable Charger"],
        "Clothing": ["Cotton T-Shirt","Denim Jeans","Running Shoes","Winter Jacket","Casual Sneakers","Wool Sweater","Silk Scarf","Leather Belt"],
        "Home & Garden": ["Ceramic Planter","LED Desk Lamp","Throw Pillow","Kitchen Scale","Wall Clock","Scented Candle","Door Mat","Shelf Organizer"],
        "Sports": ["Yoga Mat","Resistance Bands","Water Bottle","Jump Rope","Foam Roller","Tennis Balls","Cycling Gloves","Running Belt"],
        "Books": ["Python Cookbook","Data Science Handbook","Machine Learning Guide","Statistics Primer","SQL Mastery","Business Analytics","AI Ethics","Deep Learning Intro"],
        "Beauty": ["Face Moisturizer","Lip Balm Set","Sunscreen SPF50","Hair Serum","Eye Cream","Body Lotion","Nail Polish Set","Makeup Brush Kit"],
        "Toys": ["Building Blocks","Board Game","Puzzle Set","Action Figure","Art Supply Kit","Card Game","Stuffed Animal","Remote Car"],
        "Food & Beverage": ["Organic Coffee","Green Tea Pack","Protein Bars","Trail Mix","Olive Oil","Honey Jar","Granola","Dark Chocolate"]
    }
    reps = [f"{rand_name()[0]} {rand_name()[1]}" for _ in range(30)]
    rows = []
    start = datetime(2022, 1, 1)
    end = datetime(2025, 12, 31)
    for i in range(1230):
        cat = random.choice(categories)
        prod = random.choice(products[cat])
        qty = random.randint(1, 20)
        price = round(random.uniform(5, 500), 2)
        disc = round(random.choice([0, 0, 0, 0.05, 0.1, 0.15, 0.2, 0.25]), 2)
        total = round(qty * price * (1 - disc), 2)
        rows.append([
            f"ORD-{10000+i}",
            rand_date(start, end).strftime("%Y-%m-%d"),
            random.choice(regions),
            cat, prod,
            random.choice(reps),
            qty, price, disc, total,
            round(random.uniform(1, 5), 1)
        ])
    write_csv("retail_sales_clean.csv",
        ["order_id","order_date","region","product_category","product_name","sales_rep","quantity","unit_price","discount_pct","total_amount","customer_rating"], rows)


# ─── 2. employee_hr_clean.csv ───
def gen_employee_hr():
    print("2/23 employee_hr_clean.csv")
    depts = ["Engineering","Sales","Marketing","Finance","HR","Operations","Legal","Customer Support"]
    titles = {"Engineering":["Software Engineer","Senior Engineer","Staff Engineer","Engineering Manager","DevOps Engineer"],
              "Sales":["Sales Associate","Account Executive","Sales Manager","Regional Director","Sales Analyst"],
              "Marketing":["Marketing Coordinator","Content Strategist","SEO Specialist","Marketing Manager","Brand Analyst"],
              "Finance":["Financial Analyst","Accountant","Senior Accountant","Finance Manager","Controller"],
              "HR":["HR Coordinator","Recruiter","HR Business Partner","HR Manager","Benefits Specialist"],
              "Operations":["Operations Analyst","Logistics Coordinator","Operations Manager","Supply Chain Analyst","Facilities Coordinator"],
              "Legal":["Paralegal","Legal Counsel","Compliance Officer","Contract Specialist","Legal Assistant"],
              "Customer Support":["Support Agent","Senior Support Agent","Support Team Lead","Support Manager","Technical Support"]}
    rows = []
    for i in range(820):
        fn, ln = rand_name()
        dept = random.choice(depts)
        title = random.choice(titles[dept])
        hire = rand_date(datetime(2010,1,1), datetime(2025,6,1))
        age = random.randint(22, 65)
        tenure = round((datetime(2025,12,31) - hire).days / 365.25, 1)
        salary = round(random.gauss(75000, 25000))
        salary = max(35000, min(200000, salary))
        rows.append([
            f"EMP-{1000+i}", fn, ln, dept, title,
            hire.strftime("%Y-%m-%d"),
            salary, age,
            random.choice(["Male","Female","Non-binary"]),
            random.choice(["Full-time","Full-time","Full-time","Part-time","Contract"]),
            tenure,
            round(random.uniform(1, 5), 1),
            rand_phone()
        ])
    write_csv("employee_hr_clean.csv",
        ["employee_id","first_name","last_name","department","job_title","hire_date","salary","age","gender","employment_type","years_tenure","performance_score","phone"], rows)


# ─── 3. ecommerce_orders_clean.csv ───
def gen_ecommerce():
    print("3/23 ecommerce_orders_clean.csv")
    prods = ["Wireless Mouse","Mechanical Keyboard","Monitor Stand","USB Hub","Webcam","Desk Lamp","Ergonomic Chair",
             "Laptop Sleeve","Phone Stand","Cable Organizer","Mouse Pad","Headphone Hook","Screen Cleaner",
             "Portable SSD","Bluetooth Adapter","Smart Plug","LED Strip","Desk Pad","Ring Light","Microphone"]
    tags = ["tech","office","accessories","electronics","home","gadgets","productivity","ergonomic"]
    promos = ["","","","","SAVE10","WELCOME15","FLASH20","SUMMER25","HOLIDAY30"]
    payments = ["Credit Card","PayPal","Debit Card","Apple Pay","Google Pay"]
    statuses = ["Delivered","Delivered","Delivered","Delivered","Shipped","Processing","Returned","Cancelled"]
    rows = []
    for i in range(2050):
        odate = rand_date(datetime(2023,1,1), datetime(2025,12,31))
        nitems = random.randint(1, 8)
        val = round(nitems * random.uniform(10, 150), 2)
        ship = round(val * random.uniform(0.03, 0.12), 2) if val < 75 else 0.0
        rows.append([
            f"ECO-{20000+i}",
            odate.strftime("%Y-%m-%d"),
            f"CUST-{random.randint(1000,9999)}",
            random.choice(prods),
            nitems, val, ship,
            random.choice([True, False]),
            "|".join(random.sample(tags, random.randint(1,3))),
            random.choice(COUNTRIES),
            random.choice(promos),
            random.choice(payments),
            random.choice(statuses)
        ])
    write_csv("ecommerce_orders_clean.csv",
        ["order_id","order_date","customer_id","product_name","num_items","order_value_usd","shipping_cost","is_returning_customer","product_tags","country","promo_code","payment_method","delivery_status"], rows)


# ─── 4. patient_health_clean.csv ───
def gen_patient_health():
    print("4/23 patient_health_clean.csv")
    conditions = ["Hypertension","Type 2 Diabetes","Asthma","COPD","Heart Disease","Obesity","Arthritis","Depression","Migraine","Healthy"]
    codes = {"Hypertension":"I10","Type 2 Diabetes":"E11.9","Asthma":"J45.909","COPD":"J44.1",
             "Heart Disease":"I25.10","Obesity":"E66.01","Arthritis":"M19.90","Depression":"F32.9","Migraine":"G43.909","Healthy":"Z00.00"}
    rows = []
    for i in range(1525):
        age = random.randint(18, 90)
        gender = random.choice(["Male","Female"])
        h = gauss_clamp(170 if gender=="Male" else 162, 10, 140, 210)
        w = gauss_clamp(80 if gender=="Male" else 68, 15, 40, 160)
        bmi = round(w / ((h/100)**2), 1)
        cond = random.choice(conditions)
        rows.append([
            f"PAT-{5000+i}", age, gender, h, w, bmi,
            random.randint(90, 180),
            random.randint(60, 110),
            random.randint(60, 250),
            cond, codes[cond],
            random.choice(["Yes","No","No","No"]),
            rand_date(datetime(2022,1,1), datetime(2025,12,31)).strftime("%Y-%m-%d"),
            random.choice(["Yes","No","No","No","No"])
        ])
    write_csv("patient_health_clean.csv",
        ["patient_id","age","gender","height_cm","weight_kg","bmi","blood_pressure_systolic","blood_pressure_diastolic","glucose_mg_dl","condition","diagnosis_code","smoker","visit_date","readmitted"], rows)


# ─── 5. marketing_campaigns_clean.csv ───
def gen_marketing():
    print("5/23 marketing_campaigns_clean.csv")
    channels = ["Email","Social Media","Search Ads","Display Ads","Video Ads","Influencer","Direct Mail","Podcast"]
    audiences = ["18-24 Urban","25-34 Professionals","35-44 Parents","45-54 Homeowners","55+ Retirees","Small Business","Enterprise","Students"]
    camp_adj = ["Spring","Summer","Fall","Winter","Holiday","Flash","Mega","Premium","Exclusive","Launch"]
    camp_noun = ["Sale","Promo","Blast","Drive","Campaign","Push","Offer","Deal","Event","Special"]
    rows = []
    for i in range(915):
        sd = rand_date(datetime(2022,1,1), datetime(2025,10,1))
        ed = sd + timedelta(days=random.randint(7, 90))
        budget = round(random.uniform(500, 50000), 2)
        spend = round(budget * random.uniform(0.6, 1.0), 2)
        imps = random.randint(5000, 500000)
        clicks = int(imps * random.uniform(0.005, 0.08))
        ctr = round(clicks / imps * 100, 2) if imps > 0 else 0
        convs = int(clicks * random.uniform(0.01, 0.15))
        conv_rate = round(convs / clicks * 100, 2) if clicks > 0 else 0
        rev = round(convs * random.uniform(20, 200), 2)
        roi = round((rev - spend) / spend * 100, 2) if spend > 0 else 0
        rows.append([
            f"CMP-{3000+i}",
            f"{random.choice(camp_adj)} {random.choice(camp_noun)} {sd.year}",
            random.choice(channels),
            sd.strftime("%Y-%m-%d"), ed.strftime("%Y-%m-%d"),
            budget, spend, imps, clicks, ctr, convs, conv_rate, rev, roi,
            random.choice(audiences)
        ])
    write_csv("marketing_campaigns_clean.csv",
        ["campaign_id","campaign_name","channel","start_date","end_date","budget_usd","spend_usd","impressions","clicks","ctr","conversions","conversion_rate","revenue_usd","roi_pct","target_audience"], rows)


# ─── 6. real_estate_listings_clean.csv ───
def gen_real_estate():
    print("6/23 real_estate_listings_clean.csv")
    streets = ["Main St","Oak Ave","Maple Dr","Cedar Ln","Elm Blvd","Pine Rd","Washington St","Park Ave","Lake Dr","Hill Rd",
               "River Rd","Sunset Blvd","Forest Ave","Valley Ln","Spring St","Meadow Dr","Highland Ave","Church St","School Rd","Mill St"]
    prop_types = ["Single Family","Condo","Townhouse","Multi-Family","Ranch"]
    agents = [f"{rand_name()[0]} {rand_name()[1]}" for _ in range(50)]
    rows = []
    for i in range(1840):
        st = random.choice(STATES[:12])
        city = random.choice(CITIES[st])
        addr = f"{random.randint(100,9999)} {random.choice(streets)}"
        sqft = random.randint(600, 5500)
        price = round(sqft * random.uniform(100, 600) + random.uniform(-10000, 50000), -2)
        sale = round(price * random.uniform(0.92, 1.08), -2)
        ld = rand_date(datetime(2022,1,1), datetime(2025,10,1))
        dom = random.randint(3, 180)
        sd = ld + timedelta(days=dom)
        rows.append([
            f"LST-{40000+i}", addr, city, st,
            f"{random.randint(10000,99999)}",
            price, sale, sqft,
            round(random.uniform(0.05, 2.5), 2),
            random.randint(1, 6),
            random.choice([1, 1.5, 2, 2.5, 3, 3.5, 4]),
            random.randint(0, 3),
            random.randint(1950, 2024),
            random.choice(prop_types),
            dom,
            ld.strftime("%Y-%m-%d"),
            sd.strftime("%Y-%m-%d"),
            random.choice(agents)
        ])
    write_csv("real_estate_listings_clean.csv",
        ["listing_id","address","city","state","zip_code","list_price","sale_price","sqft","lot_size_acres","bedrooms","bathrooms","garage_spaces","year_built","property_type","days_on_market","listing_date","sale_date","agent_name"], rows)


# ─── 7. student_performance_clean.csv ───
def gen_student():
    print("7/23 student_performance_clean.csv")
    majors = ["Computer Science","Business","Biology","Psychology","Engineering","Mathematics","English","History","Chemistry","Economics"]
    semesters = ["Fall 2022","Spring 2023","Fall 2023","Spring 2024","Fall 2024","Spring 2025"]
    grades = {"A+":4.0,"A":4.0,"A-":3.7,"B+":3.3,"B":3.0,"B-":2.7,"C+":2.3,"C":2.0,"C-":1.7,"D":1.0,"F":0.0}
    rows = []
    for i in range(1020):
        fn, ln = rand_name()
        gpa = gauss_clamp(3.0, 0.6, 0.5, 4.0)
        att = gauss_clamp(85, 12, 30, 100)
        mid = gauss_clamp(75, 12, 20, 100)
        final = gauss_clamp(74, 14, 15, 100)
        avg = (mid + final) / 2
        if avg >= 90: g = "A"
        elif avg >= 80: g = "B"
        elif avg >= 70: g = "C"
        elif avg >= 60: g = "D"
        else: g = "F"
        rows.append([
            f"STU-{2000+i}", fn, ln,
            random.choice(majors),
            random.choice(semesters),
            random.randint(18, 30),
            random.choice(["Male","Female","Non-binary"]),
            gpa, att,
            random.randint(5, 30),
            mid, final, g,
            g != "F"
        ])
    write_csv("student_performance_clean.csv",
        ["student_id","first_name","last_name","major","semester","age","gender","gpa","attendance_pct","assignments_submitted","midterm_score","final_score","overall_grade","passed"], rows)


# ─── 8. saas_subscriptions_clean.csv ───
def gen_saas():
    print("8/23 saas_subscriptions_clean.csv")
    plans = ["Free","Starter","Professional","Enterprise"]
    mrr_range = {"Free":(0,0),"Starter":(29,99),"Professional":(100,499),"Enterprise":(500,5000)}
    industries = ["Technology","Healthcare","Finance","Retail","Education","Manufacturing","Media","Government","Non-profit","Consulting"]
    regions = ["North America","Europe","Asia Pacific","Latin America","Middle East"]
    companies = [f"{random.choice(['Acme','Nova','Apex','Zenith','Vertex','Nimbus','Forge','Spark','Pulse','Wave'])} {random.choice(['Solutions','Tech','Labs','Systems','Corp','Inc','Digital','AI','Cloud','Analytics'])}" for _ in range(500)]
    rows = []
    for i in range(1635):
        plan = random.choices(plans, weights=[10,30,40,20])[0]
        lo, hi = mrr_range[plan]
        mrr = round(random.uniform(lo, hi), 2)
        signup = rand_date(datetime(2020,1,1), datetime(2025,6,1))
        churned = random.random() < 0.25
        churn_d = (signup + timedelta(days=random.randint(30, 800))).strftime("%Y-%m-%d") if churned else ""
        age_d = (datetime(2025,12,31) - signup).days
        ll = rand_date(signup, datetime(2025,12,31))
        rows.append([
            f"CO-{6000+i}",
            random.choice(companies),
            plan, mrr,
            random.randint(0, 50000),
            age_d,
            random.choice(regions),
            random.choice(industries),
            random.choice([1,3,6,12,24]),
            signup.strftime("%Y-%m-%d"),
            churn_d, churned,
            random.randint(-100, 100),
            random.randint(0, 50),
            ll.strftime("%Y-%m-%d"),
            random.randint(1, 500)
        ])
    write_csv("saas_subscriptions_clean.csv",
        ["company_id","company_name","plan","mrr_usd","usage_events","account_age_days","region","industry","contract_months","signup_date","churn_date","churned","nps_score","support_tickets","last_login_date","seats"], rows)


# ─── 9. climate_weather_clean.csv ───
def gen_weather():
    print("9/23 climate_weather_clean.csv")
    stations = [f"WX-{s}" for s in range(1, 11)]
    conditions = ["Clear","Partly Cloudy","Cloudy","Rain","Fog","Snow","Thunderstorm","Windy","Drizzle","Haze"]
    dirs = ["N","NE","E","SE","S","SW","W","NW"]
    rows = []
    d = datetime(2023, 1, 1)
    for _ in range(5200):
        station = random.choice(stations)
        month = d.month
        base_temp = 5 + 15 * math.sin((month - 1) / 12 * 2 * math.pi - math.pi/2)
        tc = round(base_temp + random.gauss(0, 5), 1)
        tf = round(tc * 9/5 + 32, 1)
        rows.append([
            station, d.strftime("%Y-%m-%d"),
            tc, tf,
            random.randint(10, 100),
            round(max(0, random.gauss(0.1, 0.3)), 2),
            round(max(0, random.gauss(15, 8)), 1),
            random.choice(dirs),
            round(random.gauss(1013, 10), 1),
            round(max(0.5, random.gauss(10, 4)), 1),
            random.choice(conditions),
            random.randint(0, 11)
        ])
        d += timedelta(hours=random.randint(3, 8))
    write_csv("climate_weather_clean.csv",
        ["station_id","date","temp_celsius","temp_fahrenheit","humidity_pct","precipitation_inches","wind_speed_kmh","wind_direction","pressure_hpa","visibility_km","conditions","uv_index"], rows)


# ─── 10. social_media_analytics_clean.csv ───
def gen_social():
    print("10/23 social_media_analytics_clean.csv")
    platforms = ["Instagram","Twitter","Facebook","TikTok","LinkedIn","YouTube"]
    ptypes = ["Image","Video","Carousel","Text","Story","Reel","Live"]
    cats = ["Product Launch","Educational","Behind the Scenes","User Generated","Promotional","Entertainment","News","Tutorial"]
    sents = ["Positive","Neutral","Negative"]
    rows = []
    for i in range(3400):
        likes = random.randint(0, 50000)
        comments = random.randint(0, int(likes * 0.1 + 10))
        shares = random.randint(0, int(likes * 0.05 + 5))
        imps = likes * random.randint(5, 30)
        reach = int(imps * random.uniform(0.5, 0.95))
        eng = round((likes + comments + shares) / imps * 100, 2) if imps > 0 else 0
        fc = random.randint(500, 5000000)
        plat = random.choice(platforms)
        vv = random.randint(100, 500000) if plat in ("TikTok","YouTube","Instagram") else 0
        rows.append([
            f"POST-{80000+i}",
            plat,
            rand_date(datetime(2023,1,1), datetime(2025,12,31)).strftime("%Y-%m-%d"),
            random.choice(ptypes),
            random.choice(cats),
            likes, comments, shares, imps, reach, eng, fc,
            random.randint(0, 30),
            random.choices(sents, weights=[50,35,15])[0],
            random.randint(0, int(likes * 0.02 + 5)),
            vv
        ])
    write_csv("social_media_analytics_clean.csv",
        ["post_id","platform","post_date","post_type","content_category","likes","comments","shares","impressions","reach","engagement_rate","follower_count","hashtag_count","sentiment","link_clicks","video_views"], rows)


# ─── 11. supply_chain_logistics_clean.csv ───
def gen_supply_chain():
    print("11/23 supply_chain_logistics_clean.csv")
    carriers = ["FedEx","UPS","USPS","DHL","Amazon Logistics","OnTrac","XPO Logistics","Old Dominion"]
    statuses = ["Delivered","Delivered","Delivered","Delivered","In Transit","Out for Delivery","Returned","Delayed"]
    priorities = ["Standard","Express","Overnight","Economy"]
    rows = []
    for i in range(4200):
        o_st = random.choice(STATES[:15])
        d_st = random.choice(STATES[:15])
        sd = rand_date(datetime(2022,1,1), datetime(2025,12,1))
        dd_days = random.randint(1, 14)
        dd = sd + timedelta(days=dd_days)
        wt = round(random.uniform(0.1, 150), 2)
        sc = round(wt * random.uniform(0.5, 3) + random.uniform(3, 15), 2)
        tracking = f"1Z{''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=16))}"
        rows.append([
            f"SHP-{50000+i}",
            f"ORD-{random.randint(10000,60000)}",
            random.choice(CITIES[o_st]), o_st,
            random.choice(CITIES[d_st]), d_st,
            random.choice(carriers),
            sd.strftime("%Y-%m-%d"), dd.strftime("%Y-%m-%d"),
            dd_days, wt,
            round(random.uniform(5, 200), 1),
            round(random.uniform(5, 100), 1),
            round(random.uniform(5, 80), 1),
            sc,
            random.choice(statuses),
            tracking,
            random.choice(priorities),
            round(random.uniform(0, 5000), 2),
            random.choice(["No","No","No","No","Yes"])
        ])
    write_csv("supply_chain_logistics_clean.csv",
        ["shipment_id","order_id","origin_city","origin_state","dest_city","dest_state","carrier","ship_date","delivery_date","delivery_days","weight_kg","length_cm","width_cm","height_cm","shipping_cost_usd","delivery_status","tracking_number","priority","insurance_value","damage_reported"], rows)


# ─── 12. stock_price_history_clean.csv ───
def gen_stocks():
    print("12/23 stock_price_history_clean.csv")
    tickers = ["AAPL","MSFT","GOOGL","AMZN","TSLA","META","NVDA","JPM","JNJ","V","PG","UNH","HD","DIS","NFLX","PYPL","INTC","AMD","CRM","ORCL"]
    rows = []
    prices = {t: random.uniform(50, 500) for t in tickers}
    d = datetime(2022, 1, 3)
    end = datetime(2025, 8, 1)
    count = 0
    while d <= end and count < 12600:
        if d.weekday() < 5:
            for t in tickers:
                p = prices[t]
                change = p * random.gauss(0.0003, 0.015)
                p = max(10, p + change)
                prices[t] = p
                o = round(p * random.uniform(0.99, 1.01), 2)
                c = round(p, 2)
                h = round(max(o, c) * random.uniform(1.0, 1.02), 2)
                l = round(min(o, c) * random.uniform(0.98, 1.0), 2)
                vol = random.randint(1000000, 80000000)
                adj = round(c * random.uniform(0.998, 1.0), 2)
                div = round(random.uniform(0, 0.5), 2) if random.random() < 0.01 else 0.0
                rows.append([d.strftime("%Y-%m-%d"), t, o, h, l, c, vol, adj, div])
                count += 1
                if count >= 12600:
                    break
        d += timedelta(days=1)
    write_csv("stock_price_history_clean.csv",
        ["date","ticker","open","high","low","close","volume","adjusted_close","dividend"], rows)


# ─── 13. customer_reviews_nlp_clean.csv ───
def gen_reviews():
    print("13/23 customer_reviews_nlp_clean.csv")
    cats = ["Electronics","Books","Home & Kitchen","Clothing","Sports","Beauty","Toys","Grocery"]
    adj_pos = ["Amazing","Excellent","Great","Wonderful","Fantastic","Perfect","Outstanding","Superb","Love","Best"]
    adj_neg = ["Terrible","Awful","Poor","Disappointing","Bad","Worst","Broken","Defective","Useless","Horrible"]
    adj_mid = ["Okay","Decent","Average","Fine","Acceptable","Fair","Adequate","Reasonable","Alright","Standard"]
    nouns = ["product","item","purchase","quality","value","design","material","performance","delivery","experience"]
    rows = []
    for i in range(8900):
        rating = random.choices([1,2,3,4,5], weights=[5,8,15,30,42])[0]
        if rating >= 4:
            adj = random.choice(adj_pos)
            sent = "Positive"
        elif rating <= 2:
            adj = random.choice(adj_neg)
            sent = "Negative"
        else:
            adj = random.choice(adj_mid)
            sent = "Neutral"
        noun = random.choice(nouns)
        title = f"{adj} {noun}"
        text = f"This {noun} is {adj.lower()}. " + random.choice([
            f"I would definitely recommend this to others.",
            f"The {noun} met my expectations overall.",
            f"Not sure I would buy this again.",
            f"Exactly what I was looking for.",
            f"Could be better for the price.",
            f"Great {noun} for the money.",
            f"Quality is {adj.lower()} as described.",
            f"Shipping was fast and packaging was good.",
            f"I have been using this for weeks now.",
            f"Compared to similar products this stands out."
        ])
        rows.append([
            f"REV-{100000+i}",
            f"PROD-{random.randint(1000,5000)}",
            f"USR-{random.randint(10000,99999)}",
            rand_date(datetime(2022,1,1), datetime(2025,12,31)).strftime("%Y-%m-%d"),
            rating, title, text,
            random.choice([True, True, True, False]),
            random.randint(0, 200),
            random.choice(cats),
            sent
        ])
    write_csv("customer_reviews_nlp_clean.csv",
        ["review_id","product_id","user_id","review_date","rating","review_title","review_text","verified_purchase","helpful_votes","product_category","sentiment"], rows)


# ─── 14. census_demographics_clean.csv ───
def gen_census():
    print("14/23 census_demographics_clean.csv")
    workclasses = ["Private","Self-emp-not-inc","Self-emp-inc","Federal-gov","State-gov","Local-gov"]
    educations = [("Bachelors",13),("Some-college",10),("HS-grad",9),("Masters",14),("Assoc-voc",11),("Assoc-acdm",12),("Doctorate",16),("Prof-school",15),("11th",7),("10th",6)]
    maritals = ["Married-civ-spouse","Never-married","Divorced","Separated","Widowed"]
    occs = ["Exec-managerial","Prof-specialty","Craft-repair","Adm-clerical","Sales","Other-service","Machine-op-inspct","Transport-moving","Tech-support","Farming-fishing"]
    rels = ["Husband","Wife","Own-child","Not-in-family","Other-relative","Unmarried"]
    races = ["White","Black","Asian-Pac-Islander","Amer-Indian-Eskimo","Other"]
    countries = ["United-States","Mexico","Philippines","Germany","Canada","India","El-Salvador","Cuba","Jamaica","China","England","Italy","Japan","Vietnam","South-Korea"]
    housing = ["Own","Rent","With Family","Other"]
    rows = []
    for i in range(3200):
        age = random.randint(17, 90)
        ed = random.choice(educations)
        hpw = max(1, min(99, int(random.gauss(40, 12))))
        cg = max(0, int(random.gauss(1000, 5000))) if random.random() < 0.15 else 0
        cl = max(0, int(random.gauss(50, 200))) if random.random() < 0.08 else 0
        inc = ">50K" if (random.random() < 0.24) else "<=50K"
        rows.append([
            f"CEN-{70000+i}", age,
            random.choice(workclasses),
            ed[0], ed[1],
            random.choice(maritals),
            random.choice(occs),
            random.choice(rels),
            random.choices(races, weights=[75,12,5,3,5])[0],
            random.choice(["Male","Female"]),
            cg, cl, hpw,
            random.choices(countries, weights=[85]+[1]*14)[0],
            inc,
            random.choice(STATES),
            f"{random.randint(1001,56999):05d}",
            random.randint(1, 7),
            random.choice(housing),
            random.choice(["Yes","Yes","Yes","No"]),
            random.choice(["No","No","No","No","Yes"]),
            random.choice(["No","No","No","No","No","Yes"])
        ])
    write_csv("census_demographics_clean.csv",
        ["person_id","age","workclass","education","education_num","marital_status","occupation","relationship","race","sex","capital_gain","capital_loss","hours_per_week","native_country","income_bracket","state","county_fips","household_size","housing_type","health_insurance","veteran_status","disability_status"], rows)


# ─── 15. energy_consumption_clean.csv ───
def gen_energy():
    print("15/23 energy_consumption_clean.csv")
    btypes = ["Office","Retail","Hospital","School","Warehouse","Residential","Data Center"]
    hvac = ["Cooling","Heating","Auto","Off"]
    rows = []
    ts = datetime(2024, 1, 1)
    buildings = [(f"BLD-{b+1}", random.choice(btypes), random.randint(2000, 100000)) for b in range(5)]
    for _ in range(8760):
        bld = random.choice(buildings)
        hour = ts.hour
        is_wknd = ts.weekday() >= 5
        base = bld[2] * 0.001
        if 8 <= hour <= 18 and not is_wknd:
            mult = random.uniform(1.5, 3.0)
        else:
            mult = random.uniform(0.3, 0.8)
        energy = round(base * mult + random.gauss(0, base * 0.1), 2)
        month = ts.month
        temp = round(40 + 30 * math.sin((month - 1) / 12 * 2 * math.pi - math.pi/2) + random.gauss(0, 5), 1)
        rows.append([
            ts.strftime("%Y-%m-%d %H:%M:%S"),
            bld[0],
            max(0, energy),
            temp,
            random.randint(15, 95),
            0 if is_wknd else random.randint(0, 1),
            bld[1], bld[2],
            random.choice(hvac),
            is_wknd
        ])
        ts += timedelta(hours=1)
    write_csv("energy_consumption_clean.csv",
        ["timestamp","building_id","energy_kwh","temperature_f","humidity_pct","occupancy","building_type","floor_area_sqft","hvac_mode","is_weekend"], rows)


# ─── 16. clinical_genomics_clean.csv ───
def gen_genomics():
    print("16/23 clinical_genomics_clean.csv")
    cancers = ["Breast","Lung","Colorectal","Prostate","Pancreatic","Melanoma","Ovarian","Bladder"]
    stages = ["I","II","III","IV"]
    treatments = ["Chemotherapy","Immunotherapy","Targeted Therapy","Radiation","Surgery","Combination"]
    responses = ["Complete Response","Partial Response","Stable Disease","Progressive Disease"]
    genes = ["gene_BRCA1","gene_TP53","gene_EGFR","gene_KRAS","gene_PIK3CA","gene_PTEN","gene_MYC","gene_RB1","gene_APC","gene_BRAF","gene_ERBB2"]
    rows = []
    for i in range(450):
        age = random.randint(25, 85)
        stage = random.choices(stages, weights=[20,30,30,20])[0]
        surv = random.randint(30, 2500)
        row = [
            f"GEN-{9000+i}", age,
            random.choice(["Male","Female"]),
            random.choice(cancers), stage,
            random.choice(treatments),
            random.choice(responses),
            surv,
            random.choice([0, 0, 1])  # censored
        ]
        for g in genes:
            # expression value: mostly normal (0-2) with some high/low
            row.append(round(max(0, random.gauss(1.0, 0.8)), 3))
        rows.append(row)
    write_csv("clinical_genomics_clean.csv",
        ["patient_id","age","sex","cancer_type","stage","treatment","response","survival_days","censored"] + genes, rows)


# ─── 17. financial_fraud_clean.csv ───
def gen_fraud():
    print("17/23 financial_fraud_clean.csv")
    rows = []
    for i in range(28480):
        is_fraud = 1 if random.random() < 0.017 else 0
        t = random.randint(0, 172800)
        vs = []
        for v in range(28):
            if is_fraud:
                vs.append(round(random.gauss(0, 2.5), 6))
            else:
                vs.append(round(random.gauss(0, 1.0), 6))
        amt = round(abs(random.gauss(88, 250)) if not is_fraud else abs(random.gauss(120, 300)), 2)
        rows.append([f"TXN-{200000+i}", t] + vs + [amt, is_fraud])
    cols = ["transaction_id","time_seconds"] + [f"v{j}" for j in range(1,29)] + ["amount_usd","is_fraud"]
    write_csv("financial_fraud_clean.csv", cols, rows)


# ─── 18. iot_sensor_telemetry_clean.csv ───
def gen_iot():
    print("18/23 iot_sensor_telemetry_clean.csv")
    devices = [f"DEV-{d:03d}" for d in range(1, 21)]
    statuses = ["Normal","Normal","Normal","Normal","Warning","Critical"]
    rows = []
    ts = datetime(2024, 6, 1)
    for _ in range(21000):
        dev = random.choice(devices)
        status = random.choice(statuses)
        temp = gauss_clamp(45 if status == "Normal" else 70, 10, 10, 120)
        hum = random.randint(20, 85)
        vib = round(abs(random.gauss(0.5 if status == "Normal" else 2.0, 0.5)), 3)
        pres = round(random.gauss(30, 3), 2)
        pwr = round(random.gauss(250 if status == "Normal" else 400, 50), 1)
        rows.append([
            ts.strftime("%Y-%m-%d %H:%M:%S"),
            dev, temp, hum, vib, pres, status, max(0, pwr)
        ])
        ts += timedelta(seconds=random.randint(10, 120))
    write_csv("iot_sensor_telemetry_clean.csv",
        ["timestamp","device_id","temperature_c","humidity_pct","vibration_g","pressure_psi","machine_status","power_watts"], rows)


# ─── 19. employee_engagement_survey_clean.csv ───
def gen_engagement():
    print("19/23 employee_engagement_survey_clean.csv")
    depts = ["Engineering","Sales","Marketing","Finance","HR","Operations","Legal","Customer Support","Product","Design"]
    levels = ["Individual Contributor","Senior IC","Team Lead","Manager","Director","VP"]
    rows = []
    for i in range(2800):
        tenure = round(random.uniform(0.5, 20), 1)
        eng = gauss_clamp(3.5, 0.8, 1, 5)
        sat = gauss_clamp(3.4, 0.9, 1, 5)
        mgr = gauss_clamp(3.6, 0.7, 1, 5)
        risk = "High" if (eng < 2.5 and sat < 2.5) else ("Medium" if eng < 3.2 else "Low")
        rows.append([
            f"RESP-{30000+i}",
            random.choice(depts),
            random.choice(levels),
            tenure,
            eng, sat, mgr,
            gauss_clamp(3.3, 0.9, 1, 5),
            gauss_clamp(3.2, 0.8, 1, 5),
            gauss_clamp(3.4, 0.9, 1, 5),
            gauss_clamp(3.1, 1.0, 1, 5),
            gauss_clamp(3.5, 0.7, 1, 5),
            random.randint(1, 10),
            rand_date(datetime(2023,1,1), datetime(2025,12,1)).strftime("%Y-%m-%d"),
            risk
        ])
    write_csv("employee_engagement_survey_clean.csv",
        ["respondent_id","department","job_level","tenure_years","engagement_score","satisfaction_score","manager_score","worklife_balance","growth_opportunity","recognition","compensation_fairness","team_collaboration","overall_recommend","response_date","attrition_risk"], rows)


# ─── 20. geospatial_location_clean.csv ───
def gen_geospatial():
    print("20/23 geospatial_location_clean.csv")
    payments = ["Credit Card","Cash","Debit Card","Mobile"]
    # NYC area bounding box
    rows = []
    for i in range(15000):
        plat = round(random.uniform(40.65, 40.85), 6)
        plon = round(random.uniform(-74.02, -73.90), 6)
        dlat = round(random.uniform(40.65, 40.85), 6)
        dlon = round(random.uniform(-74.02, -73.90), 6)
        dist = round(abs(plat - dlat) * 69 + abs(plon - dlon) * 52 + random.uniform(0.2, 2), 2)
        dur = round(dist * random.uniform(2, 8) + random.uniform(1, 10), 1)
        fare = round(2.50 + dist * random.uniform(2, 4) + dur * 0.1, 2)
        tip = round(fare * random.uniform(0, 0.3), 2)
        pdt = rand_datetime(datetime(2024,1,1), datetime(2025,12,31))
        ddt = pdt + timedelta(minutes=int(dur))
        rows.append([
            f"TRIP-{400000+i}",
            pdt.strftime("%Y-%m-%d %H:%M:%S"),
            ddt.strftime("%Y-%m-%d %H:%M:%S"),
            plat, plon, dlat, dlon,
            random.randint(1, 6),
            dist, fare, tip,
            round(fare + tip, 2),
            random.choice(payments),
            dur
        ])
    write_csv("geospatial_location_clean.csv",
        ["trip_id","pickup_datetime","dropoff_datetime","pickup_lat","pickup_lon","dropoff_lat","dropoff_lon","passenger_count","trip_distance_miles","fare_amount","tip_amount","total_amount","payment_type","trip_duration_min"], rows)


# ─── 21. ab_test_results_clean.csv ───
def gen_ab_test():
    print("21/23 ab_test_results_clean.csv")
    experiments = [f"EXP-{e}" for e in range(1, 6)]
    variants = ["Control","Treatment_A","Treatment_B"]
    devices = ["Desktop","Mobile","Tablet"]
    browsers = ["Chrome","Safari","Firefox","Edge"]
    rows = []
    for i in range(9400):
        exp = random.choice(experiments)
        var = random.choice(variants)
        conv = random.random() < (0.03 if var == "Control" else 0.045 if var == "Treatment_A" else 0.05)
        exp_date = rand_date(datetime(2024,1,1), datetime(2025,12,1))
        ss = rand_datetime(datetime.combine(exp_date, datetime.min.time()), datetime.combine(exp_date, datetime.min.time()) + timedelta(hours=23))
        se = ss + timedelta(minutes=random.randint(1, 60))
        rev = round(random.uniform(10, 200), 2) if conv else 0.0
        rows.append([
            f"USR-{500000+i}",
            exp, var,
            exp_date.strftime("%Y-%m-%d"),
            ss.strftime("%Y-%m-%d %H:%M:%S"),
            se.strftime("%Y-%m-%d %H:%M:%S"),
            random.randint(1, 25),
            conv, rev,
            random.choice(devices),
            random.choice(browsers),
            random.choice(COUNTRIES)
        ])
    write_csv("ab_test_results_clean.csv",
        ["user_id","experiment_id","variant","first_exposure_date","session_start","session_end","page_views","converted","revenue_usd","device_type","browser","country"], rows)


# ─── 22. movie_ratings_clean.csv ───
def gen_movies():
    print("22/23 movie_ratings_clean.csv")
    genres_pool = ["Action","Comedy","Drama","Horror","Sci-Fi","Romance","Thriller","Animation","Documentary","Adventure","Fantasy","Mystery","Crime","Musical","Western"]
    tags_pool = ["classic","funny","dark","inspiring","overrated","underrated","must-see","boring","masterpiece","rewatchable","slow","intense","heartwarming","thought-provoking","visually stunning"]
    titles = []
    adj = ["The","A","Return of the","Rise of","Last","Dark","Secret","Eternal","Lost","Silent","Midnight","Golden","Iron","Crimson","Silver"]
    noun = ["Kingdom","Journey","Legend","Dream","Storm","Shadow","Phoenix","Horizon","Frontier","Odyssey","Knight","Flame","Bridge","Tower","Ocean"]
    for a in adj:
        for n in noun:
            titles.append(f"{a} {n}")
    random.shuffle(titles)
    titles = titles[:500]
    movies = {}
    for idx, t in enumerate(titles):
        mid = f"MOV-{idx+1:04d}"
        g = "|".join(random.sample(genres_pool, random.randint(1, 3)))
        yr = random.randint(1970, 2025)
        imdb = f"tt{random.randint(1000000,9999999)}"
        movies[mid] = (t, g, yr, imdb)
    rows = []
    for i in range(10083):
        mid = random.choice(list(movies.keys()))
        t, g, yr, imdb = movies[mid]
        ts = rand_datetime(datetime(2020,1,1), datetime(2025,12,31))
        rows.append([
            f"USR-{random.randint(1,5000)}",
            mid,
            round(random.choice([0.5,1,1.5,2,2.5,3,3.5,4,4.5,5]), 1),
            int(ts.timestamp()),
            t, g, yr,
            random.choice(tags_pool),
            imdb
        ])
    write_csv("movie_ratings_clean.csv",
        ["user_id","movie_id","rating","timestamp","movie_title","genres","year","tag","imdb_id"], rows)


# ─── 23. server_logs_clean.csv ───
def gen_server_logs():
    print("23/23 server_logs_clean.csv")
    methods = ["GET","GET","GET","GET","POST","POST","PUT","DELETE","PATCH"]
    endpoints = ["/","/api/users","/api/products","/api/orders","/api/auth/login","/api/auth/logout",
                 "/api/search","/api/cart","/api/checkout","/api/payments","/api/reviews",
                 "/api/inventory","/api/reports","/api/dashboard","/api/settings",
                 "/api/notifications","/api/analytics","/health","/api/upload","/api/export"]
    status_codes = [200,200,200,200,200,201,204,301,302,304,400,401,403,404,404,500,502,503]
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/119.0.0.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
        "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 Safari/17.0",
        "python-requests/2.31.0",
        "curl/8.4.0",
        "PostmanRuntime/7.35.0",
        "Go-http-client/2.0"
    ]
    referrers = ["https://www.google.com","https://www.bing.com","https://github.com",
                 "https://app.example.com","https://dashboard.example.com","direct","direct","direct",
                 "https://www.linkedin.com","https://twitter.com"]
    rows = []
    ts = datetime(2025, 1, 1)
    for i in range(50000):
        ip = f"{random.randint(10,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        method = random.choice(methods)
        ep = random.choice(endpoints)
        sc = random.choice(status_codes)
        rt = round(abs(random.gauss(120, 80)) + 5, 1) if sc < 500 else round(abs(random.gauss(2000, 1000)) + 500, 1)
        bs = random.randint(100, 50000) if sc == 200 else random.randint(50, 500)
        rows.append([
            ts.strftime("%Y-%m-%d %H:%M:%S"),
            ip, method, ep, sc, rt, bs,
            random.choice(user_agents),
            random.choice(referrers)
        ])
        ts += timedelta(seconds=random.randint(0, 3))
    write_csv("server_logs_clean.csv",
        ["timestamp","ip_address","method","endpoint","status_code","response_time_ms","bytes_sent","user_agent","referrer"], rows)


# ─── Run all generators ───
if __name__ == "__main__":
    print(f"Generating 23 clean datasets in: {OUT_DIR}\n")
    gen_retail_sales()
    gen_employee_hr()
    gen_ecommerce()
    gen_patient_health()
    gen_marketing()
    gen_real_estate()
    gen_student()
    gen_saas()
    gen_weather()
    gen_social()
    gen_supply_chain()
    gen_stocks()
    gen_reviews()
    gen_census()
    gen_energy()
    gen_genomics()
    gen_fraud()
    gen_iot()
    gen_engagement()
    gen_geospatial()
    gen_ab_test()
    gen_movies()
    gen_server_logs()
    print("\nDone! All 23 datasets generated.")
