import pandas as pd
import streamlit as st

@st.cache_data
def load_worldbank():

    df = pd.read_csv(
        "data/worldbank_exports.csv",
        skiprows=4
    )

    df = df.melt(
        id_vars=["Country Name","Country Code"],
        var_name="Year",
        value_name="Export_Value"
    )

    df.dropna(inplace=True)

    return df


@st.cache_data
def load_services():

    try:
        df = pd.read_csv("data/TiSMoS.csv")
        return df
    except:
        return pd.DataFrame()