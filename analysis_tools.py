import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px

# ABC Analysis
def abc_analysis(df):
    sales_per_product = df.groupby("item")["price"].sum().sort_values(ascending=False)
    total_sales = sales_per_product.sum()
    sales_cumulative = (sales_per_product / total_sales).cumsum()
    abc_categories = pd.cut(sales_cumulative, bins=[0, 0.8, 0.95, 1], labels=["A", "B", "C"])
    sales_per_product = sales_per_product.reset_index()
    sales_per_product["ABC"] = abc_categories.values
    return sales_per_product

# FRM Analysis
def frm_analysis(df):
    df["date"] = pd.to_datetime(df["date"])
    current_date = df["date"].max() + pd.Timedelta(days=1)
    frm = df.groupby("customer").agg(
        Frequency=("key", "count"),
        Recency=("date", lambda x: (current_date - x.max()).days),
        Monetary=("price", "sum"),)
    # Add thresholds for segmentation
    recency_threshold = frm["Recency"].astype(int).median()
    frequency_threshold = frm["Frequency"].median()
    monetary_threshold = frm["Monetary"].median()
    # Create segments
    frm['Segment'] = (frm.apply(lambda row: 'High Value' if row['Frequency'] > frequency_threshold and row['Monetary'] > monetary_threshold
                          else ('Loyal' if row['Frequency'] > frequency_threshold 
                                else ('At Risk' if row['Recency'] > recency_threshold else 'Low Value')), axis=1))
    return frm

# Visualize ABC Analysis
def visualize_abc(abc_results, output_path):
    plt.figure(figsize=(5, 4))
    abc_results.groupby("ABC")["price"].sum().plot(kind="bar", color=["green", "orange", "red"])
    plt.title("ABC Analysis", color="blue")
    plt.xlabel("Category")
    plt.xticks(rotation=0)
    plt.ylabel("Total Sales")
    plt.yticks(size=6)
    plt.grid(alpha=0.1)
    plt.savefig(output_path)
    plt.close()

# Visualize FRM Analysis
def visualize_frm(frm_results, output_path):
    plt.figure(figsize=(5, 4))
    frm_results["Segment"].value_counts().plot(kind="bar", color=['#3498db', '#2ecc71', '#f1c40f', '#e74c3c'])
    plt.title("Customer Segmentation (FRM)", color="blue")
    plt.xlabel("Segment")
    plt.xticks(rotation=0)
    plt.ylabel("Number of Customers")
    plt.grid(alpha=0.1)
    plt.savefig(output_path)
    plt.close()
    
# Interactive 3D FRM Plot ="frm_3d_plot_with_segments.html"
# Function for 3D FRM Plot with Segments
def frm_3d_scatter_with_segments(frm_results):
    if "Segment" not in frm_results.columns:
        st.error("The FRM data must contain a 'Segment' column for visualization.")
        return None
    # Create the 3D scatter plot
    fig = px.scatter_3d(frm_results.reset_index(),x="Recency", y="Frequency", z="Monetary", color="Segment", symbol="Segment", hover_name="customer",
         color_discrete_map={"High Value": "#2ecc71", "Loyal": "#3498db", "At Risk": "#e74c3c", "Low Value": "#f1c40f"})
    fig.update_traces(marker=dict(size=3, opacity=0.5))
    fig.update_layout(scene=dict(xaxis_title="Recency (Days)", yaxis_title="Frequency", zaxis_title="Monetary ($)"))
    return fig
