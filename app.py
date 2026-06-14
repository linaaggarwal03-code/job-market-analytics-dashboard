import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Data Science Salary Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Data Science Salary Analytics Dashboard")

df = pd.read_csv("data/ds_salaries.csv")
df = df.drop(columns=["Unnamed: 0"])

# KPI SECTION
avg_salary = round(df["salary_in_usd"].mean(), 2)
max_salary = df["salary_in_usd"].max()
total_jobs = len(df)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Average Salary", f"${avg_salary:,.0f}")

with col2:
    st.metric("🚀 Highest Salary", f"${max_salary:,.0f}")

with col3:
    st.metric("📄 Total Records", total_jobs)

st.divider()

st.subheader("Dataset Preview")

st.dataframe(df.head())

st.divider()

st.subheader("💼 Top 10 Highest Paying Job Titles")

top_jobs = (
    df.groupby("job_title")["salary_in_usd"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_jobs,
    x="job_title",
    y="salary_in_usd",
    title="Top 10 Highest Paying Job Titles",
)

st.plotly_chart(fig, use_container_width=True)