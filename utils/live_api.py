import requests
import pandas as pd
import streamlit as st

# ---------------------------------------------------
# FETCH ALL COUNTRIES (LIVE API)
# ---------------------------------------------------
@st.cache_data(ttl=86400)
def fetch_all_countries():
    """
    Fetch all countries from World Bank API
    Cached for 24 hours.
    """

    url = "https://api.worldbank.org/v2/country?format=json&per_page=400"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        countries = {}

        for c in data[1]:
            # ignore aggregates like 'World', 'Europe'
            if c["region"]["value"] != "Aggregates":
                countries[c["name"]] = c["id"]

        # sort alphabetically
        countries = dict(sorted(countries.items()))

        return countries

    except Exception as e:
        print("Country API failed:", e)
        return {}


# ---------------------------------------------------
# EXPORT TIMESERIES (LIVE)
# Indicator: Merchandise exports (current USD)
# ---------------------------------------------------
@st.cache_data(ttl=3600)
def fetch_export_timeseries(code):

    url = f"https://api.worldbank.org/v2/country/{code}/indicator/TX.VAL.MRCH.CD.WT?format=json&per_page=60"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        rows = []

        for item in data[1]:
            if item["value"] is not None:
                rows.append({
                    "Year": int(item["date"]),
                    "Export_Value": float(item["value"])
                })

        df = pd.DataFrame(rows).sort_values("Year")

        return df

    except:
        return pd.DataFrame()


# ---------------------------------------------------
# GDP (LIVE)
# ---------------------------------------------------
@st.cache_data(ttl=3600)
def fetch_gdp(code):

    url = f"https://api.worldbank.org/v2/country/{code}/indicator/NY.GDP.MKTP.CD?format=json"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        for item in data[1]:
            if item["value"]:
                return float(item["value"])

    except:
        pass

    return None


# ---------------------------------------------------
# INFLATION (LIVE)
# ---------------------------------------------------
@st.cache_data(ttl=3600)
def fetch_inflation(code):

    url = f"https://api.worldbank.org/v2/country/{code}/indicator/FP.CPI.TOTL.ZG?format=json"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        for item in data[1]:
            if item["value"]:
                return float(item["value"])

    except:
        pass

    return None