import streamlit as st
from multiapp import MultiApp
from apps import home, sales_overview, product_analysis, customer_behavior, location_performance, profitability_analysis, inventory_stock_analysis, customer_insights_and_loyalty, pricing_demand_analysis, forecasting_predictive_analysis, marketing_insights, introduction

# Set up Streamlit page configuration
st.set_page_config(page_title="Coffee Shop Dashboard", layout="wide")

# Create MultiApp instance
app = MultiApp()

# Add all pages, including the new Introduction page
app.add_app("Introduction", introduction.app)
app.add_app("Home", home.app)
app.add_app("Sales Overview", sales_overview.app)
app.add_app("Product Analysis", product_analysis.app)
app.add_app("Customer Behavior", customer_behavior.app)
app.add_app("Location Performance", location_performance.app)
app.add_app("Profitability Analysis", profitability_analysis.app)
app.add_app("Inventory Stock Analysis", inventory_stock_analysis.app)
app.add_app("Customer Insights And Loyalty", customer_insights_and_loyalty.app)
app.add_app("Pricing Demand Analysis", pricing_demand_analysis.app)
app.add_app("Forecasting Predictive Analysis", forecasting_predictive_analysis.app)
app.add_app("Marketing Insights", marketing_insights.app)

# Run the app
app.run()
