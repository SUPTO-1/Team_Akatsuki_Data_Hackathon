import streamlit as st
from multiapp import MultiApp
from apps import (
    home,
    sales_overview,
    product_analysis,
    customer_behavior,
    location_performance,
    profitability_analysis,
    inventory_stock_analysis,
    customer_insights_and_loyalty,
    pricing_demand_analysis,
    forecasting_predictive_analysis,
    marketing_insights
)  # Import additional modules/pages as you create them

# Set up the page
st.set_page_config(page_title="Coffee Shop Dashboard", layout="wide")

# Display the Team Name in a Large Title
st.markdown("<h1 style='text-align: center; color: #FFD700;'>Team Akatsuki</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #6B8E23;'>Welcome to the Coffee Shop Dashboard</h2>",
            unsafe_allow_html=True)
st.markdown("---")

# Initialize MultiApp manager for navigation
app = MultiApp()

# Add pages with interactive descriptions
app.add_app("Home", home.app)
app.add_app("Sales Overview", sales_overview.app)
app.add_app("Product Analysis", product_analysis.app)
app.add_app("Customer Behavior", customer_behavior.app)
app.add_app("Location Performance", location_performance.app)
app.add_app("Profit Analysis", profitability_analysis.app)
app.add_app("Inventory Stock Analysis", inventory_stock_analysis.app)
app.add_app("Customer Insights And Loyalty", customer_insights_and_loyalty.app)
app.add_app("Pricing Demand Analysis", pricing_demand_analysis.app)
app.add_app("Forecasting Predictive Analysis", forecasting_predictive_analysis.app)
app.add_app("Marketing Insights", marketing_insights.app)


# Run the application
app.run()
