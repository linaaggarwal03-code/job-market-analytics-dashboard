"""
styling.py
----------------
All visual/presentation helpers: the injected custom CSS, the SVG icon
strings used in KPI cards, the KPI card builder, and a Plotly figure
styling helper so every chart in the app shares one consistent look.

Pulling this out of app.py keeps the layout code readable -- you can see
the *structure* of the dashboard in app.py without scrolling past 150
lines of CSS first.
"""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

CUSTOM_CSS = """
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

/* Predictor result card */
.predict-result {
    background: linear-gradient(135deg, rgba(79, 70, 229, 0.08) 0%, rgba(219, 39, 119, 0.06) 100%);
    border: 1px solid rgba(79, 70, 229, 0.18);
    border-radius: 16px;
    padding: 28px;
    text-align: center;
}

.predict-result .big-number {
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(to right, #1E1B4B, #4F46E5, #9333EA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
"""

# SVG Icons used in KPI Cards
DOLLAR_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>"""
TREND_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>"""
BRIEFCASE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>"""
GLOBE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>"""

_KPI_THEMES = {
    "violet": {"bg": "rgba(79, 70, 229, 0.09)", "text": "#4F46E5"},
    "cyan": {"bg": "rgba(8, 145, 178, 0.09)", "text": "#0891B2"},
    "emerald": {"bg": "rgba(5, 150, 105, 0.09)", "text": "#059669"},
    "amber": {"bg": "rgba(217, 119, 6, 0.09)", "text": "#D97706"},
}


def inject_custom_css() -> None:
    """Inject the dashboard's global stylesheet. Call once near the top of app.py."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def make_kpi_card(title: str, value: str, svg_icon: str, color_theme: str) -> str:
    """Build the HTML for a single KPI summary card."""
    theme = _KPI_THEMES.get(color_theme, _KPI_THEMES["violet"])
    return f"""
    <div class="kpi-card" style="border-left: 4px solid {theme['text']};">
        <div class="kpi-icon-container" style="background: {theme['bg']}; color: {theme['text']};">
            {svg_icon}
        </div>
        <div class="kpi-content">
            <span class="kpi-label">{title}</span>
            <span class="kpi-value">{value}</span>
        </div>
    </div>
    """


def style_plotly_fig(fig: go.Figure, title_text: str) -> go.Figure:
    """Apply the dashboard's shared Plotly theme (fonts, colors, grid) to a figure."""
    fig.update_layout(
        title={
            "text": f"<b>{title_text}</b>",
            "y": 0.94,
            "x": 0.05,
            "xanchor": "left",
            "yanchor": "top",
            "font": {"size": 18, "family": "Outfit, sans-serif", "color": "#1E293B"},
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_family="Outfit, sans-serif",
        font_color="#475569",
        margin=dict(l=50, r=30, t=80, b=50),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_size=13,
            font_family="Outfit, sans-serif",
            font_color="#1E293B",
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor="rgba(0, 0, 0, 0.08)",
        tickfont=dict(color="#475569", size=11),
        title_font=dict(color="#1E293B", size=12),
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(0, 0, 0, 0.05)",
        linecolor="rgba(0, 0, 0, 0.08)",
        tickfont=dict(color="#475569", size=11),
        title_font=dict(color="#1E293B", size=12),
    )
    return fig
