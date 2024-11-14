import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("Profitability Analysis by Product Type and Category")
    st.write("An in-depth analysis of profit generation across products, with average cost per product type for the selected category.")

    # Load the dataset
    data = pd.read_csv("Cleaned_Coffee_Shop_Sales.csv")
    data['transaction_date'] = pd.to_datetime(data['transaction_date'])

    # Calculate cost and profit based on average cost and total sales
    data['cost'] = data['average_cost'] * data['transaction_qty']
    data['profit'] = data['total_sales'] - data['cost']

    # Sidebar for Product Category selection
    st.sidebar.header("Product Category Filter")
    selected_category = st.sidebar.selectbox("Select a Product Category", data['product_category'].unique())

    # Filter data based on the selected category
    category_data = data[data['product_category'] == selected_category]

    # Display Average Cost Table for Selected Category
    st.write(f"### Average Cost per Product Type in {selected_category}")
    cost_table = category_data[['product_type', 'average_cost']].drop_duplicates().sort_values(by='product_type')
    st.table(cost_table.rename(columns={"product_type": "Product Type", "average_cost": "Average Cost ($)"}))

    # Profit Analysis for Selected Category
    st.write(f"### Profit Analysis for Product Types in {selected_category}")
    profit_analysis = category_data.groupby('product_type').agg({
        'total_sales': 'sum',
        'cost': 'sum',
        'profit': 'sum',
        'transaction_qty': 'sum'
    })
    profit_analysis['avg_cost_per_unit'] = profit_analysis['cost'] / profit_analysis['transaction_qty']
    profit_analysis['profit_margin'] = (profit_analysis['profit'] / profit_analysis['total_sales']) * 100

    # Display profit analysis table
    st.dataframe(profit_analysis[['total_sales', 'cost', 'profit', 'profit_margin']].rename(
        columns={
            'total_sales': 'Total Sales ($)',
            'cost': 'Total Cost ($)',
            'profit': 'Total Profit ($)',
            'profit_margin': 'Profit Margin (%)'
        }
    ))

    # Profit and Cost Comparison Visualization for Selected Category
    st.write(f"## Profit and Cost Comparison by Product Type for {selected_category}")
    fig = px.bar(
        profit_analysis,
        x=profit_analysis.index,
        y=['cost', 'profit'],
        labels={"value": "Amount ($)", "variable": "Metric", "x": "Product Type"},
        title=f"Cost and Profit by Product Type in {selected_category}",
        barmode='group',
        color_discrete_sequence=['blue', 'green']
    )
    st.plotly_chart(fig, use_container_width=True)

    # Additional Analysis Information
    st.write("## Analysis Summary")
    total_sales = profit_analysis['total_sales'].sum()
    total_cost = profit_analysis['cost'].sum()
    total_profit = profit_analysis['profit'].sum()
    avg_profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

    st.markdown(f"""
    - **Total Sales for {selected_category}**: ${total_sales:,.2f}
    - **Total Cost for {selected_category}**: ${total_cost:,.2f}
    - **Total Profit for {selected_category}**: ${total_profit:,.2f}
    - **Average Profit Margin for {selected_category}**: {avg_profit_margin:.2f}%
    """)

    # High-Demand, Low-Profit Products
    st.write("## High-Demand, Low-Profit Products")
    demand_profit_data = category_data.groupby('product_detail').agg({
        'transaction_qty': 'sum',
        'profit': 'sum'
    })
    demand_profit_data['profit_per_unit'] = demand_profit_data['profit'] / demand_profit_data['transaction_qty']
    high_demand_low_profit = demand_profit_data[(demand_profit_data['transaction_qty'] > demand_profit_data['transaction_qty'].mean()) &
                                                (demand_profit_data['profit_per_unit'] < demand_profit_data['profit_per_unit'].mean())]

    fig = px.scatter(
        high_demand_low_profit,
        x='transaction_qty',
        y='profit',
        size='transaction_qty',
        color='profit_per_unit',
        labels={"transaction_qty": "Demand (Units Sold)", "profit": "Total Profit ($)", "profit_per_unit": "Profit per Unit"},
        title="High-Demand, Low-Profit Products",
        hover_data={'profit_per_unit': ':.2f'},
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Demand vs. Profitability Scatter Plot for All Products
    st.write("## Demand vs. Profitability for All Products in Category")
    fig = px.scatter(
        demand_profit_data,
        x='transaction_qty',
        y='profit_per_unit',
        size='profit',
        color='profit',
        labels={"transaction_qty": "Demand (Units Sold)", "profit_per_unit": "Profit per Unit", "profit": "Total Profit ($)"},
        title="Demand vs. Profitability by Product in Category",
        hover_data={'profit': ':.2f'},
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)
