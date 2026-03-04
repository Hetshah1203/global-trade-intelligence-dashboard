import plotly.express as px

def demand_chart(df):
    fig = px.bar(
        df,
        x="Country",
        y="Demand_Score",
        title="Demand Score by Country"
    )
    return fig

def growth_tariff_chart(df):
    fig = px.scatter(
        df,
        x="Tariff_Percent",
        y="Growth_Rate",
        size="Demand_Score",
        color="Country",
        title="Market Attractiveness Map"
    )
    return fig