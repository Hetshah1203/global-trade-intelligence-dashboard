import pandas as pd

def build_features(df, gdp, inflation):

    df["Growth_Rate"] = df["Export_Value"].pct_change()*100
    df["Demand_Score"] = df["Export_Value"]/df["Export_Value"].max()*100

    # Risk Score
    risk = (inflation*0.6) - (gdp/1e13)

    df["Risk_Score"] = abs(risk)*50

    df.fillna(0,inplace=True)

def build_features(df,gdp,inflation):
    df=df.copy()
    df["Growth_Rate"]=df["Export_Value"].pct_change().fillna(0)*100
    return df


    return df