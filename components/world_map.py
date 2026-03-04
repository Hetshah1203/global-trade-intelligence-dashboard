import plotly.express as px

def world_map(df):

    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="AI_Score",
        title="Global Export Opportunity Map"
    )

    return fig