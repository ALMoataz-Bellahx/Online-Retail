# Online-Retail
# 🛍️ Online Retail Analytics &amp; Interactive EDA Dashboard
## Dataset

[Online Retail dataset](https://archive.ics.uci.edu/dataset/352/online+retail) (also on Kaggle): **541,909 raw transactions** from a UK-based online gift retailer, 1 Dec 2010 to 9 Dec 2011.

After cleaning: **397,884 transactions · 18,532 invoices · 4,338 customers · 37 countries · £8.9M revenue** (prices are in sterling).

**Cleaning steps:** removed rows with missing `CustomerID`, removed cancellation and return records (negative quantities), removed non-positive prices, then engineered `TotalAmount`, `Year`, `Month`, `DayOfWeek`, `Hour`, and `YearMonth`.

## What's Inside

| File | Description |
|------|-------------|
| `project_2.ipynb` | Part 1: data loading, cleaning, feature engineering, univariate analysis |
| `02_bivariate_analysis_2.ipynb` | Part 2: **15 business questions** (bivariate and multivariate analysis) |
| `strmx.py` | Streamlit dashboard with country and date filters, KPI cards, and 4 deep-dive analyses |
| `online_retail_cleaned_2.csv.gz` | Cleaned dataset (compressed, pandas reads it directly) |
| `requirements.txt` | Python dependencies |

## Key Findings

- **The UK drives the business:** over 80% of revenue, with the Netherlands (3.2%), EIRE (3.0%), Germany (2.6%), and France (2.3%) next.
- **Strong seasonality:** revenue climbs from September to November 2011, peaking in November at about £1.16M. This is consistent with pre-holiday demand.
- **Revenue is concentrated in a few customers:** the top 10% of customers generate roughly 60% of revenue, and about 26% of customers account for 80%.
- **Timing patterns:** Thursday is the strongest day (about 22% of revenue), there are no Saturday orders, and 12:00 is the busiest hour for invoices.

## Dashboard Features

- Sidebar filters for country and date range
- KPI cards: total revenue, invoices, unique customers, average order value
- Monthly revenue trend, top products, revenue by country, and a day-of-week vs. hour order heatmap
- Deep dives: revenue by country, customer Pareto curve (80/20), top customers, and unit price vs. quantity
- Data inspector with CSV export of the filtered data

## Tech Stack

Python · Pandas · NumPy · Plotly Express · Streamlit · Jupyter Notebook

## Run Locally

```bash
git clone https://github.com/ALMoataz-Bellahx/Online-Retail.git
cd Online-Retail
pip install -r requirements.txt
streamlit run strmx.py
```

To re-run the notebooks, download the raw `OnlineRetail.csv` from the link above for `project_2.ipynb`. For `02_bivariate_analysis_2.ipynb`, change the file name in the `pd.read_csv(...)` line to `online_retail_cleaned_2.csv.gz`.

## Author

**Abd-Elrahman Al-Moataz Bellah**: [LinkedIn](https://www.linkedin.com/in/al-moataz/) · [GitHub](https://github.com/ALMoataz-Bellahx)
