import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
from datetime import timedelta


def app():
    st.title("Forecasting and Predictive Analysis")
    st.write("An interactive analysis of sales forecasting, demand prediction, and peak time projections.")

    # Load the dataset
    data = pd.read_csv("Cleaned_Coffee_Shop_Sales.csv")
    data['transaction_date'] = pd.to_datetime(data['transaction_date'])

    # Prepare data for forecasting
    sales_data = data.groupby('transaction_date')['total_sales'].sum().reset_index()

    # Analysis Summary
    st.write("## Forecasting Analysis Summary")

    # Calculate summary metrics
    total_sales = sales_data['total_sales'].sum()
    avg_daily_sales = sales_data['total_sales'].mean()
    last_sales_date = sales_data['transaction_date'].max()

    st.write(f"""
    - **Total Sales (Historical)**: ${total_sales:,.2f}
    - **Average Daily Sales**: ${avg_daily_sales:,.2f}
    - **Last Date of Historical Data**: {last_sales_date.strftime('%Y-%m-%d')}
    """)

    # Forecasting Sales with ARIMA
    st.write("## Sales Forecasting (Next 30 Days)")

    # Set up ARIMA model for the total sales time series
    sales_series = sales_data.set_index('transaction_date')['total_sales']
    model = ARIMA(sales_series, order=(5, 1, 0))  # ARIMA model with order (5,1,0)
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=30)  # Forecast for the next 30 days

    # Create a DataFrame for forecasted values
    forecast_dates = pd.date_range(start=last_sales_date + timedelta(days=1), periods=30, freq='D')
    forecast_df = pd.DataFrame({'transaction_date': forecast_dates, 'forecast_sales': forecast})

    # Plot historical sales and forecasted sales
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sales_data['transaction_date'], y=sales_data['total_sales'], mode='lines',
                             name='Historical Sales'))
    fig.add_trace(go.Scatter(x=forecast_df['transaction_date'], y=forecast_df['forecast_sales'], mode='lines',
                             name='Forecasted Sales', line=dict(dash='dash')))
    fig.update_layout(
        title="30-Day Sales Forecast",
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        legend_title="Legend"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Predicted Demand for Key Products
    st.write("## Predicted Demand for Key Products")

    # Forecast demand for a specific product
    product = st.selectbox("Select Product for Demand Forecasting", data['product_detail'].unique())
    product_data = data[data['product_detail'] == product].groupby('transaction_date')[
        'transaction_qty'].sum().reset_index()

    # Set up ARIMA model for product demand time series
    product_series = product_data.set_index('transaction_date')['transaction_qty']
    product_model = ARIMA(product_series, order=(5, 1, 0))  # ARIMA model for product demand
    product_model_fit = product_model.fit()
    product_forecast = product_model_fit.forecast(steps=30)  # Forecast for the next 30 days

    # Create a DataFrame for product forecasted demand
    product_forecast_df = pd.DataFrame({'transaction_date': forecast_dates, 'forecast_demand': product_forecast})

    # Plot historical demand and forecasted demand for the selected product
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=product_data['transaction_date'], y=product_data['transaction_qty'], mode='lines',
                             name='Historical Demand'))
    fig.add_trace(
        go.Scatter(x=product_forecast_df['transaction_date'], y=product_forecast_df['forecast_demand'], mode='lines',
                   name='Forecasted Demand', line=dict(dash='dash')))
    fig.update_layout(
        title=f"30-Day Demand Forecast for {product}",
        xaxis_title="Date",
        yaxis_title="Demand (Units)",
        legend_title="Legend"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Projected Peak Times
    st.write("## Projected Peak Times")

    # Identify peak demand days in forecast
    forecast_peak_days = forecast_df[forecast_df['forecast_sales'] > forecast_df['forecast_sales'].quantile(0.9)]

    st.write("### Projected High-Demand Days (Top 10%)")
    st.dataframe(forecast_peak_days[['transaction_date', 'forecast_sales']].rename(
        columns={'transaction_date': 'Date', 'forecast_sales': 'Projected Sales ($)'}))

    # Additional Insights for Forecasting
    st.write("## Additional Insights for Forecasting")
    st.write(f"""
    - **30-Day Sales Forecast**: Indicates expected sales trends, which can guide inventory and staffing.
    - **Product Demand Forecast**: Helps anticipate demand for key products, improving supply planning.
    - **Peak Time Projections**: Identifies high-demand days, useful for resource allocation and promotional planning.
    """)

