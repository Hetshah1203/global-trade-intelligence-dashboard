def create_features(df):

    df = df.sort_values("Year")

    df["Growth_Rate"] = df["Export_Value"].pct_change()*100
    df["Demand_Score"] = (
        df["Export_Value"]/df["Export_Value"].max()
    )*100

    df["Market_Stability"] = (
        100 - df["Growth_Rate"].abs().fillna(0)
    )

    df.fillna(0,inplace=True)

    return df