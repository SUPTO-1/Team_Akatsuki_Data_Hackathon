import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def app():
    st.title("Pricing & Demand Analysis")
    st.write("An interactive analysis of demand elasticity, optimal pricing, and price sensitivity across products.")

    # Load the dataset
    data = pd.read_csv("Cleaned_Coffee_Shop_Sales.csv")
    data['transaction_date'] = pd.to_datetime(data['transaction_date'])

    # Sidebar Filters
    st.sidebar.header("Filters")
    product_category = st.sidebar.selectbox("Select Product Category", data['product_category'].unique())
    product_filter = st.sidebar.multiselect("Select Products", options=data[data['product_category'] == product_category]['product_detail'].unique(), default=None)
    min_price, max_price = st.sidebar.slider("Select Price Range", float(data['unit_price'].min()), float(data['unit_price'].max()), (float(data['unit_price'].min()), float(data['unit_price'].max())))

    # Filter data based on sidebar inputs
    pricing_data = data[(data['product_category'] == product_category) &
                        (data['unit_price'] >= min_price) &
                        (data['unit_price'] <= max_price)]
    if product_filter:
        pricing_data = pricing_data[pricing_data['product_detail'].isin(product_filter)]

    # Analysis Summary
    st.write("## Pricing & Demand Analysis Summary")

    avg_price = pricing_data['unit_price'].mean()
    max_price = pricing_data['unit_price'].max()
    min_price = pricing_data['unit_price'].min()
    total_demand = pricing_data['transaction_qty'].sum()

    st.write(f"""
    - **Selected Category**: {product_category}
    - **Average Price**: ${avg_price:.2f}
    - **Price Range**: ${min_price:.2f} - ${max_price:.2f}
    - **Total Demand**: {total_demand} units
    """)

    # Demand Elasticity by Price
    st.write("## Demand Elasticity by Price")
    price_demand = pricing_data.groupby('unit_price')['transaction_qty'].sum().reset_index()

    fig = px.line(
        price_demand,
        x='unit_price',
        y='transaction_qty',
        labels={"unit_price": "Unit Price ($)", "transaction_qty": "Total Demand (Units)"},
        title="Demand Elasticity: How Demand Changes with Price",
        markers=True,
        line_shape="spline"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Elasticity Calculation and Analysis
    price_demand['demand_elasticity'] = price_demand['transaction_qty'].pct_change() / price_demand['unit_price'].pct_change()
    avg_elasticity = price_demand['demand_elasticity'].mean()

    st.write("### Demand Elasticity Insights")
    st.write(f"- **Average Elasticity**: {avg_elasticity:.2f} (Values >1 indicate elastic demand; <1 indicate inelastic demand)")
    st.write(f"- **Elasticity Analysis**: Higher elasticity suggests that demand is highly sensitive to price changes in the selected range.")

    # Optimal Pricing Points
    st.write("## Optimal Pricing Points")
    product_avg_prices = pricing_data.groupby('product_detail').agg({'unit_price': 'mean', 'transaction_qty': 'sum'}).reset_index()

    fig = px.scatter(
        product_avg_prices,
        x='unit_price',
        y='transaction_qty',
        labels={"unit_price": "Average Unit Price ($)", "transaction_qty": "Total Demand (Units)"},
        title="Optimal Pricing Points for Different Products",
        color='transaction_qty',
        size='transaction_qty',
        hover_data={'product_detail': True},
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Price Sensitivity Analysis for Similar Products
    st.write("## Price Sensitivity Analysis for Selected Products")

    fig = px.scatter(
        pricing_data,
        x='unit_price',
        y='transaction_qty',
        color='product_detail',
        labels={"unit_price": "Unit Price ($)", "transaction_qty": "Demand (Units)"},
        title="Price Sensitivity Across Selected Products",
        size='transaction_qty',
        hover_data={'product_detail': True}
    )
    st.plotly_chart(fig, use_container_width=True)

    # Additional Insights for Pricing Optimization
    st.write("## Additional Insights for Pricing Optimization")
    st.write(f"""
    - **Demand elasticity** shows how sensitive demand is to price changes in the selected range.
    - **Optimal pricing points** highlight where demand peaks, which helps identify ideal price settings.
    - **Price sensitivity** analysis of similar products aids in competitive pricing within the category.
    """)
