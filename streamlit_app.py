import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from analysis_tools import abc_analysis, frm_analysis, visualize_abc, visualize_frm, frm_3d_scatter_with_segments
from io import StringIO
import plotly.express as px
import os

# Page configuration
st.set_page_config(page_title="Advanced Coffee Point Analysis", layout="wide", page_icon=":coffee:")

# Custom CSS
st.markdown("""
    <style>
        /* Ensure custom styling is properly applied */
        .custom-title {
            font-family: 'Arial', sans-serif;
            color: #2E8B57 !important; /* Green color */
            font-size: 34px;
            text-align: center;
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1); /* Optional shadow */
        }
        [data-testid="stSidebar"] {
            background-image: url("https://images.unsplash.com/photo-1690983325598-dd23fcf8f835?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Y29mZmVlJTIwdG9wJTIwdmlld3xlbnwwfHwwfHx8MA%3D%3D");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            color: white;
        } 
        .main {
        background-color: #f5f5f5;
        background-size: cover;
        background-position: center; 
        }
    </style>""", unsafe_allow_html=True)

# Title and Introduction - Only shown initially
st.markdown("<h1 class='custom-title'>Coffee Point Analysis Application</h1>", unsafe_allow_html=True)
st.components.v1.html(""" <script>
    var decoration = window.parent.document.querySelectorAll('[data-testid="stDecoration"]')[0];
    var sidebar = window.parent.document.querySelectorAll('[data-testid="stSidebar"]')[0];
    function outputsize() {
        decoration.style.left = `${sidebar.offsetWidth}px`;
    }
    new ResizeObserver(outputsize).observe(sidebar);
    outputsize();
    decoration.style.height = "3.0rem";
    decoration.style.right = "45px";
    decoration.style.backgroundImage = "url(https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZp73jURGSAYeFbobOinuGO58tQcQ0SEKwUg&s)";
    decoration.style.backgroundSize = "contain";
    </script> """, width=0, height=0)
# Sidebar Navigation
st.sidebar.header(":coffee: :blue[Navigation]")
menu = st.sidebar.radio("Go to", ["Topic", "Instruction", "Overview", "ABC Analysis", "FRM Analysis", "Insights","Conclusion"])

# File uploader
st.sidebar.subheader("Upload Your Data")
uploaded_file = st.sidebar.file_uploader(":red[Upload your CSV file]", type=["csv"])

# Ensure output directory exists
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
# Topic session
if menu == "Topic":
    # st.header(":star: Topic")
    st.subheader(":blue[Welcome to the] :red[Coffee Point Analysis Application].")     
    st.subheader(":blue[This tool allows you to:]")
    st.subheader(" :balloon: :blue[Analyze sales data using] :red[ABC Analysis] :blue[to identify key revenue-generating products.]  ")
    st.subheader(" :balloon: :blue[Segment customers using] :red[FRM Analysis] :blue[for targeted marketing strategies.]  ")
    st.subheader(" :balloon: :blue[Explore detailed insights into sales trends and customer behavior.]")
    st.header(" :rainbow[Upload your data and start exploring!]")
    
    def set_background(image_url):
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("{image_url}");
                background-size: 77% auto;
                background-position: right;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            .main {{
                background-color: rgba(255, 255, 255, 0.8);  # Adds a semi-transparent white overlay
            }}
            </style>""", unsafe_allow_html=True)
    # Call the function with your image URL
    set_background('https://coffeepoint.ae/wp-content/uploads/2022/08/image133.jpg')
    
# Instruction Section
if menu == "Instruction":
    st.header(":book: :blue[Instruction]")
    st.markdown("""
        **How to Use This Application**:
        1. Go to the **Overview** section to upload your CSV file.
        2. Explore:
            - **:red[ABC Analysis]** for identifying top products.
            - **:red[FRM Analysis]** for customer segmentation.
            - **:red[Insights]** for trends and deeper analysis.
        3. Navigate between sections using the sidebar.
        
        **CSV File Format**:
        - Ensure your file has the following columns:
            - `key`: Unique order identifier.
            - `item`: Product name.
            - `date`: Order date in `YYYY-MM-DD` format.
            - `price`: Price of the product.
            - `customer`: Customer ID.
    """)

# Home Section
if menu == "Overview":
    st.header(":coffee: :blue[Upload and View Data]")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        col1, col2, col3= st.columns([3.8,2,3.4])
        with col1:
            st.write("Dataset Preview")
            st.dataframe(df,hide_index =True)
        with col3:
            st.write("Quick Info")
            buffer = StringIO()
            df.info(buf=buffer)
            st.text(buffer.getvalue())
        with col2:
            st.write("Statistical Summary")
            st.dataframe(df.describe())
    else:
        st.warning("Please upload a CSV file.")

# ABC Analysis Section
if menu == "ABC Analysis":
    st.header(":chart_with_upwards_trend: :blue[ABC Analysis]")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        abc_results = abc_analysis(df)
        col1, col2 = st.columns([1.5, 2])
        with col1:
            st.write("ABC Analysis Table")
            st.dataframe(abc_results)
        with col2:
            abc_chart_path = os.path.join(output_dir, "abc_chart.png")
            visualize_abc(abc_results, abc_chart_path)
            st.image(abc_chart_path, caption="ABC Analysis Chart", use_column_width=True)

        st.subheader(":red[Key Insights]")
        total_sales = df["price"].sum()
        category_summary = abc_results.groupby("ABC")["price"].sum()
        for cat, value in category_summary.items():
            st.write(f"- Category {cat}: ${value:.2f} ({(value/total_sales)*100:.2f}%)")
    else:
        st.warning("Please upload a CSV file.")

# FRM Analysis Section
if menu == "FRM Analysis":
    st.header(":busts_in_silhouette: :blue[FRM Analysis]")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        frm_results = frm_analysis(df)
        col1, col2 = st.columns([1.5, 2])
        with col1:
            st.write("FRM Analysis Table")
            st.dataframe(frm_results)
        with col2:
            frm_chart_path = os.path.join(output_dir, "frm_chart.png")
            visualize_frm(frm_results, frm_chart_path)
            st.image(frm_chart_path, caption="FRM Analysis Chart", use_column_width=True)

        st.subheader(":red[Customer Segmentation Insights]")
        segment_counts = frm_results["Segment"].value_counts()
        for segment, count in segment_counts.items():
            st.write(f"- Segment {segment}: {count} customers")
    else:
        st.warning("Please upload a CSV file.")

# Insights Section
if menu == "Insights":
    st.header(":bar_chart: :blue[Additional Insights]")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df["date"] = pd.to_datetime(df["date"])
        
        # Extract 'month' and 'day_of_week' columns
        df['month'] = df['date'].dt.strftime('%B')  # Full month name
        df['day_of_week'] = df['date'].dt.strftime('%A')  # Full day name
        # Convert 'month' to a categorical type for proper ordering
        month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        df['month'] = pd.Categorical(df['month'], month_order, ordered=True)
        day_order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        df['day_of_week'] = pd.Categorical(df['day_of_week'],categories=day_order,ordered=True)
        
        st.subheader(":red[1. Sales Trends Over Time]")
        # Aggregate sales by month
        sales_trend = df.groupby("month")["price"].sum()
        # Plotting the sales trend
        fig, ax = plt.subplots(figsize=(4, 3))
        sales_trend.plot(kind="line", ax=ax, color="blue", marker='o',label="Monthly Sales")
        # ax.set_title("Monthly Sales Trend", fontsize=12)
        col1, col2 = st.columns([4.5,1])
        with col1:
            ax.set_xlabel("Month", fontsize=6)
            ax.set_ylabel("Total Sales ($)", fontsize=6)
            ax.set_xticks(range(12))
            ax.set_xticklabels(month_order, rotation=45, ha='right',fontsize=5)
            ax.tick_params(axis='y', labelsize=5)
            ax.grid(alpha=0.1)
            ax.legend(fontsize=4)
            st.pyplot(fig, use_container_width=False)
        # Auto-generated insight
        with col2:
            st.write(f"**:red[Insight]**: Total sales peaked in :orange[{sales_trend.idxmax()}], with :orange[${sales_trend.max():,.2f}] in revenue. The lowest sales occurred in :orange[{sales_trend.idxmin()}], with :orange[$${sales_trend.min():,.2f}].")
        
        st.subheader(":red[2. Transactions Trends Over Time]")
        # Aggregate sales by month
        transactions_trend = df.groupby("month")["price"].count()
        col1, col2 = st.columns([4.5,1])
        with col1:
            # Plotting the sales trend
            fig, ax = plt.subplots(figsize=(4, 3))
            transactions_trend.plot(kind="bar", ax=ax, color="coral", label="Monthly Transactions")
            # ax.set_title("Monthly Sales Trend", fontsize=12)
            ax.set_xlabel("Month", fontsize=6)
            ax.set_ylabel("Total Transactions", fontsize=6)
            ax.tick_params(axis='x', labelsize=5, rotation=45)
            ax.tick_params(axis='y', labelsize=5)
            ax.grid(alpha=0.1)
            ax.legend(fontsize=4)
            st.pyplot(fig, use_container_width=False)
        with col2:
        # Auto-generated insight
            st.write(f"**:red[Insight]**: The highest number of transactions occurred in :orange[{transactions_trend.idxmax()}], with :orange[{transactions_trend.max()}] transactions. The lowest occurred in :orange[{transactions_trend.idxmin()}].")
        
        # Transactions by Day of Week
        st.subheader(":red[3. Transactions by Day of Week]")
        transactions_day_of_week = df.groupby('day_of_week')['price'].count()
        col1, col2 = st.columns([4.5,1])
        with col1:
            fig, ax = plt.subplots(figsize=(4,3))
            transactions_day_of_week.plot(kind='bar', ax=ax, color = 'DarkCyan')
            ax.set_xlabel("Day",fontsize=6)
            ax.set_ylabel("Transactions", fontsize=6)
            ax.tick_params(axis='x',labelsize=5,rotation=30)
            ax.tick_params(axis='y',labelsize=5)
            ax.grid(alpha = 0.1)
            st.pyplot(fig, use_container_width=False)
        with col2:
        # Auto-generated insight
            st.write(f"**:red[Insight]**: Most transactions occurred on :orange[{transactions_day_of_week.idxmax()}] with :orange[{transactions_day_of_week.max()}] transactions, while the least occurred on :orange[{transactions_day_of_week.idxmin()}].")

        # Transactions by Product Category
        st.subheader(":red[4. Transactions by Product Category]")
        sales_by_product = df.groupby('item')['price'].count().sort_values(ascending=True)
        col1, col2 = st.columns([4.5,1])
        with col1:
            fig, ax = plt.subplots(figsize=(4,3))
            sales_by_product.plot(kind='barh', ax=ax, color = 'DeepSkyBlue')
            ax.set_xlabel("Transactions",fontsize=6)
            ax.set_ylabel("item", fontsize=6)
            ax.tick_params(axis='x',labelsize=5)
            ax.tick_params(axis='y',labelsize=5,rotation = 45)
            ax.grid(alpha = 0.1)
            st.pyplot(fig, use_container_width=False)   
        with col2:
        # Auto-generated insight
            st.write(f"**:red[Insight]**: The least popular product is :orange[{sales_by_product.idxmin()}] with only :orange[{sales_by_product.min()}] transactions. The most popular product is :orange[{sales_by_product.idxmax()}] with :orange[{sales_by_product.max()}] transactions.")

        st.subheader(":red[5. Top Performing Products]")
        top_products = df.groupby("item")["price"].sum().sort_values(ascending=False).head(5)
        col1, col2 = st.columns([4.5,1])
        with col1:
            fig, ax = plt.subplots(figsize=(4,3))
            top_products.plot(kind="bar", color=["#2ecc71", "#f39c12", "#e74c3c", "#3498db", "#9b59b6"], ax=ax)
            ax.set_title("Top 5 Products by Revenue",fontsize=6,color='blue')
            ax.set_xlabel("Item",fontsize=6)
            ax.set_ylabel("Revenue", fontsize=6)
            ax.tick_params(axis='x',labelsize=5,rotation = 0)
            ax.tick_params(axis='y',labelsize=5)
            ax.grid(alpha = 0.1)
            st.pyplot(fig, use_container_width=False)    
        with col2:
        # Auto-generated insight
            st.write(f"**:red[Insight]**: The top-performing product is :orange[{top_products.idxmax()}] generating :orange[${top_products.max():,.2f}] in revenue.")

        # Cumulative Contribution Line Chart
        st.subheader(":red[6. Cumulative Revenue Contribution]")
        abc_results = abc_analysis(df)
        col1, col2 = st.columns([4.5,1.5])
        with col1:
            cumulative_fig = px.line(abc_results.sort_values("price", ascending=False).assign(cumulative=lambda x: x["price"].cumsum()), x="item",
            y="cumulative", labels={"cumulative": "Cumulative Revenue ($)", "item": "Products"})
            st.plotly_chart(cumulative_fig, use_container_width=True)
        # Display cumulative contribution insights
        with col2:
            st.write(f":red[**Insight**]: The top **20% of products** contribute approximately **{abc_results.loc[:int(len(abc_results)*0.2), 'price'].sum() / abc_results['price'].sum():.2%}** of total revenue.")
            st.write("Products in the tail end have minimal revenue impact, suggesting opportunities for discontinuation or optimization.")

        
        # Pie Chart - Revenue Contribution by Category
        st.subheader(":red[7. Revenue Contribution by ABC Category]")
        col1, col2 = st.columns([3.5,3])
        with col1:
            fig, ax = plt.subplots(figsize=(3,3))
            abc_results["ABC"].value_counts().plot.pie(autopct="%1.1f%%", colors=["green", "orange", "red"], startangle=90, wedgeprops={'alpha':0.7})
            ax.set_ylabel("")  # Remove y-axis label
            st.pyplot(fig, use_container_width=False)   
        # Display ABC category insights
        with col2:
            category_contributions = abc_results.groupby("ABC")["price"].sum() / abc_results["price"].sum()
            st.write(f"- **Category A** accounts for **{category_contributions['A']:.2%}** of total revenue, representing top-performing products.")
            st.write(f"- **Category B** contributes **{category_contributions['B']:.2%}**, showing medium-performing products.")
            st.write(f"- **Category C** accounts for **{category_contributions['C']:.2%}**, indicating products with low revenue contribution.")
            st.write("=> Consider promoting or phasing out Category C products to improve inventory efficiency.")
            
        st.subheader(":red[8. Customer Retention Metrics]")
        frm_results = frm_analysis(df)
        avg_recency = frm_results["Recency"].mean()
        avg_frequency = frm_results["Frequency"].mean()
        avg_monetary = frm_results["Monetary"].sum()/frm_results["Frequency"].sum()
        # Display overall metrics
        st.write(f"- **Average Recency**: Customers make purchases on average every **{avg_recency:.2f} days**.")
        st.write(f"- **Average Frequency**: Customers make an average of **{avg_frequency:.2f} purchases**.")
        st.write(f"- **Average Monetary Value**: On average, customers spend **${avg_monetary:.2f}** per transaction.")
        
        # Show key metrics by segment
        st.write("##### :blue[Key Metrics by Segment]:")
        frm_results["meanMonetary"] = frm_results["Monetary"]/frm_results["Frequency"]
        segment_metrics = frm_results.groupby("Segment").agg(
            AvgRecency=("Recency", "mean"),
            AvgFrequency=("Frequency", "mean"),
            AvgMonetary=("meanMonetary", "mean"),
            CustomerCount=("Segment", "size"))
        st.dataframe(segment_metrics)
        # Display segment-level insights
        st.write(f"- **High Value Segment**: Customers in this segment spend an average of **${segment_metrics.loc['High Value', 'AvgMonetary']:.2f}** per purchase.")
        st.write(f"- **Loyal Segment**: These customers purchase **{segment_metrics.loc['Loyal', 'AvgFrequency']:.2f} times** on average but might spend less per transaction.")
        st.write(f"- **At Risk Segment**: Customers in this segment haven’t purchased in an average of **{segment_metrics.loc['At Risk', 'AvgRecency']:.2f} days**, suggesting the need for retention strategies.")
        st.write("- Focus retention efforts on :green[At Risk] customers and reward :green[Loyal] customers to increase their monetary value.")

        # 3D FRM Clustering
        st.subheader(":red[9. 3D FRM Clustering with Segments]")
        fig = frm_3d_scatter_with_segments(frm_results)
        st.plotly_chart(fig, use_container_width=True)
        # Display clustering insights
        st.write(":blue[**Customer Clustering Analysis**:]")
        st.write("  - Customers are segmented based on their purchasing behavior, offering actionable insights into engagement and marketing strategies.")
        st.write("  - Segments with overlapping behavior can indicate areas where additional data or features might refine segmentation.")
        st.write("- Use the clustering plot to identify standout segments and focus marketing campaigns for the most valuable groups.")
    else:
        st.warning("Please upload a CSV file.")
# Conclusion Section
if menu == "Conclusion":
    st.header(":dart: :blue[Conclusion]")
    st.markdown("""
        :red[**1. For ABC Analysis:**]
        - Products in Category A are the backbone of revenue. Ensuring their availability and promoting them will sustain growth.
        - Category B products are stable contributors. Monitor them for opportunities to upsell.
        - Category C products need review. Consider reducing stock levels or bundling them to improve profitability.

        :white_check_mark: :blue[Inventory Optimization Recommendations:]
        - Minimize Overstock: Keep inventory of Category C low to free up capital. 
        - Bundle Low-Performing Products
        - Invest in Category A

        
        :red[**2. For RFM Analysis:**]
        - Our high-value customers contribute the most to revenue. Efforts to reward their loyalty should yield better profitability.
        - At-risk customers need re-engagement campaigns, as losing them could significantly impact sales.
        - Low-value customers are less critical but might respond well to special offers or discounts.
        
        :white_check_mark: :blue[Customer Retention Recommendations:]
        - Monitor Recency: Send reminders or special offers to customers inactive for 30 days.
        - Focus on High-Value Segments: Reward them with points or free gifts.
        - Upsell Opportunities: Frequent buyers of low-value items may respond to cross-selling higher-value products.

    """)
