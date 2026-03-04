import streamlit as st
import pandas as pd
import plotly.express as px
import random

from utils.live_api import (
    fetch_export_timeseries,
    fetch_gdp,
    fetch_inflation,
    fetch_all_countries
)

from utils.analytics_engine import build_features
from utils.industry_live_api import fetch_industry_exports
from utils.industry_forecast import forecast_industry_growth


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="Global Trade Intelligence", layout="wide")

# ---------------------------------------------------
# PROFESSIONAL UI STYLE
# ---------------------------------------------------
st.markdown("""
<style>

.block-container{
    padding-top:1.5rem;
}

.dashboard-card{
    background:#161B22;
    padding:18px;
    border-radius:12px;
    box-shadow:0px 4px 18px rgba(0,0,0,0.45);
    margin-bottom:12px;
}

.section-title{
    font-size:20px;
    font-weight:600;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.title("🌍 Global Trade Intelligence")
st.markdown(
"##### AI-Driven Global Trade Strategy & Market Intelligence Platform"
)

st.divider()

# ---------------------------------------------------
# COUNTRY LIST
# ---------------------------------------------------
countries = fetch_all_countries()

if not countries:
    countries = {
        "India":"IND",
        "United States":"USA",
        "Germany":"DEU",
        "China":"CHN",
        "Japan":"JPN"
    }

country_names = list(countries.keys())

colA, colB = st.columns(2)

with colA:
    primary_country = st.selectbox("Primary Country", country_names)

with colB:
    compare_country = st.selectbox("Compare With", country_names, index=1)

primary_code = countries[primary_country]
compare_code = countries[compare_country]


# ---------------------------------------------------
# COUNTRY METRIC ENGINE
# ---------------------------------------------------
def load_country_metrics(code):

    exports = fetch_export_timeseries(code)
    gdp = fetch_gdp(code)
    inflation = fetch_inflation(code)

    if exports is None or exports.empty:
        exports = pd.DataFrame({
            "Year":[2020,2021,2022,2023],
            "Export_Value":[1e9,1.1e9,1.2e9,1.3e9]
        })

    if gdp is None:
        gdp = 1e12

    if inflation is None:
        inflation = 5.0

    data = build_features(exports, gdp, inflation)
    latest = data.iloc[-1]

    growth = latest["Growth_Rate"]
    export_value = latest["Export_Value"]

    opportunity = max(5, min(100, growth*10 - inflation*2))
    risk = min(100, inflation*10)

    return {
        "exports": exports,
        "growth": growth,
        "export_value": export_value,
        "gdp": gdp,
        "inflation": inflation,
        "opportunity": opportunity,
        "risk": risk
    }


primary = load_country_metrics(primary_code)
compare = load_country_metrics(compare_code)

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
st.subheader("Executive Indicators")

kpi1, kpi2 = st.columns(2)

with kpi1:
    st.markdown(f"### 🇺🇳 {primary_country}")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Exports", f"${primary['export_value']/1e9:.2f}B")
    c2.metric("Growth", f"{primary['growth']:.2f}%")
    c3.metric("GDP", f"${primary['gdp']/1e12:.2f}T")
    c4.metric("Inflation", f"{primary['inflation']:.2f}%")

with kpi2:
    st.markdown(f"### 🌐 {compare_country}")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Exports", f"${compare['export_value']/1e9:.2f}B")
    c2.metric("Growth", f"{compare['growth']:.2f}%")
    c3.metric("GDP", f"${compare['gdp']/1e12:.2f}T")
    c4.metric("Inflation", f"{compare['inflation']:.2f}%")


# ---------------------------------------------------
# EXECUTIVE AI SUMMARY
# ---------------------------------------------------
industry_df = fetch_industry_exports(primary_code)

if industry_df is None or industry_df.empty:

    base = primary["export_value"]

    weights = {
        "Electronics":0.22,
        "Machinery":0.18,
        "Chemicals":0.15,
        "Clothing":0.12,
        "Pharmaceuticals":0.10,
        "Food":0.10,
        "Grains":0.08,
        "Pulses":0.05
    }

    industry_df = pd.DataFrame({
        "Industry":weights.keys(),
        "Export_Value_USD":[base*w for w in weights.values()]
    })

forecast_df = forecast_industry_growth(industry_df)

best_industry = forecast_df.sort_values(
    "Forecast_2026",
    ascending=False
).iloc[0]["Industry"]

summary = f"""
**{primary_country}** currently shows export growth of **{primary['growth']:.2f}%** 
with inflation at **{primary['inflation']:.2f}%**, indicating moderate trade stability. 
Comparatively, **{compare_country}** demonstrates a growth rate of **{compare['growth']:.2f}%**.  
Based on projected trade expansion, the **{best_industry} sector** offers the strongest 
future export opportunity driven by global demand and competitive supply advantages.
"""

st.markdown("###  Executive Insight Summary")
st.info(summary)

# ---------------------------------------------------
# GRID ROW 1
# ---------------------------------------------------
col1, col2 = st.columns(2)

# EXPORT TREND
with col1:

    df1 = primary["exports"].copy()
    df2 = compare["exports"].copy()

    df1["Country"] = primary_country
    df2["Country"] = compare_country

    combined = pd.concat([df1, df2])

    fig_line = px.line(
        combined,
        x="Year",
        y="Export_Value",
        color="Country",
        markers=True
    )

    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Export Performance Comparison</div>', unsafe_allow_html=True)

    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# INDUSTRY FORECAST
with col2:

    fig_ind = px.bar(
        forecast_df,
        x="Industry",
        y="Forecast_2026",
        color="Forecast_2026"
    )

    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Industry Growth Forecast</div>', unsafe_allow_html=True)

    st.plotly_chart(fig_ind, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# GRID ROW 2
# ---------------------------------------------------
col3, col4 = st.columns(2)

# DECISION MATRIX
with col3:

    quad_df = pd.DataFrame({
        "Country":[primary_country, compare_country],
        "Opportunity":[primary["opportunity"], compare["opportunity"]],
        "Risk":[primary["risk"], compare["risk"]]
    })

    fig_quad = px.scatter(
        quad_df,
        x="Risk",
        y="Opportunity",
        text="Country",
        size="Opportunity",
        color="Opportunity"
    )

    fig_quad.update_traces(textposition="top center")

    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Decision Intelligence Matrix</div>', unsafe_allow_html=True)

    st.plotly_chart(fig_quad, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# INDUSTRY MARKET RECOMMENDER
# ---------------------------------------------------
with col4:

    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Best Market Recommender</div>', unsafe_allow_html=True)

    if st.button("Find Best Expansion Markets"):

        industries = [
            "Electronics","Machinery","Chemicals","Clothing",
            "Grains","Pulses","Pharmaceuticals","Food Processing"
        ]

        industry_weights = {
            "Electronics":1.6,
            "Machinery":1.4,
            "Chemicals":1.3,
            "Clothing":1.1,
            "Grains":1.0,
            "Pulses":0.9,
            "Pharmaceuticals":1.5,
            "Food Processing":1.2
        }

        results = []

        country_pool = list(countries.items())
        random.shuffle(country_pool)

        sample_countries = country_pool[:50]

        for industry in industries:

            best_country = None
            best_score = -999

            for name, code in sample_countries:

                metrics = load_country_metrics(code)

                gdp_factor = metrics["gdp"] / 1e12

                score = (
                    metrics["opportunity"] * industry_weights[industry]
                    + gdp_factor * 5
                    - metrics["risk"] * 0.6
                )

                if score > best_score:
                    best_score = score
                    best_country = name

            results.append({
                "Industry":industry,
                "Best Market":best_country,
                "Opportunity Score":round(best_score,2)
            })

        result_df = pd.DataFrame(results)

        st.dataframe(result_df, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# GLOBAL TRADE OPPORTUNITY RANKING
# ---------------------------------------------------
st.markdown("###  Global Trade Opportunity Ranking")

ranking = []

country_pool = list(countries.items())
random.shuffle(country_pool)

for name, code in country_pool[:20]:

    metrics = load_country_metrics(code)

    score = metrics["opportunity"] - metrics["risk"]*0.5

    ranking.append({
        "Country":name,
        "Opportunity Score":round(score,2)
    })

rank_df = pd.DataFrame(ranking).sort_values(
    "Opportunity Score",
    ascending=False
)

st.dataframe(rank_df, use_container_width=True)

fig_rank = px.bar(
    rank_df,
    x="Country",
    y="Opportunity Score",
    title="Top 20 Global Trade Expansion Opportunities"
)

st.plotly_chart(fig_rank, use_container_width=True)