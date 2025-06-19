import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="📊 Marketing Strategy - Prescriptive Analytics", layout="wide")

# Persistent signature in bottom-right corner (always visible)
st.markdown("""
    <style>
    #credit {
        position: fixed;
        bottom: 15px;
        right: 25px;
        background-color: rgba(240, 242, 246, 0.9);
        padding: 10px 20px;
        border-radius: 10px;
        font-size: 14px;
        font-weight: 600;
        color: #444;
        box-shadow: 0 0 8px rgba(0,0,0,0.1);
        z-index: 9999;
    }
    </style>
    <div id='credit'>Made by Vinayak Shukla</div>
""", unsafe_allow_html=True)

st.title("🚀 Prescriptive Marketing Strategy Dashboard")

st.markdown("""
This dashboard provides **prescriptive insights** into marketing campaign performance. 
Our objective is to help the marketing team **identify what's working**, **reduce wasteful spend**, and **optimize conversion strategies**.

📌 _Company Problem Statement:_
> The marketing team is unsure which campaigns drive the most engagement and reach. There is a need to identify high-performing segments, visualize trends, and derive data-backed decisions to improve ROI.
""")

# Local path fallback and cloud-safe default
local_path = r"F:\\New folder\\Campaign-Data.csv"
default_path = "Campaign-Data.csv"

try:
    if os.path.exists(local_path):
        df = pd.read_csv(local_path)
        st.success("✅ Data loaded from local system.")
    else:
        df = pd.read_csv(default_path)
        st.success("✅ Data loaded from app directory.")

    # Tabs for organized layout
    tab1, tab2, tab3, tab4 = st.tabs(["📁 Data Overview", "📊 KPI Insights", "📉 Heatmap Analysis", "💡 Strategic Insights"])

    with tab1:
        st.subheader("Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)

        st.subheader("Basic Info")
        st.markdown(f"**Rows:** {df.shape[0]}  |  **Columns:** {df.shape[1]}")
        st.markdown(f"**Columns:** {', '.join(df.columns)}")
        st.write(df.describe())

    with tab2:
        st.subheader("📌 Key Performance Indicators")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Campaign Records", df.shape[0])
        with col2:
            top_col = df.select_dtypes(include=['int64', 'float64']).columns[0] if not df.select_dtypes(include=['int64', 'float64']).empty else None
            if top_col:
                st.metric(f"Total {top_col}", f"{df[top_col].sum():,.0f}")
        with col3:
            if top_col:
                avg = df[top_col].mean()
                st.metric(f"Avg. {top_col}", f"{avg:,.2f}")

        st.subheader("📊 Distribution & Trend Visualization")
        chart_col = st.selectbox("Select a column to visualize", df.columns)

        if df[chart_col].dtype in ['int64', 'float64']:
            fig, ax = plt.subplots()
            sns.histplot(df[chart_col], kde=True, ax=ax, color="skyblue")
            ax.set_title(f"Distribution of {chart_col}")
            st.pyplot(fig)
        else:
            st.bar_chart(df[chart_col].value_counts())

    with tab3:
        st.subheader("🔍 Correlation Heatmap")
        numeric_df = df.select_dtypes(include=['int64', 'float64'])

        if not numeric_df.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)
        else:
            st.warning("No numeric columns found for correlation analysis.")

    with tab4:
        st.subheader("💡 Strategic Insights")

        st.markdown("**📌 Suggested Actions Based on Initial Data Review:**")
        st.markdown("""
        - Identify which metric (e.g., Impressions, Clicks, Views) is most critical for your campaign and optimize based on that.
        - Look into time-based performance (e.g., monthly or weekly trends) to determine campaign timing effectiveness.
        - Reallocate marketing resources toward consistently high-performing categories or platforms.
        - Use correlation analysis to understand the impact of spend, impressions, or engagement rates on outcomes.
        - Consider A/B testing strategies for campaigns with ambiguous performance.
        """)

except Exception as e:
    st.error("❌ Data file could not be loaded. Please ensure it exists at the specified path or in the app directory.")







