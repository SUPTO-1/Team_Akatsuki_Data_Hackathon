import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def app():
    st.title("Product Analysis")
    st.write("Detailed insights into product performance, including categories, types, pricing, and popularity.")

    # Load the dataset
    data = pd.read_csv("Cleaned_Coffee_Shop_Sales.csv")
    data['transaction_date'] = pd.to_datetime(data['transaction_date'])

    # Sidebar Filters
    st.sidebar.header("Filters")
    product_category_options = data['product_category'].unique()
    selected_category = st.sidebar.selectbox("Select a Product Category", product_category_options, index=0)

    # Filter data based on selected product category
    category_data = data[data['product_category'] == selected_category]

    # Key Metrics
    st.write(f"## Key Metrics for {selected_category}")
    total_revenue = category_data['total_sales'].sum()
    total_quantity = category_data['transaction_qty'].sum()
    unique_products = category_data['product_id'].nunique()
    avg_unit_price = category_data['unit_price'].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Total Quantity Sold", f"{total_quantity}")
    col3.metric("Unique Products", f"{unique_products}")
    col4.metric("Average Unit Price", f"${avg_unit_price:.2f}")

    # Product Popularity and Revenue Contribution
    st.write(f"## {selected_category} Product Popularity and Revenue Contribution")
    col5, col6 = st.columns(2)

    with col5:
        # Top 10 Products by Quantity Sold
        top_products_qty = category_data.groupby('product_detail')['transaction_qty'].sum().nlargest(10)
        fig = px.bar(
            top_products_qty,
            x=top_products_qty.values,
            y=top_products_qty.index,
            orientation='h',
            title="Top 10 Products by Quantity Sold",
            labels={"x": "Quantity Sold", "y": "Product"},
            color=top_products_qty.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        # Top 10 Products by Revenue
        top_products_revenue = category_data.groupby('product_detail')['total_sales'].sum().nlargest(10)
        fig = px.bar(
            top_products_revenue,
            x=top_products_revenue.values,
            y=top_products_revenue.index,
            orientation='h',
            title="Top 10 Products by Revenue",
            labels={"x": "Revenue ($)", "y": "Product"},
            color=top_products_revenue.values,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Pricing Distribution
    st.write(f"## Pricing Distribution for {selected_category}")
    fig = px.histogram(
        category_data,
        x='unit_price',
        nbins=20,
        title="Unit Price Distribution",
        labels={"unit_price": "Unit Price ($)"},
        color_discrete_sequence=['teal']
    )
    st.plotly_chart(fig, use_container_width=True)

    # Analysis of Coffee Product Types (if Coffee is a focal category)
    if selected_category == "Coffee":
        st.write("## Analysis of Coffee Product Types")
        col7, col8 = st.columns(2)

        # Sales Volume by Coffee Type
        coffee_sales_by_type = category_data.groupby('product_type')['transaction_qty'].sum().sort_values()
        fig = px.bar(
            coffee_sales_by_type,
            x=coffee_sales_by_type.values,
            y=coffee_sales_by_type.index,
            orientation='h',
            title="Sales Volume by Coffee Type",
            labels={"x": "Quantity Sold", "y": "Coffee Type"},
            color=coffee_sales_by_type.values,
            color_continuous_scale='Reds'
        )
        col7.plotly_chart(fig, use_container_width=True)

        # Unit Price Trends by Coffee Type
        avg_price_by_type = category_data.groupby('product_type')['unit_price'].mean().sort_values()
        fig = px.bar(
            avg_price_by_type,
            x=avg_price_by_type.values,
            y=avg_price_by_type.index,
            orientation='h',
            title="Average Unit Price by Coffee Type",
            labels={"x": "Average Price ($)", "y": "Coffee Type"},
            color=avg_price_by_type.values,
            color_continuous_scale='Purples'
        )
        col8.plotly_chart(fig, use_container_width=True)

    # Additional Insights: Revenue Contribution by Product Type
    st.write(f"## Revenue Contribution by {selected_category} Product Types")
    product_type_revenue = category_data.groupby('product_type')['total_sales'].sum()

    fig = px.pie(
        product_type_revenue,
        values=product_type_revenue.values,
        names=product_type_revenue.index,
        title="Revenue Contribution by Product Type",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Sunset
    )
    st.plotly_chart(fig, use_container_width=True)

    # Most Expensive Products in the Category
    st.write(f"## Most Expensive Products in {selected_category}")

    # Filter and sort to get the top 10 most expensive products
    most_expensive_products = (
        category_data[['product_detail', 'unit_price']]
        .sort_values(by='unit_price', ascending=False)
        .drop_duplicates(subset='product_detail')
        .head(10)
    )

    # Plotting the data in a bar chart
    fig = px.bar(
        most_expensive_products,
        x='unit_price',
        y='product_detail',
        orientation='h',
        title="Top 10 Most Expensive Products",
        labels={"unit_price": "Unit Price ($)", "product_detail": "Product"},
        color='unit_price',
        color_continuous_scale='reds'
    )
    st.plotly_chart(fig, use_container_width=True)
