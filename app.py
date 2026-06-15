import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Data Science Salary Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Data Science Salary Analytics Dashboard")

st.markdown("""
Analyze salary trends, job roles, experience levels, company sizes,
and remote work patterns in the Data Science industry.
""")

df = pd.read_csv("data/ds_salaries.csv")
df = df.drop(columns=["Unnamed: 0"])

experience_map = {
    "EN": "Entry Level",
    "MI": "Mid Level",
    "SE": "Senior Level",
    "EX": "Executive Level"
}

df["experience_level"] = df["experience_level"].map(experience_map)

remote_map = {
    0: "On-site",
    50: "Hybrid",
    100: "Remote"
}
company_size_map = {
    "S": "Small",
    "M": "Medium",
    "L": "Large"
}
country_map = {
    "US": "United States",
    "GB": "United Kingdom",
    "DE": "Germany",
    "IN": "India",
    "CA": "Canada",
    "FR": "France",
    "ES": "Spain",
    "JP": "Japan",
    "AU": "Australia",
    "NL": "Netherlands"
}

df["company_location"] = df["company_location"].replace(country_map)
df["company_size"] = df["company_size"].map(company_size_map)
df["remote_ratio"] = df["remote_ratio"].map(remote_map)

st.sidebar.header("Filters")

selected_experience = st.sidebar.selectbox(
    "Experience Level",
    ["All"] + sorted(df["experience_level"].unique().tolist())
)

if selected_experience != "All":
    df = df[df["experience_level"] == selected_experience]

selected_country = st.sidebar.selectbox(
    "Company Location",
    ["All"] + sorted(df["company_location"].dropna().unique().tolist())
)

if selected_country != "All":
    df = df[df["company_location"] == selected_country]

selected_company_size = st.sidebar.selectbox(
    "Company Size",
    ["All"] + sorted(df["company_size"].dropna().unique().tolist())
)

if selected_company_size != "All":
    df = df[df["company_size"] == selected_company_size]

# KPI SECTION STARTS HERE
avg_salary = round(df["salary_in_usd"].mean(), 2)
max_salary = df["salary_in_usd"].max()
total_jobs = len(df)
total_countries = df["company_location"].nunique()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Average Salary", f"${avg_salary:,.0f}")

with col2:
    st.metric("Highest Salary", f"${max_salary:,.0f}")

with col3:
    st.metric("Total Records", total_jobs)
    
with col4:
    st.metric("🌍 Countries", total_countries)    

st.divider()

st.subheader("Dataset Preview")

st.dataframe(df.head())

st.divider()

st.subheader("Top 10 Highest Paying Job Titles")

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

st.divider()

st.subheader("📈 Average Salary by Experience Level")

salary_by_exp = (
    df.groupby("experience_level")["salary_in_usd"]
    .mean()
    .reset_index()
)

fig2 = px.bar(
    salary_by_exp,
    x="experience_level",
    y="salary_in_usd",
    title="Average Salary by Experience Level"
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("🌍 Top 10 Countries by Average Salary")

country_salary = (
    df.groupby("company_location")["salary_in_usd"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    country_salary,
    x="company_location",
    y="salary_in_usd",
    title="Top 10 Countries by Average Salary"
)

st.plotly_chart(fig3, use_container_width=True)

st.divider()

st.subheader("🏠 Remote Work Distribution")

remote_jobs = (
    df["remote_ratio"]
    .value_counts()
    .reset_index()
)

remote_jobs.columns = ["Work Type", "Count"]

fig4 = px.pie(
    remote_jobs,
    names="Work Type",
    values="Count",
    title="Remote vs Hybrid vs On-site Jobs"
)

st.plotly_chart(fig4, use_container_width=True)

st.divider()

st.subheader("🏢 Average Salary by Company Size")

company_salary = (
    df.groupby("company_size")["salary_in_usd"]
    .mean()
    .reset_index()
)

fig5 = px.bar(
    company_salary,
    x="company_size",
    y="salary_in_usd",
    title="Average Salary by Company Size"
)

st.plotly_chart(fig5, use_container_width=True)