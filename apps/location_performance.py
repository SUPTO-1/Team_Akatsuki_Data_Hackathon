import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

def app():
    st.title("Location Performance")
    st.write("Comparative analysis of performance across different store locations, including sales, transactions, and peak times.")

    # Load the dataset
    data = pd.read_csv("Cleaned_Coffee_Shop_Sales.csv")
    data['transaction_date'] = pd.to_datetime(data['transaction_date'])
    data['transaction_hour'] = pd.to_datetime(data['transaction_time'], format='%H:%M:%S').dt.hour
    data['day_of_week'] = data['transaction_date'].dt.day_name()

    # Sidebar filter for Date Range
    st.sidebar.header("Filters")
    start_date = st.sidebar.date_input("Start Date", value=data['transaction_date'].min())
    end_date = st.sidebar.date_input("End Date", value=data['transaction_date'].max())
    selected_location = st.sidebar.selectbox("Select Store Location", options=data['store_location'].unique())

    # Filter data based on the selected date range and location
    filtered_data = data[(data['transaction_date'] >= pd.to_datetime(start_date)) &
                         (data['transaction_date'] <= pd.to_datetime(end_date))]
    location_data = filtered_data[filtered_data['store_location'] == selected_location]

    # Key Metrics for the Selected Location
    st.write(f"## Key Metrics for {selected_location}")
    total_sales = location_data['total_sales'].sum()
    transaction_count = location_data['transaction_id'].nunique()
    avg_transaction_value = location_data['total_sales'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Transaction Count", f"{transaction_count}")
    col3.metric("Avg. Transaction Value", f"${avg_transaction_value:.2f}")

    # Sales by Day of the Week
    st.write(f"## Sales by Day of the Week for {selected_location}")
    weekday_sales = location_data.groupby('day_of_week')['total_sales'].sum().reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )
    fig = px.bar(weekday_sales, x=weekday_sales.index, y=weekday_sales.values,
                 labels={"x": "Day of the Week", "y": "Total Sales ($)"},
                 title="Total Sales by Day of the Week",
                 color=weekday_sales.values, color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)

    # Peak Sales Hours for Selected Location
    st.write(f"## Peak Sales Hours for {selected_location}")
    hourly_sales = location_data.groupby('transaction_hour')['total_sales'].sum()
    fig = px.line(hourly_sales, x=hourly_sales.index, y=hourly_sales.values,
                  labels={"x": "Hour of Day", "y": "Total Sales ($)"},
                  title="Total Sales by Hour of the Day",
                  markers=True, color_discrete_sequence=['blue'])
    st.plotly_chart(fig, use_container_width=True)

    # High-performing vs. Low-performing Stores Comparison
    st.write("## High-Performing vs. Low-Performing Stores")

    # Total sales by location
    location_sales = filtered_data.groupby('store_location')['total_sales'].sum().sort_values(ascending=False)
    fig = px.bar(location_sales, x=location_sales.index, y=location_sales.values,
                 labels={"x": "Store Location", "y": "Total Sales ($)"},
                 title="Total Sales by Store Location",
                 color=location_sales.values, color_continuous_scale='Teal')
    st.plotly_chart(fig, use_container_width=True)

    # Average transaction value by location
    avg_transaction_value_location = filtered_data.groupby('store_location')['total_sales'].mean().sort_values(ascending=False)
    fig = px.bar(avg_transaction_value_location, x=avg_transaction_value_location.index, y=avg_transaction_value_location.values,
                 labels={"x": "Store Location", "y": "Avg. Transaction Value ($)"},
                 title="Average Transaction Value by Store Location",
                 color=avg_transaction_value_location.values, color_continuous_scale='Sunset')
    st.plotly_chart(fig, use_container_width=True)

    # Heatmap of Sales by Hour and Day of the Week for Selected Location
    st.write(f"## Heatmap of Sales by Hour and Day for {selected_location}")
    heatmap_data = location_data.pivot_table(values='total_sales', index='day_of_week', columns='transaction_hour', aggfunc='sum').reindex(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu", linewidths=0.5, ax=ax)
    ax.set_title("Sales Heatmap by Hour and Day of the Week")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Day of the Week")
    st.pyplot(fig)

    # Additional Insight: Comparison Metrics (Top 5 and Bottom 5 Stores by Sales)
    st.write("## Top 5 and Bottom 5 Stores by Sales")

    # Top 5 Stores
    top_5_stores = location_sales.head(5)
    fig = px.bar(top_5_stores, x=top_5_stores.values, y=top_5_stores.index, orientation='h',
                 labels={"x": "Total Sales ($)", "y": "Store Location"},
                 title="Top 5 High-Performing Stores by Total Sales",
                 color=top_5_stores.values, color_continuous_scale='Blues')
    st.plotly_chart(fig, use_container_width=True)

    # Bottom 5 Stores
    bottom_5_stores = location_sales.tail(5)
    fig = px.bar(bottom_5_stores, x=bottom_5_stores.values, y=bottom_5_stores.index, orientation='h',
                 labels={"x": "Total Sales ($)", "y": "Store Location"},
                 title="Bottom 5 Low-Performing Stores by Total Sales",
                 color=bottom_5_stores.values, color_continuous_scale='Reds')
    st.plotly_chart(fig, use_container_width=True)
