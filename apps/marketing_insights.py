import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("Marketing Insights")
    st.write("An interactive analysis of customer segmentation, purchase patterns, and trends.")

    # Load the dataset
    data = pd.read_csv("Cleaned_Coffee_Shop_Sales.csv")
    data['transaction_date'] = pd.to_datetime(data['transaction_date'])

    # Top Analysis Summary
    st.write("## Marketing Insights Summary")

    # Summary Metrics
    total_transactions = data['transaction_id'].nunique()
    total_sales = data['total_sales'].sum()
    avg_spend_per_transaction = total_sales / total_transactions

    st.write(f"""
    - **Total Transactions**: {total_transactions}
    - **Total Sales**: ${total_sales:,.2f}
    - **Average Spend per Transaction**: ${avg_spend_per_transaction:,.2f}
    """)

    # Customer Purchase Patterns
    st.write("## Customer Purchase Patterns")

    # Assuming 'total_sales' represents spending level
    spend_levels = pd.cut(data['total_sales'], bins=[0, 10, 50, 100, 500], labels=['Low', 'Medium', 'High', 'Premium'])
    data['spend_level'] = spend_levels

    # Interactive filter for spend levels
    selected_spend_level = st.selectbox("Select Spend Level", options=data['spend_level'].unique(), index=0)

    # Filter data by selected spend level
    segment_data = data[data['spend_level'] == selected_spend_level]

    # Identify top products for the selected spend level
    top_products = segment_data.groupby('product_detail')['transaction_qty'].sum().sort_values(ascending=False).head(10).reset_index()

    st.write(f"### Top Products for {selected_spend_level} Spenders")
    fig = px.bar(
        top_products,
        x='transaction_qty',
        y='product_detail',
        orientation='h',
        labels={"transaction_qty": "Quantity Sold", "product_detail": "Product"},
        title=f"Top 10 Products Purchased by {selected_spend_level} Spenders",
        color='transaction_qty',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Additional Marketing Insights
    st.write("## Additional Marketing Insights")
    st.write(f"""
    - **Customer purchase patterns** provide insights into top products by spend level, useful for targeted recommendations.
    """)
