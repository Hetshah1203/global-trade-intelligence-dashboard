import xgboost as xgb

def train_ai(df):

    X = df[["Demand_Score","Growth_Rate","Market_Stability"]]

    y = (
        0.5*df["Demand_Score"]
        +0.3*df["Growth_Rate"]
        +0.2*df["Market_Stability"]
    )

    model = xgb.XGBRegressor(
        n_estimators=120,
        max_depth=4
    )

    model.fit(X,y)

    df["Opportunity_Score"] = model.predict(X)

    return df.sort_values(
        "Opportunity_Score",
        ascending=False
    )