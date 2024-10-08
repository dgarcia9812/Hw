import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")


# Question 1: Category selection
option = st.selectbox(
    "Which category would you like?",
    ("Furniture", "Office Supplies", "Technology"),
)

# Question 2: Subcategory multiselect
options = st.multiselect(
    "What is the subcategory?",
    ["Chairs", "Tables", "Binders", "Accessories","Bookcase", "Furnishings", "Envelopes", "Art", "Papers", "Phones"],
)

st.write("You selected:", options)

# Filter the data based on selected category and subcategories
filtered_data = df[(df['Category'] == option) & (df['Sub_Category'].isin(options))]


# 3 - Line chart of sales for selected sub-categories
# Section: Sales Trend Visualization
st.write("### Sales Trend Visualization")
if not filtered_data.empty:
    sales_by_month_filtered = filtered_data.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
    st.line_chart(sales_by_month_filtered, y="Sales")

  # 4 - Metrics for selected subcategories: Total Sales, Total Profit, and Profit Margin
    total_sales = filtered_data['Sales'].sum()
    total_profit = filtered_data['Profit'].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

    st.write("### Metrics for Selected Sub_Categories")
    st.metric("Total Sales", f"${total_sales:,.2f}")
    st.metric("Total Profit", f"${total_profit:,.2f}")
    st.metric("Profit Margin (%)", f"{profit_margin:.2f}%")

    # 5 - Overall profit margin and delta
    overall_sales = df['Sales'].sum()
    overall_profit = df['Profit'].sum()
    overall_profit_margin = (overall_profit / overall_sales) * 100 if overall_sales != 0 else 0

    # Show the delta value for profit margin compared to overall profit margin
    st.metric("Overall Profit Margin (%)", f"{profit_margin:.2f}%", delta=f"{(profit_margin - overall_profit_margin):.2f}%")
else:
    st.write("Please select at least one subcategory to view the data.")












    


