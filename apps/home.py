import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def app():
    st.title("Coffee Shop Sales Dashboard")
    st.write(
        "Welcome to the Coffee Shop Sales Dashboard! Get insights into sales trends, product performance, and customer behaviors across all store locations.")

    # Load the dataset
    data = pd.read_csv("Cleaned_Coffee_Shop_Sales.csv")
    data['transaction_date'] = pd.to_datetime(data['transaction_date'])

    # Sidebar filters for interactivity
    st.sidebar.header("Filter Options")
    category_options = data['product_category'].unique()
    selected_category = st.sidebar.selectbox("Product Category", category_options)

    # Date Range Filter
    st.sidebar.subheader("Select Date Range")
    start_date = st.sidebar.date_input("Start Date", data['transaction_date'].min())
    end_date = st.sidebar.date_input("End Date", data['transaction_date'].max())

    # Filter data based on sidebar selections
    filtered_data = data[(data['product_category'] == selected_category) &
                         (data['transaction_date'] >= pd.to_datetime(start_date)) &
                         (data['transaction_date'] <= pd.to_datetime(end_date))]

    # Display key metrics for the selected category and date range
    st.write(f"## Key Metrics for {selected_category} Category")
    total_sales = filtered_data['total_sales'].sum()
    total_transactions = filtered_data['transaction_id'].nunique()
    avg_transaction_value = filtered_data['total_sales'].mean()
    unique_products = filtered_data['product_id'].nunique()

    col1, col2 = st.columns(2)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col1.metric("Total Transactions", f"{total_transactions}")
    col2.metric("Average Transaction Value", f"${avg_transaction_value:,.2f}")
    col2.metric("Unique Products", f"{unique_products}")

    # Monthly Sales Trend
    st.write(f"## Monthly Sales Trend for {selected_category}")
    monthly_sales = filtered_data.groupby(filtered_data['transaction_date'].dt.to_period("M")).agg(
        {"total_sales": "sum"}).reset_index()
    monthly_sales['transaction_date'] = monthly_sales[
        'transaction_date'].dt.to_timestamp()  # Convert period to timestamp for plotting

    fig = px.line(monthly_sales, x='transaction_date', y='total_sales',
                  labels={"transaction_date": "Month", "total_sales": "Total Sales ($)"},
                  title="Monthly Sales Trend",
                  markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # Two-column layout for additional insights
    col3, col4 = st.columns(2)

    with col3:
        # Sales Distribution by Product Detail
        st.write(f"### Sales Distribution by Product Detail in {selected_category}")
        product_sales = filtered_data.groupby('product_detail')['total_sales'].sum().reset_index()
        fig = px.bar(product_sales, x='total_sales', y='product_detail',
                     labels={"total_sales": "Total Sales ($)", "product_detail": "Product"},
                     title=f"Sales by Product Detail in {selected_category}",
                     orientation='h')
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        # Peak Sales Hours for selected category
        st.write(f"### Peak Sales Hours in {selected_category}")
        filtered_data['transaction_hour'] = pd.to_datetime(filtered_data['transaction_time'], format='%H:%M:%S').dt.hour
        hourly_sales = filtered_data.groupby('transaction_hour')['total_sales'].sum().reset_index()
        fig = px.bar(hourly_sales, x='transaction_hour', y='total_sales',
                     labels={"transaction_hour": "Hour of the Day", "total_sales": "Total Sales ($)"},
                     title="Sales Volume by Hour")
        st.plotly_chart(fig, use_container_width=True)

    # Pie Chart for Sales by Product Type
    st.write(f"## Sales Breakdown by Product Type in {selected_category}")
    product_type_sales = filtered_data.groupby('product_type')['total_sales'].sum().reset_index()
    fig = px.pie(product_type_sales, values='total_sales', names='product_type',
                 title=f"Sales Breakdown by Product Type in {selected_category}",
                 hole=0.3)
    st.plotly_chart(fig, use_container_width=True)

    # Top 5 Products by Sales Volume for selected category
    st.write(f"## Top 5 Products by Sales Volume in {selected_category}")
    top_products = filtered_data.groupby('product_detail')['transaction_qty'].sum().nlargest(5).reset_index()
    fig = px.bar(top_products, x='transaction_qty', y='product_detail',
                 orientation='h', labels={"transaction_qty": "Quantity Sold", "product_detail": "Product"},
                 title=f"Top 5 Products by Quantity Sold in {selected_category}")
    st.plotly_chart(fig, use_container_width=True)

    st.write("### Explore More")
    st.markdown("""
    - **[Sales Overview](#)**: View detailed sales metrics across time, location, and products.
    - **[Product Analysis](#)**: Analyze the performance of individual products and categories.
    - **[Customer Behavior](#)**: Get insights into customer purchase patterns.
    - **[Location Performance](#)**: Compare the performance of different store locations.
    """)

