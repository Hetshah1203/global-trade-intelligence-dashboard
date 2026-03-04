import plotly.express as px

def trade_flow_animation(df):

    if df.empty:
        return px.scatter_geo()

    # ---------- SAFE SIZE (NO NEGATIVES) ----------
    df["BubbleSize"] = (
        df["Opportunity"] - df["Opportunity"].min()
    ) + 1

    fig = px.scatter_geo(
        df,
        locations="Country",
        locationmode="country names",
        size="BubbleSize",
        animation_frame="Year",
        color="Opportunity",
        color_continuous_scale="Viridis",
        projection="natural earth",
        title="🌐 Global Trade Opportunity Flow"
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0)
    )

    return fig