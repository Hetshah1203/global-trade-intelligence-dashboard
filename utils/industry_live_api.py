import requests
import pandas as pd
import streamlit as st

# WTO-based approximate global trade shares
INDUSTRY_WEIGHTS = {
    "Clothing": 0.12,
    "Grains": 0.08,
    "Pulses": 0.05,
    "Electronics": 0.22,
    "Pharmaceuticals": 0.10,
    "Chemicals": 0.15,
    "Machinery": 0.18,
    "Food Processing": 0.10
}


@st.cache_data(ttl=3600)
def fetch_industry_exports(country_code):

    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/TX.VAL.MRCH.CD.WT?format=json&per_page=5"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        if len(data) < 2:
            return pd.DataFrame()

        df = pd.DataFrame(data[1])[["date", "value"]]
        df = df.dropna()

        if df.empty:
            return pd.DataFrame()

        latest_export = float(df.iloc[0]["value"])

        industry_data = []

        for industry, weight in INDUSTRY_WEIGHTS.items():
            industry_data.append({
                "Industry": industry,
                "Export_Value_USD": latest_export * weight
            })

        def fetch_industry_exports(code):
            return pd.DataFrame()

        return pd.DataFrame(industry_data)

    except Exception:
        return pd.DataFrame()