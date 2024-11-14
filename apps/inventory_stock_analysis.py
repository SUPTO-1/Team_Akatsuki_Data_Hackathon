import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def app():
    st.title("Inventory & Stock Analysis")
    st.write("An interactive analysis of inventory metrics, including monthly demand, seasonal patterns, turnover rate, and demand forecasting.")

    # Load the dataset
    data = pd.read_csv("Cleaned_Coffee_Shop_Sales.csv")
    data['transaction_date'] = pd.to_datetime(data['transaction_date'])

    # Sidebar filter for Product Category selection
    st.sidebar.header("Product Category Filter")
    selected_category = st.sidebar.selectbox("Select a Product Category", data['product_category'].unique())

    # Filter data for the selected category
    category_data = data[data['product_category'] == selected_category]

    # Add Year-Month column for monthly aggregation
    category_data['year_month'] = category_data['transaction_date'].dt.to_period('M')

    # Top Analysis Summary
    st.write("## Inventory Analysis Summary")
    total_demand = category_data['transaction_qty'].sum()
    monthly_demand_avg = category_data.groupby('year_month')['transaction_qty'].sum().mean()
    inventory_turnover_rate = total_demand / category_data['transaction_id'].nunique()  # Simplified turnover calculation

    st.write(f"""
    - **Total Demand for {selected_category}**: {total_demand} units
    - **Average Monthly Demand**: {monthly_demand_avg:.2f} units
    - **Inventory Turnover Rate**: {inventory_turnover_rate:.2f} (units per transaction)
    """)

    # Monthly Product Demand
    st.write("## Monthly Product Demand for Stock Requirements")
    monthly_demand = category_data.groupby('year_month')['transaction_qty'].sum().reset_index()
    monthly_demand['year_month'] = monthly_demand['year_month'].astype(str)  # Convert for Plotly compatibility
    fig = px.line(
        monthly_demand,
        x='year_month',
        y='transaction_qty',
        labels={"year_month": "Month", "transaction_qty": "Total Demand (units)"},
        title=f"Monthly Product Demand for {selected_category}",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

    # Seasonal Demand Patterns
    st.write("## Seasonal Demand Patterns")
    category_data['month'] = category_data['transaction_date'].dt.month
    seasonal_demand = category_data.groupby('month')['transaction_qty'].sum().reset_index()

    fig = px.bar(
        seasonal_demand,
        x='month',
        y='transaction_qty',
        labels={"month": "Month", "transaction_qty": "Total Demand (units)"},
        title=f"Seasonal Demand Patterns for {selected_category}",
        color='transaction_qty',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Inventory Turnover Rate Visualization
    st.write("## Inventory Turnover Rate Analysis")
    turnover_rate_data = category_data.groupby('product_type').agg({
        'transaction_qty': 'sum',
        'transaction_id': 'nunique'
    })
    turnover_rate_data['turnover_rate'] = turnover_rate_data['transaction_qty'] / turnover_rate_data['transaction_id']
    turnover_rate_data = turnover_rate_data.sort_values(by='turnover_rate', ascending=False)

    fig = px.bar(
        turnover_rate_data,
        x=turnover_rate_data.index,
        y='turnover_rate',
        labels={"x": "Product Type", "turnover_rate": "Turnover Rate (units per transaction)"},
        title=f"Inventory Turnover Rate by Product Type for {selected_category}",
        color='turnover_rate',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Demand Forecasting using a Simple Moving Average
    st.write("## Demand Forecasting")
    monthly_demand['demand_forecast'] = monthly_demand['transaction_qty'].rolling(window=3).mean()  # 3-month moving average

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_demand['year_month'],
        y=monthly_demand['transaction_qty'],
        mode='lines+markers',
        name='Actual Demand',
        line=dict(color='blue')
    ))
    fig.add_trace(go.Scatter(
        x=monthly_demand['year_month'],
        y=monthly_demand['demand_forecast'],
        mode='lines',
        name='Forecast (3-Month Moving Average)',
        line=dict(color='orange', dash='dash')
    ))
    fig.update_layout(
        title=f"Demand Forecasting for {selected_category}",
        xaxis_title="Month",
        yaxis_title="Demand (units)",
        legend_title="Legend"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Additional Insights on Inventory Needs
    st.write("## Inventory Planning Insights")
    peak_month = seasonal_demand.loc[seasonal_demand['transaction_qty'].idxmax(), 'month']
    st.write(f"**Peak Demand Month**: {peak_month} (Plan for higher inventory requirements during this period)")
    st.write(f"The **average turnover rate** for {selected_category} is {inventory_turnover_rate:.2f} units per transaction, indicating the frequency at which inventory is cycled.")

