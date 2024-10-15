import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Page configuration
st.set_page_config(page_title="E-commerce Insights Dashboard 🌟", layout="wide")
sns.set(style='darkgrid')
palette = sns.color_palette("Blues", 10)

# Load dataset
data = pd.read_csv("data/all_data.csv")
data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])
data['order_approved_at'] = pd.to_datetime(data['order_approved_at'])
data['order_delivered_customer_date'] = pd.to_datetime(data['order_delivered_customer_date'])
data['order_estimated_delivery_date'] = pd.to_datetime(data['order_estimated_delivery_date'])

# Title and Metrics
st.title("E-commerce Insights Dashboard 🌟")

# Tabs for organizing content
tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🏆 Top Products", "📍 Customer Demographics", "📦 Shipping Analysis"])

with tab1:
    st.header("Overview")
    total_sales = data['price'].sum()
    avg_delivery_time = (data['order_delivered_customer_date'] - data['order_estimated_delivery_date']).mean()
    st.metric(label="Total Sales", value=format_currency(total_sales, 'USD', locale='en_US'))
    st.metric(label="Average Delivery Delay", value=f"{avg_delivery_time.days} days")
    
    # Improved Daily Orders Line Chart with consistent color
    fig, ax = plt.subplots(figsize=(12, 6))
    daily_orders = data.groupby(data['order_purchase_timestamp'].dt.date)['order_id'].count()
    ax.plot(daily_orders.index, daily_orders.values, marker='o', color=palette[5], linewidth=2, label='Daily Orders')
    ax.set_title('Daily Orders with Rolling Average', fontsize=16)
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Orders')

    # Add rolling average
    rolling_avg = daily_orders.rolling(window=7).mean()
    ax.plot(daily_orders.index, rolling_avg, color=palette[3], linestyle='--', label='7-Day Rolling Average')

    # Add peak annotations
    max_orders_date = daily_orders.idxmax()
    max_orders_value = daily_orders.max()
    ax.annotate(f'Max: {max_orders_value} Orders', xy=(max_orders_date, max_orders_value), 
                 xytext=(max_orders_date, max_orders_value + 50), 
                 arrowprops=dict(facecolor=palette[2], arrowstyle='->'))

    ax.legend()
    st.pyplot(fig)

with tab2:
    st.header("Top Products")
    product_freq = data['product_category_name_english'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(y=product_freq.index, x=product_freq.values, palette='viridis', ax=ax)
    ax.set_title('Top 10 Products by Order Count')
    ax.set_xlabel('Order Count')
    ax.set_ylabel('Product Category')
    st.pyplot(fig)

with tab3:
    st.header("Customer Demographics")
    city_freq = data['customer_city'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(y=city_freq.index, x=city_freq.values, palette='coolwarm', ax=ax)
    ax.set_title('Top 10 Cities by Customer Orders')
    ax.set_xlabel('Number of Orders')
    ax.set_ylabel('City')
    st.pyplot(fig)

    # Geospatial Analysis (Optional)
    st.subheader("Geospatial Distribution of Customers")
    # Visualization code can be added here for geospatial maps using libraries like Folium or Plotly.

with tab4:
    st.header("Shipping Analysis")
    # Distribution of delivery delays
    st.subheader("Delivery Delay Distribution")
    data['delivery_delay'] = (data['order_delivered_customer_date'] - data['order_estimated_delivery_date']).dt.days
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data['delivery_delay'], bins=30, color="navy", ax=ax)
    ax.axvline(data['delivery_delay'].mean(), color='red', linestyle='--', linewidth=2, label='Average Delay')
    ax.set_title("Distribution of Delivery Delays", fontsize=14)
    ax.set_xlabel("Days of Delay")
    ax.set_ylabel("Number of Orders")
    ax.legend()
    st.pyplot(fig)

    # Impact of approval time on delivery schedule
    st.subheader("Impact of Approval Time on Delivery Duration")
    approval_delivery_diff = (data['order_delivered_customer_date'] - data['order_approved_at']).dt.days
    avg_approval_diff = approval_delivery_diff.groupby(data['order_approved_at'].dt.date).mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    avg_approval_diff.plot(ax=ax, color='darkblue')
    ax.set_title("Average Delivery Time Based on Approval Date", fontsize=14)
    ax.set_xlabel("Approval Date")
    ax.set_ylabel("Average Days of Delivery")
    st.pyplot(fig)

# Sidebar filters for advanced analysis
with st.sidebar:
    st.image("ecommerceasset.jpg")
    st.header("Advanced Filters")
    selected_city = st.multiselect("Filter by Cities", options=data['customer_city'].unique(), default=None)
    date_range = st.date_input("Date Range", value=[data['order_purchase_timestamp'].min(), data['order_purchase_timestamp'].max()])
    
    # Filter data based on user selection
    filtered_data = data.copy()
    if selected_city:
        filtered_data = filtered_data[filtered_data['customer_city'].isin(selected_city)]
    if date_range:
        start_date, end_date = date_range
        filtered_data = filtered_data[(filtered_data['order_purchase_timestamp'].dt.date >= start_date) &
                                      (filtered_data['order_purchase_timestamp'].dt.date <= end_date)]

# Download filtered data
st.sidebar.markdown("### Download Filtered Data")
csv = filtered_data.to_csv(index=False)
st.sidebar.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='filtered_data.csv',
    mime='text/csv',
)

# Comments section for user feedback
st.sidebar.text_area("Add Comments", "provide me suggestions.")
