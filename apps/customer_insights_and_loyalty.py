import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("Customer Insights and Loyalty Analysis (Transaction-Based)")
    st.write("An interactive analysis of transaction patterns, focusing on popular products and transaction trends.")

    # Load the dataset
    data = pd.read_csv("Cleaned_Coffee_Shop_Sales.csv")
    data['transaction_date'] = pd.to_datetime(data['transaction_date'])

    # Popular Products in Transactions
    st.write("## Popular Products in Transactions")
    popular_products = data.groupby('product_detail')['transaction_qty'].sum().sort_values(ascending=False).head(10).reset_index()

    fig = px.bar(
        popular_products,
        x='transaction_qty',
        y='product_detail',
        orientation='h',
        labels={"transaction_qty": "Quantity Sold", "product_detail": "Product"},
        title="Top 10 Products in Transactions",
        color='transaction_qty',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Monthly Transaction Trends
    st.write("## Monthly Transaction Trends")
    data['year_month'] = data['transaction_date'].dt.to_period('M').astype(str)  # Convert Period to string for compatibility
    monthly_transactions = data.groupby('year_month')['transaction_id'].nunique().reset_index()

    fig = px.line(
        monthly_transactions,
        x='year_month',
        y='transaction_id',
        labels={"year_month": "Month", "transaction_id": "Unique Transaction Count"},
        title="Monthly Unique Transaction Trends",
        markers=True,
        line_shape='linear'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Additional Insights on Transaction-Based Loyalty
    st.write("## Additional Transaction Insights")
    st.write(f"""
    - **Top 10 popular products in transactions** highlight frequently bought items, which can inform promotional strategies.
    - **Monthly transaction trends** reveal seasonal trends or peak periods in transaction frequency, which can guide inventory and marketing efforts.
    """)
