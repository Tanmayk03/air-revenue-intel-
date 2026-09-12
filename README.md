<div align="center">

# ✈️ AIRLINE REVENUE LEAKAGE & PRICING INTELLIGENCE

### *End-to-End Pricing Intelligence, Revenue Exposure Estimation & Expected Fare Modeling*

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analytics-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML%20Benchmark-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-Executive_Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![R2 Score](https://img.shields.io/badge/Model_R²-91.29%25-brightgreen?style=for-the-badge)

</div>

---

## 📌 Executive Summary

Airlines operate in a high-frequency dynamic pricing environment. Sub-optimal fare bucket allocations often result in **Revenue Leakage** (selling tickets below market benchmark prices during high-value windows) or **Competitive Pricing Risk** (overpricing tickets relative to market competitors and losing passenger volume).

This project establishes a **Machine Learning Expected Fare Benchmark**, calculates **Segment Leakage Scores (%)**, quantifies **₹10.07 Crores of Directional Revenue Exposure**, and delivers executive recommendations backed by SQL and Power BI architecture.

---

## 🏗 Project Architecture & Pipeline

```
Raw Flight Data (300K+ Rows)
       │
       ├──► 1. Data Hygiene & Cleaning (Zero Nulls, Categorical Audit)
       │
       ├──► 2. Business Feature Engineering
       │        ├── Route Pairs (source -> destination)
       │        ├── Booking Window Buckets (0-7, 8-14, 15-30, 31+ Days)
       │        └── Route Competition Counts
       │
       ├──► 3. Expected Fare Benchmark Model (Linear Regression | R² = 91.29%)
       │
       ├──► 4. Leakage Score (%) & Directional Revenue Exposure (₹ Lacs/Crs)
       │
       ├──► 5. SQLite Analytics Engine (CASE WHEN, DENSE_RANK Window Functions)
       │
       └──► 6. 4-Page Power BI Executive Dashboard Architecture
```

---

## 🎯 Key Project Metrics

| Metric | Value | Business Significance |
| :--- | :--- | :--- |
| **Total Analyzed Flights** | `300,153` | Full 6-Metro Domestic Indian Flight Coverage |
| **Model $R^2$ Score** | `91.29%` | Highly reliable expected fare baseline ($\hat{y}$) |
| **Model MAE** | `₹4,447.11` | Tight benchmark accuracy across Economy & Business |
| **Directional Exposure** | `₹10.07 Crores` | Identified uncaptured revenue upside across underpriced segments |
| **Top Leakage Segment** | `-28.56%` | `Chennai -> Kolkata` (31+ Days Advance Window) |

---

## 💡 Business Hypotheses & Key Findings

> [!IMPORTANT]
> **H1 (Advance Booking Revenue Leakage)**: Fares in the `31+ Days` advance window on long-haul routes are underpriced by **24% to 28%**, creating an estimated **₹10.07 Crores** of directional revenue opportunity.

> [!NOTE]
> **H2 (Last-Minute Corporate Yield Capture)**: In the `0-7 Days` window on business routes (`Delhi -> Mumbai`), Full-Service Carriers (Vistara & Air India) command a **~60% premium** over Low-Cost Carriers (SpiceJet & AirAsia).

> [!WARNING]
> **H3 (Competitive Overpricing Risk)**: Fares on `Delhi <-> Hyderabad` in advance booking windows are **+70% to +103% higher** than expected market benchmarks, posing severe passenger churn risk.

---

## 🤖 Expected Fare Model Performance

An interpretable **Linear Regression Model** was trained on 240,122 flights and evaluated on 60,031 test flights:

* **Target Variable ($y$)**: `price` (INR)
* **Predictor Features ($X$)**: `airline`, `source_city`, `destination_city`, `class`, `stops`, `departure_time`, `days_bucket`, `duration`, `days_left`, `competition_count`

```python
# Model Evaluation Summary
MAE  = ₹4,447.11
RMSE = ₹6,699.37
R²   = 0.9129 (91.29% Variance Explained)
```

---

## 📐 Segment Leakage Score Formula

$$\text{Segment Leakage Score (\%)} = \left( \frac{\text{Mean Actual Fare} - \text{Mean Expected Fare}}{\text{Mean Expected Fare}} \right) \times 100$$

* **Negative Score (%)**: Ticket sold below benchmark $\rightarrow$ **Revenue Leakage**
* **Positive Score (%)**: Ticket sold above benchmark $\rightarrow$ **Competitive Overpricing Risk**

---

## 🗄️ SQL Analytics Highlights

The dataset was exported to **SQLite (`data/processed/airline_revenue.db`)** for production querying:

### 1. Business Status Classification (`CASE WHEN`)
```sql
SELECT 
    route,
    days_bucket,
    ROUND(AVG(price), 2) AS avg_price,
    ROUND(AVG(expected_fare), 2) AS expected_fare,
    CASE 
        WHEN ((AVG(price) - AVG(expected_fare)) / AVG(expected_fare)) * 100 < -15 THEN 'Severe Revenue Leakage'
        WHEN ((AVG(price) - AVG(expected_fare)) / AVG(expected_fare)) * 100 > 15 THEN 'Severe Overpricing Risk'
        ELSE 'Optimal Pricing'
    END AS pricing_status
FROM flights
WHERE class = 'Economy'
GROUP BY route, days_bucket;
```

### 2. Airline Price Rank (`DENSE_RANK() OVER`)
```sql
WITH RouteAirlineRank AS (
    SELECT 
        route, days_bucket, airline,
        ROUND(AVG(price), 2) AS avg_airline_fare,
        DENSE_RANK() OVER (PARTITION BY route, days_bucket ORDER BY AVG(price) ASC) AS price_rank
    FROM flights
    WHERE class = 'Economy'
    GROUP BY route, days_bucket, airline
)
SELECT * FROM RouteAirlineRank WHERE route = 'Delhi -> Mumbai' AND days_bucket = '0-7 Days';
```

---

## 📊 Power BI Dashboard Architecture

| Page | Title | Core Visuals & Features |
| :--- | :--- | :--- |
| **Page 1** | Executive Summary | Key KPI Cards (Exposure in Cr, Avg Fare, Leakage %), Exposure Bar Chart |
| **Page 2** | Route Explorer | Days to Departure Price Curve (Actual vs Expected Benchmark) |
| **Page 3** | Competitor Benchmark | Airline Pricing Matrix & Price Rank Leaderboard |
| **Page 4** | Scenario Simulator | What-If Parameter Slider (% Price Adjustment vs Revenue Impact) |

---

## 🚀 Project Folder Structure

```
airline-revenue-intelligence/
│
├── data/
│   ├── raw/
│   │   └── Clean_Dataset.csv
│   └── processed/
│       ├── airline_revenue.db             <-- SQLite Database
│       └── airline_revenue_processed.csv  <-- Power BI Ready Dataset
│
├── notebooks/
│   └── airline_analysis.ipynb             <-- Full Analysis & ML Notebook
│
├── sql/
│   └── analysis.sql                       <-- Production SQL Queries
│
├── dashboard/                             <-- Power BI Dashboard (.pbix)
├── reports/                               <-- PDF / Presentation Reports
├── .gitignore                             <-- Git Ignore Configuration
└── README.md                              <-- Project Documentation
```

---

## 🤝 Key Recommendations & Action Plan

1. **Step-Up Advance Booking Fares**: Raise advance window (`31+ Days`) price floors by **10–15%** on long-haul routes (`Mumbai -> Kolkata`, `Kolkata -> Bangalore`) to capture **₹10.07 Crores** in directional leakage.
2. **Dynamic Corporate Surcharge**: Introduce last-minute (`0-7 Days`) corporate dynamic surcharges (+₹1,000 to ₹1,500) for budget carriers on high-density business routes (`Delhi -> Mumbai`).
3. **Re-align Overpriced Advance Fares**: Reduce initial advance fares on `Delhi <-> Hyderabad` to prevent early passenger churn to competitors.

---

<div align="center">
  <b>Designed & Developed as a Business Analytics & Data Science Portfolio Project</b>
</div>
