import streamlit as st
import pandas as pd
import plotly.express as px

def calculate_approval_rate(df):
    """Calculate the approval rate based on loan_status (1 = Approved, 0 = Rejected)."""
    approved = len(df[df['loan_status'] == 1])
    total = len(df)
    rate = approved / total * 100
    return f"{rate:.2f}%"

def app(df):
    st.title("📊 Loan Approval Analytics Dashboard")

    # Display Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    total_records = len(df)
    approved_count = len(df[df['loan_status'] == 1])
    rejected_count = len(df[df['loan_status'] == 0])
    approval_rate = calculate_approval_rate(df)

    col1.metric("📁 Total Records", total_records)
    col2.metric("✅ Approved Loans", approved_count)
    col3.metric("❌ Rejected Loans", rejected_count)
    col4.metric("📈 Approval Rate", approval_rate)

    # Show Data Sample
    if st.button("📄 Show Sample Data"):
        st.dataframe(df.sample(5))

    st.header("📌 Analysis Selection")

    # Numeric Analysis
    if st.checkbox("📉 Show Univariate Analysis (Numeric)"):
        st.subheader("Numeric Variable Distributions")
        num_cols = df.select_dtypes(include=['int64', 'float64']).columns
        for col in num_cols:
            fig = px.histogram(df, x=col, title=f"Distribution of {col}")
            st.plotly_chart(fig, use_container_width=True)

    # Categorical Analysis (FIXED)
    if st.checkbox("🧩 Show Categorical Analysis"):
        st.subheader("Categorical Variable Distributions")
        cat_cols = df.select_dtypes(include=['object']).columns
        for col in cat_cols:
            value_counts = df[col].value_counts().reset_index()
            value_counts.columns = [col, 'count']  # Rename for clarity
            fig = px.bar(value_counts, 
                         x=col, y='count', 
                         title=f"Distribution of {col}",
                         labels={col: col, 'count': 'Count'})
            st.plotly_chart(fig, use_container_width=True)

    # Correlation Heatmap
    if st.checkbox("🔗 Show Correlation Heatmap (Numeric)"):
        st.subheader("Correlation Heatmap")
        num_data = df.select_dtypes(include=['int64', 'float64'])
        corr = num_data.corr()
        fig = px.imshow(corr, 
                        text_auto=True, 
                        title="Correlation Heatmap", 
                        aspect="auto", 
                        color_continuous_scale="Blues")
        st.plotly_chart(fig, use_container_width=True)
