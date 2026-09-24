streamlit
pandas
plotly

# ==========================================
# STREAMLIT INTERACTIVE DASHBOARD
# File: strmx.py
# ==========================================

import os
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# ------------------------------------------
# 1. Page Configuration
# ------------------------------------------
st.set_page_config(
    page_title="Online Retail Analytics Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------
# 2. Optimized Data Loading & Path Resolution
# ------------------------------------------
@st.cache_data
def load_data():
    # Resolve exact path to handle running from either root or subfolder
    possible_paths = [
        "online_retail_cleaned_2.csv.gz",
        "online_retail_cleaned_2.csv",
        "final DA.PY PROJ/online_retail_cleaned_2.csv",
        "cleaned_online_retail.csv",
        "online_retail_cleaned.csv",
        "final DA.PY PROJ/cleaned_online_retail.csv",
        "final DA.PY PROJ/online_retail_cleaned.csv"
    ]
    
    file_path = None
    for p in possible_paths:
        if os.path.exists(p):
            file_path = p
            break
            
    if file_path is None:
        raise FileNotFoundError(
            "Could not locate the cleaned CSV file. Please make sure your CSV is in the project folder."
        )

    df = pd.read_csv(file_path)
    
    # Standardize data types
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['CustomerID'] = df['CustomerID'].astype(str)
    
    # Feature Engineering Safety Checks (prevents KeyError)
    if 'TotalAmount' not in df.columns:
        if 'TotalPrice' in df.columns:
            df['TotalAmount'] = df['TotalPrice']
        else:
            df['TotalAmount'] = df['Quantity'] * df['UnitPrice']
            
    if 'YearMonth' not in df.columns:
        df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)
        
    if 'DayOfWeek' not in df.columns:
        df['DayOfWeek'] = df['InvoiceDate'].dt.day_name()
        
    if 'Hour' not in df.columns:
        df['Hour'] = df['InvoiceDate'].dt.hour
        
    return df

try:
    df_sales = load_data()
except Exception as e:
    st.error(f"❌ Failed to load dataset: {e}")
    st.stop()

# ------------------------------------------
# 3. Sidebar Filters
# ------------------------------------------
st.sidebar.header("🎯 Global Dashboard Filters")

# Country Selection
all_countries = sorted(df_sales['Country'].dropna().unique().tolist())
default_countries = [c for c in ['United Kingdom', 'Germany', 'France', 'EIRE', 'Netherlands'] if c in all_countries]

selected_countries = st.sidebar.multiselect(
    "Select Countries:",
    options=all_countries,
    default=default_countries if default_countries else all_countries[:5]
)

# Date Range Selection
min_date = df_sales['InvoiceDate'].min().date()
max_date = df_sales['InvoiceDate'].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range:",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Prevent crash while the user is actively selecting dates
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
elif isinstance(date_range, (list, tuple)) and len(date_range) == 1:
    start_date = end_date = date_range[0]
else:
    start_date, end_date = min_date, max_date

# Filter Dataset
filtered_df = df_sales[
    (df_sales['Country'].isin(selected_countries if selected_countries else all_countries)) &
    (df_sales['InvoiceDate'].dt.date >= start_date) &
    (df_sales['InvoiceDate'].dt.date <= end_date)
]

if filtered_df.empty:
    st.warning("No data for the selected filters. Please widen your selection.")
    st.stop()

# Sidebar Dataset Summary
st.sidebar.markdown("---")
st.sidebar.subheader("📌 Quick Info")
st.sidebar.write(f"**Total Filtered Rows:** {len(filtered_df):,}")
st.sidebar.write(f"**Selected Countries:** {len(selected_countries)}")

# ------------------------------------------
# 4. Header Banner & KPIs
# ------------------------------------------
st.title("🛍️ Online Retail EDA & Sales Dashboard")
st.markdown("Interactive analysis platform for the **Kaggle Online Retail Dataset**.")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

total_revenue = filtered_df['TotalAmount'].sum()
total_orders = filtered_df['InvoiceNo'].nunique()
total_customers = filtered_df['CustomerID'].nunique()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

col1.metric("Total Revenue", f"£{total_revenue:,.2f}")
col2.metric("Total Invoices", f"{total_orders:,}")
col3.metric("Unique Customers", f"{total_customers:,}")
col4.metric("Average Order Value (AOV)", f"£{avg_order_value:,.2f}")

st.markdown("---")

# ------------------------------------------
# 5. Interactive Dashboard Tabs
# ------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📈 Executive Overview", 
    "🔍 EDA Deep Dives", 
    "📄 Data Inspector"
])

# ------------------------------------------
# TAB 1: EXECUTIVE OVERVIEW
# ------------------------------------------
with tab1:
    st.header("Executive Overview & Revenue Trends")
    
    r1_col1, r1_col2 = st.columns(2)
    
    with r1_col1:
        monthly_rev = filtered_df.groupby('YearMonth')['TotalAmount'].sum().reset_index()
        fig_monthly = px.line(
            monthly_rev, x='YearMonth', y='TotalAmount', markers=True,
            title="Monthly Revenue Trend",
            labels={'YearMonth': 'Month', 'TotalAmount': 'Revenue (£)'},
            template="plotly_dark", color_discrete_sequence=['#00E5FF']
        )
        st.plotly_chart(fig_monthly, use_container_width=True)
        
    with r1_col2:
        top_prod = filtered_df.groupby('Description')['TotalAmount'].sum().sort_values(ascending=False).head(8).reset_index()
        fig_top_prod = px.bar(
            top_prod, x='TotalAmount', y='Description', orientation='h',
            title="Top 8 Revenue-Generating Products",
            labels={'TotalAmount': 'Revenue (£)', 'Description': 'Product'},
            template="plotly_dark", color='TotalAmount', color_continuous_scale='Viridis'
        )
        fig_top_prod.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_top_prod, use_container_width=True)

    r2_col1, r2_col2 = st.columns(2)
    
    with r2_col1:
        country_rev = filtered_df.groupby('Country')['TotalAmount'].sum().reset_index()
        fig_country = px.pie(
            country_rev, values='TotalAmount', names='Country',
            title="Revenue Contribution by Country", hole=0.4,
            template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Bold
        )
        st.plotly_chart(fig_country, use_container_width=True)
        
    with r2_col2:
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Sunday']
        heatmap_data = filtered_df.groupby(['DayOfWeek', 'Hour'])['InvoiceNo'].nunique().unstack()
        heatmap_data = heatmap_data.reindex([d for d in day_order if d in heatmap_data.index])
        
        fig_heat = px.imshow(
            heatmap_data,
            title="Order Heatmap (Day of Week vs Hour)",
            labels=dict(x="Hour of Day", y="Day of Week", color="Invoices"),
            template="plotly_dark", color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_heat, use_container_width=True)

# ------------------------------------------
# TAB 2: EDA DEEP DIVES
# ------------------------------------------
with tab2:
    st.header("Interactive Analysis Questions")
    
    selected_question = st.selectbox(
        "Select an Analysis Question:",
        options=[
            "Q1: Revenue Contribution by Country",
            "Q2: Customer Pareto Concentration (80/20 Rule)",
            "Q3: Top Customers by Total Spend",
            "Q4: Unit Price vs. Quantity Correlation"
        ]
    )
    
    if "Q1:" in selected_question:
        q1_data = filtered_df.groupby('Country')['TotalAmount'].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(
            q1_data, x='TotalAmount', y='Country', orientation='h',
            title="Total Revenue by Country", color='TotalAmount',
            template="plotly_dark", color_continuous_scale='Plasma'
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
        top_country = q1_data.iloc[0]
        top_share = top_country['TotalAmount'] / q1_data['TotalAmount'].sum() * 100
        st.info(f"💡 **Insight:** {top_country['Country']} generates {top_share:.1f}% of revenue in the current selection.")
        
    elif "Q2:" in selected_question:
        cust_rev = filtered_df.groupby('CustomerID')['TotalAmount'].sum().sort_values(ascending=False).reset_index()
        cust_rev['CumulativeRevenue'] = cust_rev['TotalAmount'].cumsum()
        cust_rev['CumulativePercent'] = (cust_rev['CumulativeRevenue'] / cust_rev['TotalAmount'].sum()) * 100
        cust_rev['CustomerRankPercent'] = (np.arange(len(cust_rev)) + 1) / len(cust_rev) * 100
        
        fig = px.line(
            cust_rev, x='CustomerRankPercent', y='CumulativePercent',
            title="Pareto Curve: % of Customers vs % of Total Revenue",
            template="plotly_dark", color_discrete_sequence=['#FFD700']
        )
        fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="80% Revenue Benchmark")
        st.plotly_chart(fig, use_container_width=True)
        top20_share = cust_rev.loc[cust_rev['CustomerRankPercent'] <= 20, 'TotalAmount'].sum() / cust_rev['TotalAmount'].sum() * 100
        pct_for_80 = ((cust_rev['CumulativePercent'] < 80).sum() + 1) / len(cust_rev) * 100
        st.info(f"💡 **Insight:** The top 20% of customers generate {top20_share:.1f}% of revenue, and {pct_for_80:.1f}% of customers account for 80%.")
        
    elif "Q3:" in selected_question:
        top_cust = filtered_df.groupby('CustomerID')['TotalAmount'].sum().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(
            top_cust, x='CustomerID', y='TotalAmount',
            title="Top 10 High-Value Customers", color='TotalAmount',
            template="plotly_dark", color_continuous_scale='Electric'
        )
        st.plotly_chart(fig, use_container_width=True)
        top10_share = top_cust['TotalAmount'].sum() / filtered_df['TotalAmount'].sum() * 100
        st.info(f"💡 **Insight:** The top 10 customers contribute {top10_share:.1f}% of revenue; the largest single customer spent £{top_cust['TotalAmount'].iloc[0]:,.0f}.")
        
    elif "Q4:" in selected_question:
        subset_df = filtered_df[(filtered_df['Quantity'] < 500) & (filtered_df['UnitPrice'] < 50)]
        sample_df = subset_df.sample(min(2000, len(subset_df)), random_state=42)
        fig = px.scatter(
            sample_df, x='UnitPrice', y='Quantity', color='TotalAmount',
            title="Unit Price vs Quantity (Sampled Data)",
            template="plotly_dark", color_continuous_scale='Rainbow', opacity=0.7
        )
        st.plotly_chart(fig, use_container_width=True)
        if len(subset_df) > 1:
            corr = subset_df['UnitPrice'].corr(subset_df['Quantity'])
            trend = " Cheaper items tend to be bought in larger quantities." if corr < 0 else ""
            st.info(f"💡 **Insight:** Correlation between unit price and quantity is r = {corr:.2f}.{trend}")

# ------------------------------------------
# TAB 3: DATA INSPECTOR & EXPORT
# ------------------------------------------
with tab3:
    st.header("Filtered Dataset Preview")
    st.dataframe(filtered_df.head(100), use_container_width=True)
    
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Filtered Data as CSV",
        data=csv,
        file_name='filtered_online_retail.csv',
        mime='text/csv'
    )
