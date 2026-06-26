import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Data Science Salary Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Light Glassmorphism & Outfit Font)
st.markdown("""
<style>
/* Custom font */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

/* Global styles */
html, body, [data-testid="stAppViewContainer"], .main {
    font-family: 'Outfit', sans-serif;
    background-color: #f8fafc;
    color: #1e293b;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid rgba(0, 0, 0, 0.06);
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
    color: #0f172a;
    font-weight: 600;
}

/* Hide default headers/footers */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {background-color: transparent !important;}

/* Custom KPI Cards */
.kpi-card {
    background: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(0, 0, 0, 0.04);
    border-radius: 16px;
    padding: 22px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.02);
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.kpi-card:hover {
    transform: translateY(-4px);
    border-color: rgba(99, 102, 241, 0.35);
    box-shadow: 0 12px 24px -8px rgba(99, 102, 241, 0.15);
    background: rgba(255, 255, 255, 0.95);
}

.kpi-icon-container {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.kpi-content {
    display: flex;
    flex-direction: column;
}

.kpi-label {
    font-size: 12px;
    color: #64748b;
    margin: 0;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.kpi-value {
    font-size: 24px;
    color: #0f172a;
    margin: 4px 0 0 0;
    font-weight: 700;
}

/* Tabs customization */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: transparent;
    padding: 0 10px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.stTabs [data-baseweb="tab"] {
    background-color: rgba(241, 245, 249, 0.6);
    border: 1px solid rgba(0, 0, 0, 0.03);
    border-radius: 8px 8px 0 0;
    color: #64748b;
    padding: 12px 24px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #0f172a;
    background-color: rgba(241, 245, 249, 0.95);
    border-color: rgba(0, 0, 0, 0.08);
}

.stTabs [aria-selected="true"] {
    background-color: rgba(99, 102, 241, 0.07) !important;
    border-color: rgba(99, 102, 241, 0.2) !important;
    color: #4f46e5 !important;
    border-bottom: 2px solid #4f46e5 !important;
    font-weight: 600;
}

/* Styling DataFrame wrapper */
.element-container:has(div.stDataFrame) {
    background: rgba(255, 255, 255, 0.6);
    border: 1px solid rgba(0, 0, 0, 0.05);
    border-radius: 12px;
    padding: 8px;
}

/* Alert/warning styling overrides */
div[data-testid="stAlert"] {
    background-color: rgba(254, 243, 199, 0.6);
    border: 1px solid rgba(245, 158, 11, 0.25);
    border-radius: 12px;
    color: #92400e;
}

</style>
""", unsafe_allow_html=True)

# SVG Icons for KPI Cards
dollar_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>"""
trend_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>"""
briefcase_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>"""
globe_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>"""

def make_kpi_card(title, value, svg_icon, color_theme):
    themes = {
        "violet": {"bg": "rgba(79, 70, 229, 0.09)", "text": "#4F46E5"},
        "cyan": {"bg": "rgba(8, 145, 178, 0.09)", "text": "#0891B2"},
        "emerald": {"bg": "rgba(5, 150, 105, 0.09)", "text": "#059669"},
        "amber": {"bg": "rgba(217, 119, 6, 0.09)", "text": "#D97706"}
    }
    t = themes.get(color_theme, themes["violet"])
    return f"""
    <div class="kpi-card" style="border-left: 4px solid {t['text']};">
        <div class="kpi-icon-container" style="background: {t['bg']}; color: {t['text']};">
            {svg_icon}
        </div>
        <div class="kpi-content">
            <span class="kpi-label">{title}</span>
            <span class="kpi-value">{value}</span>
        </div>
    </div>
    """

def style_plotly_fig(fig, title_text):
    fig.update_layout(
        title={
            'text': f"<b>{title_text}</b>",
            'y': 0.94,
            'x': 0.05,
            'xanchor': 'left',
            'yanchor': 'top',
            'font': {'size': 18, 'family': 'Outfit, sans-serif', 'color': '#1E293B'}
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family="Outfit, sans-serif",
        font_color="#475569",
        margin=dict(l=50, r=30, t=80, b=50),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_size=13,
            font_family="Outfit, sans-serif",
            font_color="#1E293B"
        )
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor='rgba(0, 0, 0, 0.08)',
        tickfont=dict(color='#475569', size=11),
        title_font=dict(color='#1E293B', size=12)
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor='rgba(0, 0, 0, 0.05)',
        linecolor='rgba(0, 0, 0, 0.08)',
        tickfont=dict(color='#475569', size=11),
        title_font=dict(color='#1E293B', size=12)
    )
    return fig

# Load Data
df = pd.read_csv("data/ds_salaries.csv")
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# Mappings
experience_map = {
    "EN": "Entry Level",
    "MI": "Mid Level",
    "SE": "Senior Level",
    "EX": "Executive Level"
}

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
    "AE": "United Arab Emirates", "AS": "American Samoa", "AT": "Austria", "AU": "Australia",
    "BE": "Belgium", "BR": "Brazil", "CA": "Canada", "CH": "Switzerland", "CL": "Chile",
    "CN": "China", "CO": "Colombia", "CZ": "Czechia", "DE": "Germany", "DK": "Denmark",
    "DZ": "Algeria", "EE": "Estonia", "ES": "Spain", "FR": "France", "GB": "United Kingdom",
    "GR": "Greece", "HN": "Honduras", "HR": "Croatia", "HU": "Hungary", "IE": "Ireland",
    "IL": "Israel", "IN": "India", "IQ": "Iraq", "IR": "Iran", "IT": "Italy", "JP": "Japan",
    "KE": "Kenya", "LU": "Luxembourg", "MD": "Moldova", "MT": "Malta", "MX": "Mexico",
    "MY": "Malaysia", "NG": "Nigeria", "NL": "Netherlands", "NZ": "New Zealand",
    "PK": "Pakistan", "PL": "Poland", "PT": "Portugal", "RO": "Romania", "RU": "Russia",
    "SG": "Singapore", "SI": "Slovenia", "TR": "Turkey", "UA": "Ukraine", "US": "United States",
    "VN": "Vietnam"
}

iso2_to_iso3 = {
    "AE": "ARE", "AS": "ASM", "AT": "AUT", "AU": "AUS", "BE": "BEL", "BR": "BRA",
    "CA": "CAN", "CH": "CHE", "CL": "CHL", "CN": "CHN", "CO": "COL", "CZ": "CZE",
    "DE": "DEU", "DK": "DNK", "DZ": "DZA", "EE": "EST", "ES": "ESP", "FR": "FRA",
    "GB": "GBR", "GR": "GRC", "HN": "HND", "HR": "HRV", "HU": "HUN", "IE": "IRL",
    "IL": "ISR", "IN": "IND", "IQ": "IRQ", "IR": "IRN", "IT": "ITA", "JP": "JPN",
    "KE": "KEN", "LU": "LUX", "MD": "MDA", "MT": "MLT", "MX": "MEX", "MY": "MYS",
    "NG": "NGA", "NL": "NLD", "NZ": "NZL", "PK": "PAK", "PL": "POL", "PT": "PRT",
    "RO": "ROU", "RU": "RUS", "SG": "SGP", "SI": "SVN", "TR": "TUR", "UA": "UKR",
    "US": "USA", "VN": "VNM"
}

df["company_location_iso3"] = df["company_location"].map(iso2_to_iso3).fillna(df["company_location"])
df["company_location"] = df["company_location"].replace(country_map)
df["company_size"] = df["company_size"].map(company_size_map)
df["experience_level"] = df["experience_level"].map(experience_map)
df["remote_ratio"] = df["remote_ratio"].map(remote_map)

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
filtered_df = df.copy()
if selected_experience != "All":
    filtered_df = filtered_df[filtered_df["experience_level"] == selected_experience]

if selected_country != "All":
    filtered_df = filtered_df[filtered_df["company_location"] == selected_country]

if selected_company_size != "All":
    filtered_df = filtered_df[filtered_df["company_size"] == selected_company_size]

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
        st.markdown(make_kpi_card("Average Salary", f"${avg_salary:,.0f}", dollar_svg, "violet"), unsafe_allow_html=True)
    with col2:
        st.markdown(make_kpi_card("Highest Salary", f"${max_salary:,.0f}", trend_svg, "cyan"), unsafe_allow_html=True)
    with col3:
        st.markdown(make_kpi_card("Total Records", f"{total_jobs:,}", briefcase_svg, "emerald"), unsafe_allow_html=True)
    with col4:
        st.markdown(make_kpi_card("Total Countries", f"{total_countries}", globe_svg, "amber"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs definition
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Overview & Data",
        "💼 Roles & Experience",
        "🌍 Global Geography",
        "🏢 Company & Environment"
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

    # TAB 3: Global Geography
    with tab3:
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

    # TAB 4: Company & Environment
    with tab4:
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
            fig5.update_layout(showlegend=False)ss
            st.plotly_chart(fig5, use_container_width=True)