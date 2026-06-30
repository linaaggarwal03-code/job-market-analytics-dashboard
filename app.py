import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ml_model import train_salary_model, predict_salary
from utils.styling import inject_custom_css, make_kpi_card, style_plotly_fig, DOLLAR_SVG, TREND_SVG, BRIEFCASE_SVG, GLOBE_SVG
from utils.data_loader import load_data, filter_data, EXPERIENCE_ORDER, COMPANY_SIZE_ORDER

st.set_page_config(
    page_title="Data Science Salary Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Light Glassmorphism & Outfit Font)
inject_custom_css()

# Load Data
df = load_data("data/ds_salaries.csv")

# Sidebar Filters
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.title("🎛️ Dashboard Filters")
st.sidebar.markdown("Use the options below to filter dataset visualizations.")

selected_experience = st.sidebar.selectbox(
    "Experience Level",
    ["All"] + sorted(df["experience_level"].dropna().unique().tolist())
)

selected_country = st.sidebar.selectbox(
    "Company Location",
    ["All"] + sorted(df["company_location"].dropna().unique().tolist())
)

selected_company_size = st.sidebar.selectbox(
    "Company Size",
    ["All"] + sorted(df["company_size"].dropna().unique().tolist())
)

# Apply Filters
# Apply Filters
filtered_df = filter_data(df, selected_experience, selected_country, selected_company_size)

# Main Title & Hero Banner
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(79, 70, 229, 0.06) 0%, rgba(219, 39, 119, 0.06) 100%); padding: 2.2rem 2.5rem; border-radius: 20px; border: 1px solid rgba(79, 70, 229, 0.12); margin-bottom: 2rem; position: relative; overflow: hidden;">
    <div style="position: absolute; top: -50px; right: -50px; width: 180px; height: 180px; background: radial-gradient(circle, rgba(99, 102, 241, 0.18) 0%, transparent 70%); filter: blur(30px);"></div>
    <div style="position: absolute; bottom: -50px; left: -50px; width: 180px; height: 180px; background: radial-gradient(circle, rgba(6, 182, 212, 0.15) 0%, transparent 70%); filter: blur(30px);"></div>
    <h1 style="margin: 0; font-size: 2.6rem; font-weight: 700; background: linear-gradient(to right, #1E1B4B, #4F46E5, #9333EA); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        Data Science Salary Analytics Dashboard
    </h1>
    <p style="margin: 10px 0 0 0; font-size: 1.05rem; color: #475569; max-width: 800px; line-height: 1.5;">
        Explore global data science compensation insights, including compensation by job title, salary growth across experience levels, country-by-country mapping, and remote working trends.
    </p>
</div>
""", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("⚠️ No records match the selected filter combination. Please modify your filters in the sidebar.")
else:
    # Compute KPI Stats
    avg_salary = round(filtered_df["salary_in_usd"].mean(), 2)
    max_salary = filtered_df["salary_in_usd"].max()
    total_jobs = len(filtered_df)
    total_countries = filtered_df["company_location"].nunique()

    # KPI Layout
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(make_kpi_card("Average Salary", f"${avg_salary:,.0f}",  DOLLAR_SVG, "violet"), unsafe_allow_html=True)
    with col2:
        st.markdown(make_kpi_card("Highest Salary", f"${max_salary:,.0f}", TREND_SVG, "cyan"), unsafe_allow_html=True)
    with col3:
        st.markdown(make_kpi_card("Total Records", f"{total_jobs:,}", BRIEFCASE_SVG, "emerald"), unsafe_allow_html=True)
    with col4:
        st.markdown(make_kpi_card("Total Countries", f"{total_countries}", GLOBE_SVG, "amber"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs definition
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Overview & Data",
    "💼 Roles & Experience",
    "📈 Trends Over Time",
    "🌍 Global Geography",
    "🏢 Company & Environment",
    "🤖 Salary Predictor"
])

    # TAB 1: Overview
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Data Overview")
        st.markdown("Search and export the records matching the active filters.")

        search_term = st.text_input("🔍 Search by job title", placeholder="e.g. Data Engineer, ML Scientist...")

        table_df = filtered_df
        if search_term:
            table_df = table_df[table_df["job_title"].str.contains(search_term, case=False, na=False)]
            st.caption(f"Found {len(table_df):,} matching record(s).")

        st.dataframe(table_df.head(100), use_container_width=True)

        st.download_button(
            label="⬇️ Download filtered data as CSV",
            data=table_df.to_csv(index=False).encode("utf-8"),
            file_name="filtered_salaries.csv",
            mime="text/csv",
        )
    # TAB 2: Roles & Experience
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        col_left, col_right = st.columns(2)

        with col_left:
            top_jobs = (
                filtered_df.groupby("job_title")["salary_in_usd"]
                .mean()
                .reset_index()
                .sort_values("salary_in_usd", ascending=True)
                .tail(10)
            )
            fig1 = px.bar(
                top_jobs,
                x="salary_in_usd",
                y="job_title",
                orientation='h',
                color="salary_in_usd",
                color_continuous_scale=["#A5B4FC", "#6366F1", "#312E81"],
                labels={"salary_in_usd": "Avg Salary (USD)", "job_title": "Job Title"}
            )
            fig1 = style_plotly_fig(fig1, "Top 10 Highest Paying Job Titles")
            fig1.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig1, use_container_width=True)

        with col_right:
            salary_by_exp = (
                filtered_df.groupby("experience_level")["salary_in_usd"]
                .mean()
                .reset_index()
            )
            # Reorder experience levels
            exp_order = ["Entry Level", "Mid Level", "Senior Level", "Executive Level"]
            salary_by_exp["experience_level"] = pd.Categorical(
                salary_by_exp["experience_level"], 
                categories=exp_order, 
                ordered=True
            )
            salary_by_exp = salary_by_exp.dropna().sort_values("experience_level")
            
            fig2 = px.bar(
                salary_by_exp,
                x="experience_level",
                y="salary_in_usd",
                color="experience_level",
                color_discrete_sequence=["#818CF8", "#6366F1", "#4F46E5", "#312E81"],
                labels={"salary_in_usd": "Avg Salary (USD)", "experience_level": "Experience Level"}
            )
            fig2 = style_plotly_fig(fig2, "Average Salary by Experience Level")
            fig2.update_layout(showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
    # TAB 3: Trends Over Time
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("See how average compensation has shifted year over year, and how that growth differs by seniority.")

        col_left, col_right = st.columns(2)

        with col_left:
            yearly = filtered_df.groupby("work_year")["salary_in_usd"].mean().reset_index()
            fig_year = px.line(
                yearly,
                x="work_year",
                y="salary_in_usd",
                markers=True,
                labels={"salary_in_usd": "Avg Salary (USD)", "work_year": "Year"},
                color_discrete_sequence=["#4F46E5"]
            )
            fig_year = style_plotly_fig(fig_year, "Average Salary by Year")
            fig_year.update_xaxes(dtick=1)
            st.plotly_chart(fig_year, use_container_width=True)

        with col_right:
            exp_order = ["Entry Level", "Mid Level", "Senior Level", "Executive Level"]
            yearly_by_exp = (
                filtered_df.groupby(["work_year", "experience_level"])["salary_in_usd"]
                .mean()
                .reset_index()
            )
            fig_year_exp = px.line(
                yearly_by_exp,
                x="work_year",
                y="salary_in_usd",
                color="experience_level",
                markers=True,
                category_orders={"experience_level": exp_order},
                color_discrete_sequence=["#818CF8", "#6366F1", "#4F46E5", "#312E81"],
                labels={"salary_in_usd": "Avg Salary (USD)", "work_year": "Year", "experience_level": "Experience"}
            )
            fig_year_exp = style_plotly_fig(fig_year_exp, "Salary Growth by Experience Level")
            fig_year_exp.update_xaxes(dtick=1)
            st.plotly_chart(fig_year_exp, use_container_width=True)
    # TAB 4: Global Geography
    with tab4:
        st.markdown("<br>", unsafe_allow_html=True)
        col_map_left, col_map_right = st.columns(2)

        with col_map_left:
            country_salary = (
                filtered_df.groupby("company_location")["salary_in_usd"]
                .mean()
                .reset_index()
                .sort_values("salary_in_usd", ascending=True)
                .tail(10)
            )
            fig3 = px.bar(
                country_salary,
                x="salary_in_usd",
                y="company_location",
                orientation='h',
                color="salary_in_usd",
                color_continuous_scale=["#67E8F9", "#06B6D4", "#0891B2", "#0F766E"],
                labels={"salary_in_usd": "Avg Salary (USD)", "company_location": "Country"}
            )
            fig3 = style_plotly_fig(fig3, "Top 10 Countries by Average Salary")
            fig3.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig3, use_container_width=True)

        with col_map_right:
            map_data = (
                filtered_df.groupby(["company_location_iso3", "company_location"])["salary_in_usd"]
                .mean()
                .reset_index()
            )
            fig_map = px.choropleth(
                map_data,
                locations="company_location_iso3",
                color="salary_in_usd",
                hover_name="company_location",
                color_continuous_scale=["#E0E7FF", "#6366F1", "#312E81"],
                labels={"salary_in_usd": "Avg Salary (USD)"}
            )
            fig_map = style_plotly_fig(fig_map, "Global Salary Distribution Mapping")
            fig_map.update_layout(
                geo=dict(
                    showframe=False,
                    showcoastlines=True,
                    projection_type='equirectangular',
                    bgcolor='rgba(0,0,0,0)',
                    landcolor='#E2E8F0',
                    subunitcolor='#CBD5E1',
                    coastlinecolor='#94A3B8',
                    showcountries=True,
                    countrycolor='#CBD5E1'
                ),
                margin=dict(l=0, r=0, t=60, b=0)
            )
            st.plotly_chart(fig_map, use_container_width=True)

    # TAB 5: Company & Environment
    with tab5:
        st.markdown("<br>", unsafe_allow_html=True)
        col_comp_left, col_comp_right = st.columns(2)

        with col_comp_left:
            remote_jobs = (
                filtered_df["remote_ratio"]
                .value_counts()
                .reset_index()
            )
            remote_jobs.columns = ["Work Type", "Count"]
            color_map = {"Remote": "#0D9488", "Hybrid": "#3B82F6", "On-site": "#F59E0B"}
            
            fig4 = px.pie(
                remote_jobs,
                names="Work Type",
                values="Count",
                hole=0.45,
                color="Work Type",
                color_discrete_map=color_map,
            )
            fig4 = style_plotly_fig(fig4, "Remote Work Distribution")
            fig4.update_layout(
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.15,
                    xanchor="center",
                    x=0.5,
                    font=dict(color="#475569")
                )
            )
            st.plotly_chart(fig4, use_container_width=True)

        with col_comp_right:
            company_salary = (
                filtered_df.groupby("company_size")["salary_in_usd"]
                .mean()
                .reset_index()
            )
            # Reorder sizes
            size_order = ["Small", "Medium", "Large"]
            company_salary["company_size"] = pd.Categorical(
                company_salary["company_size"],
                categories=size_order,
                ordered=True
            )
            company_salary = company_salary.dropna().sort_values("company_size")

            fig5 = px.bar(
                company_salary,
                x="company_size",
                y="salary_in_usd",
                color="company_size",
                color_discrete_sequence=["#C084FC", "#A855F7", "#7E22CE"],
                labels={"salary_in_usd": "Avg Salary (USD)", "company_size": "Company Size"}
            )
            fig5 = style_plotly_fig(fig5, "Average Salary by Company Size")
            fig5.update_layout(showlegend=False)
            st.plotly_chart(fig5, use_container_width=True)
    # TAB 6: Salary Predictor (ML)
    with tab6:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🤖 ML-Powered Salary Predictor")
        st.markdown(
            "Pick a role profile below and a **Random Forest** model -- trained on the full, "
            "unfiltered dataset -- will estimate the expected salary in USD."
        )

        with st.spinner("Training model..."):
            model_result = train_salary_model(df)

        with st.expander("ℹ️ About this model"):
            st.markdown(f"""
- **Algorithm:** Random Forest Regressor (scikit-learn), 200 trees
- **Features:** work year, experience level, employment type, job title, remote ratio, company location, company size
- **Train/test split:** 80/20, evaluated on held-out test data
- **Test R² score:** `{model_result.r2:.3f}`
- **Test Mean Absolute Error:** `${model_result.mae:,.0f}`
            """)

        pred_col1, pred_col2, pred_col3 = st.columns(3)
        with pred_col1:
            in_job_title = st.selectbox("Job Title", model_result.job_titles)
            in_experience = st.selectbox("Experience Level", ["Entry Level", "Mid Level", "Senior Level", "Executive Level"])
        with pred_col2:
            in_company_size = st.selectbox("Company Size", ["Small", "Medium", "Large"])
            in_remote = st.selectbox("Remote Ratio", ["On-site", "Hybrid", "Remote"])
        with pred_col3:
            in_country = st.selectbox("Company Location", model_result.countries)
            in_employment = st.selectbox("Employment Type", sorted(df["employment_type"].dropna().unique().tolist()))

        in_year = st.slider("Work Year", min_value=int(df["work_year"].min()), max_value=int(df["work_year"].max()) + 1, value=int(df["work_year"].max()))

        if st.button("🔮 Predict Salary", type="primary", use_container_width=True):
            prediction, uncertainty = predict_salary(
                model_result,
                work_year=in_year,
                experience_level=in_experience,
                employment_type=in_employment,
                job_title=in_job_title,
                remote_ratio=in_remote,
                company_location=in_country,
                company_size=in_company_size,
            )

            st.markdown(f"""
<div class="predict-result">
    <div style="font-size: 13px; color: #64748b; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600;">
        Estimated Salary (USD / year)
    </div>
    <div class="big-number">${prediction:,.0f}</div>
    <div style="color: #475569; margin-top: 8px;">
        Typical range: ${max(prediction - uncertainty, 0):,.0f} – ${prediction + uncertainty:,.0f}
    </div>
</div>
""", unsafe_allow_html=True)        