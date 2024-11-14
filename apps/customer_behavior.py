import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def app():
    st.title("Customer Behavior Analysis")
    st.write("Insights into customer purchase patterns, including peak hours, transaction values, and segmentation.")

    # Load the dataset
    data = pd.read_csv("Cleaned_Coffee_Shop_Sales.csv")
    data['transaction_date'] = pd.to_datetime(data['transaction_date'])
    data['transaction_hour'] = pd.to_datetime(data['transaction_time'], format='%H:%M:%S').dt.hour
    data['day_of_week'] = data['transaction_date'].dt.day_name()

    # Sidebar filter for Date Range
    st.sidebar.header("Filters")
    start_date = st.sidebar.date_input("Start Date", value=data['transaction_date'].min())
    end_date = st.sidebar.date_input("End Date", value=data['transaction_date'].max())
    filtered_data = data[(data['transaction_date'] >= pd.to_datetime(start_date)) &
                         (data['transaction_date'] <= pd.to_datetime(end_date))]

    # Peak Purchase Hours
    st.write("## Peak Purchase Times")
    col1, col2 = st.columns(2)

    with col1:
        hourly_sales = filtered_data.groupby('transaction_hour')['total_sales'].sum()
        fig = px.bar(hourly_sales, x=hourly_sales.index, y=hourly_sales.values,
                     labels={"x": "Hour of Day", "y": "Total Sales ($)"},
                     title="Total Sales by Hour of Day",
                     color=hourly_sales.values, color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        weekday_sales = filtered_data.groupby('day_of_week')['total_sales'].sum().reindex(
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        )
        fig = px.bar(weekday_sales, x=weekday_sales.index, y=weekday_sales.values,
                     labels={"x": "Day of the Week", "y": "Total Sales ($)"},
                     title="Total Sales by Day of the Week",
                     color=weekday_sales.values, color_continuous_scale='Greens')
        st.plotly_chart(fig, use_container_width=True)

    # Analysis of Average Basket Size and Transaction Value
    st.write("## Basket Size and Transaction Value Analysis")
    col3, col4 = st.columns(2)

    # Basket Size Distribution
    with col3:
        basket_sizes = filtered_data.groupby('transaction_id')['transaction_qty'].sum()
        fig = px.histogram(basket_sizes, x=basket_sizes.values, nbins=20,
                           labels={"x": "Items per Transaction", "y": "Frequency"},
                           title="Distribution of Basket Sizes",
                           color_discrete_sequence=['teal'])
        st.plotly_chart(fig, use_container_width=True)

    # Transaction Value Distribution
    with col4:
        transaction_values = filtered_data.groupby('transaction_id')['total_sales'].sum()
        fig = px.histogram(transaction_values, x=transaction_values.values, nbins=20,
                           labels={"x": "Transaction Value ($)", "y": "Frequency"},
                           title="Distribution of Transaction Values",
                           color_discrete_sequence=['orange'])
        st.plotly_chart(fig, use_container_width=True)

    # Transaction-Based Segmentation Based on Spending Behavior
    st.write("## Transaction Segmentation")

    # Use total sales per transaction for segmentation
    transaction_spending = filtered_data.groupby('transaction_id')['total_sales'].sum()

    # Define segmentation labels and bins based on transaction values
    bins = [0, 20, 100, 200, float('inf')]
    labels = ['Low Value', 'Moderate Value', 'High Value', 'Very High Value']
    transaction_segments = pd.cut(transaction_spending, bins=bins, labels=labels)

    # Count the number of transactions in each segment
    segment_counts = transaction_segments.value_counts().reindex(labels)

    # Pie chart for transaction segment distribution
    fig = px.pie(
        values=segment_counts.values,
        names=segment_counts.index,
        title="Transaction Segmentation by Value",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Sunset
    )
    st.plotly_chart(fig, use_container_width=True)

    # Average Transaction Value by Segment
    avg_transaction_value_by_segment = transaction_spending.groupby(transaction_segments).mean()
    fig = px.bar(
        avg_transaction_value_by_segment,
        x=avg_transaction_value_by_segment.index,
        y=avg_transaction_value_by_segment.values,
        labels={"y": "Average Transaction Value ($)", "x": "Transaction Segment"},
        title="Average Transaction Value by Segment",
        color=avg_transaction_value_by_segment.values,
        color_continuous_scale='Bluered'
    )
    st.plotly_chart(fig, use_container_width=True)
