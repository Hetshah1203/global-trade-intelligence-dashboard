import pandas as pd
import streamlit as st
import time
from utils.live_api import fetch_export_timeseries, fetch_inflation


# -------- REGION FILTER --------
def filter_region(countries, group):

    if group == "All":
        return countries

    ranges = {
        "A–F": ("A","F"),
        "G–L": ("G","L"),
        "M–R": ("M","R"),
        "S–Z": ("S","Z")
    }

    start, end = ranges[group]

    return {
        k:v for k,v in countries.items()
        if start <= k[0].upper() <= end
    }


# -------- GLOBAL RANKING (DAILY CACHE) --------
@st.cache_data(ttl=86400)
def compute_global_ranking(countries):

    sample_countries = list(countries.items())[:20]

    rank = []

    for name, code in sample_countries:

        df = fetch_export_timeseries(code)

        if df is None or df.empty:
            continue

        infl = fetch_inflation(code)

        latest_export = df["Export_Value"].iloc[-1]

        score = (latest_export / 1e9) - (infl * 2)

        rank.append({
            "Country": name,
            "Score": float(score)
        })

        time.sleep(0.2)

    if len(rank) == 0:
        return pd.DataFrame({"Country": [], "Score": []})

    return pd.DataFrame(rank).sort_values(
        "Score",
        ascending=False
    )