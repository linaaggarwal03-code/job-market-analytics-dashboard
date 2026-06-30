"""
data_loader.py
----------------
Handles everything related to getting the salary dataset ready for the
dashboard: loading the raw CSV, translating coded values (e.g. "EN" ->
"Entry Level") into human-readable labels, and applying sidebar filters.

Keeping this logic separate from app.py means the UI code in app.py stays
focused purely on layout/visuals, and this module can be unit-tested or
reused independently (e.g. by ml_model.py).
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Static lookup tables
# ---------------------------------------------------------------------------

EXPERIENCE_MAP: dict[str, str] = {
    "EN": "Entry Level",
    "MI": "Mid Level",
    "SE": "Senior Level",
    "EX": "Executive Level",
}

EXPERIENCE_ORDER: list[str] = [
    "Entry Level",
    "Mid Level",
    "Senior Level",
    "Executive Level",
]

REMOTE_MAP: dict[int, str] = {
    0: "On-site",
    50: "Hybrid",
    100: "Remote",
}

COMPANY_SIZE_MAP: dict[str, str] = {
    "S": "Small",
    "M": "Medium",
    "L": "Large",
}

COMPANY_SIZE_ORDER: list[str] = ["Small", "Medium", "Large"]

COUNTRY_MAP: dict[str, str] = {
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
    "VN": "Vietnam",
}

ISO2_TO_ISO3: dict[str, str] = {
    "AE": "ARE", "AS": "ASM", "AT": "AUT", "AU": "AUS", "BE": "BEL", "BR": "BRA",
    "CA": "CAN", "CH": "CHE", "CL": "CHL", "CN": "CHN", "CO": "COL", "CZ": "CZE",
    "DE": "DEU", "DK": "DNK", "DZ": "DZA", "EE": "EST", "ES": "ESP", "FR": "FRA",
    "GB": "GBR", "GR": "GRC", "HN": "HND", "HR": "HRV", "HU": "HUN", "IE": "IRL",
    "IL": "ISR", "IN": "IND", "IQ": "IRQ", "IR": "IRN", "IT": "ITA", "JP": "JPN",
    "KE": "KEN", "LU": "LUX", "MD": "MDA", "MT": "MLT", "MX": "MEX", "MY": "MYS",
    "NG": "NGA", "NL": "NLD", "NZ": "NZL", "PK": "PAK", "PL": "POL", "PT": "PRT",
    "RO": "ROU", "RU": "RUS", "SG": "SGP", "SI": "SVN", "TR": "TUR", "UA": "UKR",
    "US": "USA", "VN": "VNM",
}


@st.cache_data(show_spinner=False)
def load_data(csv_path: str = "data/ds_salaries.csv") -> pd.DataFrame:
    """
    Load the raw salary CSV and apply all label mappings.

    Cached with st.cache_data so the (relatively expensive) read + mapping
    step only runs once per session instead of on every rerun triggered by
    a filter change -- this is the single biggest performance win available
    in a Streamlit app like this.

    Raises
    ------
    FileNotFoundError
        Re-raised with a clearer message if the CSV can't be found, since
        this is the most common setup mistake for first-time users.
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"Could not find '{csv_path}'. Make sure you're running "
            "`streamlit run app.py` from the project's root folder."
        ) from exc

    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    df["company_location_iso3"] = (
        df["company_location"].map(ISO2_TO_ISO3).fillna(df["company_location"])
    )
    df["company_location"] = df["company_location"].replace(COUNTRY_MAP)
    df["company_size"] = df["company_size"].map(COMPANY_SIZE_MAP)
    df["experience_level"] = df["experience_level"].map(EXPERIENCE_MAP)
    df["remote_ratio"] = df["remote_ratio"].map(REMOTE_MAP)

    return df


def filter_data(
    df: pd.DataFrame,
    experience: str = "All",
    country: str = "All",
    company_size: str = "All",
) -> pd.DataFrame:
    """Apply the sidebar dropdown filters and return the resulting subset."""
    filtered = df

    if experience != "All":
        filtered = filtered[filtered["experience_level"] == experience]
    if country != "All":
        filtered = filtered[filtered["company_location"] == country]
    if company_size != "All":
        filtered = filtered[filtered["company_size"] == company_size]

    return filtered
