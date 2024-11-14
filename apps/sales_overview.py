import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

def app():
    st.title("Sales Overview")
    st.write("A comprehensive view of sales data with trends, breakdowns, and location-based insights.")

    # Load the dataset
    data = pd.read_csv("Cleaned_Coffee_Shop_Sales.csv")
    data['transaction_date'] = pd.to_datetime(data['transaction_date'])

    # Sidebar filters for Date Range and Product Category
    st.sidebar.header("Filters")
    start_date = st.sidebar.date_input("Start Date", value=data['transaction_date'].min())
    end_date = st.sidebar.date_input("End Date", value=data['transaction_date'].max())
    category_options = data['product_category'].unique()
    selected_category = st.sidebar.multiselect("Select Product Categories", category_options, default=category_options)

    # Filter data based on the selected date range and categories
    filtered_data = data[
        (data['transaction_date'] >= pd.to_datetime(start_date)) &
        (data['transaction_date'] <= pd.to_datetime(end_date)) &
        (data['product_category'].isin(selected_category))
    ]

    # Key metrics
    st.write("## Key Sales Metrics")
    total_sales = filtered_data['total_sales'].sum()
    total_transactions = filtered_data['transaction_id'].nunique()
    avg_transaction_value = filtered_data['total_sales'].mean()
    unique_products = filtered_data['product_id'].nunique()
    unique_locations = filtered_data['store_location'].nunique()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sales", f"${total_sales:,.2f}")
    with col2:
        st.metric("Total Transactions", f"{total_transactions}")
    with col3:
        st.metric("Average Transaction Value", f"${avg_transaction_value:,.2f}")
    st.write(f"Unique Products Sold: {unique_products}")
    st.write(f"Unique Store Locations: {unique_locations}")

    # Sales Trends with toggle for daily, weekly, or monthly
    st.write("## Sales Trends")
    trend_option = st.selectbox("Select Trend Frequency", ["Daily", "Weekly", "Monthly"])

    if trend_option == "Daily":
        sales_trend = filtered_data.groupby(filtered_data['transaction_date'].dt.date)['total_sales'].sum()
        title = "Daily Sales Trend"
        x_title = "Date"
    elif trend_option == "Weekly":
        sales_trend = filtered_data.set_index('transaction_date').resample('W')['total_sales'].sum()
        title = "Weekly Sales Trend"
        x_title = "Week"
    else:
        sales_trend = filtered_data.set_index('transaction_date').resample('M')['total_sales'].sum()
        title = "Monthly Sales Trend"
        x_title = "Month"

    fig = px.line(sales_trend, x=sales_trend.index, y=sales_trend.values, labels={"x": x_title, "y": "Total Sales ($)"}, title=title)
    st.plotly_chart(fig, use_container_width=True)

    # Sales by Product Category
    st.write("## Sales Breakdown by Product Category and Type")
    col4, col5 = st.columns(2)

    with col4:
        # Interactive pie chart for product category sales distribution
        category_sales = filtered_data.groupby('product_category')['total_sales'].sum()
        fig = px.pie(
            category_sales,
            values=category_sales.values,
            names=category_sales.index,
            title="Sales Distribution by Product Category",
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)

    with col5:
        # Top product types in selected categories
        top_product_types = filtered_data.groupby('product_type')['total_sales'].sum().nlargest(10)
        fig = px.bar(
            top_product_types,
            x=top_product_types.values,
            y=top_product_types.index,
            orientation='h',
            title="Top 10 Product Types by Sales",
            labels={"x": "Total Sales ($)", "y": "Product Type"}
        )
        st.plotly_chart(fig, use_container_width=True)

    # Comparison of Sales by Store Location with sorting
    st.write("## Sales by Store Location")
    location_sales = filtered_data.groupby('store_location')['total_sales'].sum().sort_values(ascending=False)
    location_sort_option = st.radio("Sort Locations by:", ["Highest Sales", "Lowest Sales"])

    if location_sort_option == "Lowest Sales":
        location_sales = location_sales.sort_values(ascending=True)

    fig = px.bar(
        location_sales,
        x=location_sales.values,
        y=location_sales.index,
        orientation='h',
        title="Sales by Store Location",
        labels={"x": "Total Sales ($)", "y": "Store Location"}
    )
    st.plotly_chart(fig, use_container_width=True)

    # Heatmap for Location-based Analysis (Sales by Product Category and Location)
    st.write("## Location-Based Sales by Product Category")
    location_category_sales = filtered_data.pivot_table(
        index='store_location',
        columns='product_category',
        values='total_sales',
        aggfunc='sum',
        fill_value=0
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(location_category_sales, annot=True, fmt=".0f", cmap="YlGnBu", linewidths=0.5, ax=ax)
    ax.set_title("Sales by Product Category and Store Location")
    ax.set_xlabel("Product Category")
    ax.set_ylabel("Store Location")
    st.pyplot(fig)

    # Additional Insights (Top 5 Products and Average Sales per Day of the Week)
    st.write("## Additional Insights")
    col6, col7 = st.columns(2)

    # Top 5 Products by Sales Volume with filtering
    with col6:
        top_products = filtered_data.groupby('product_detail')['transaction_qty'].sum().nlargest(5)
        fig = px.bar(
            top_products,
            x=top_products.values,
            y=top_products.index,
            orientation='h',
            title="Top 5 Products by Quantity Sold",
            labels={"x": "Quantity Sold", "y": "Product"}
        )
        st.plotly_chart(fig, use_container_width=True)

    # Average Sales by Day of the Week
    with col7:
        filtered_data['day_of_week'] = filtered_data['transaction_date'].dt.day_name()
        weekday_sales = filtered_data.groupby('day_of_week')['total_sales'].mean().reindex(
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        )

        fig = px.bar(
            weekday_sales,
            x=weekday_sales.index,
            y=weekday_sales.values,
            title="Average Sales by Day of the Week",
            labels={"x": "Day of the Week", "y": "Average Sales ($)"}
        )
        st.plotly_chart(fig, use_container_width=True)
