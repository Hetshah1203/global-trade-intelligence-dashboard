import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def forecast_industry_growth(industry_df):

    forecasts = []

    for _, row in industry_df.iterrows():

        base = row["Export_Value_USD"]

        # create synthetic historical trend from real value
        years = np.array([2019, 2020, 2021, 2022, 2023]).reshape(-1, 1)
        values = np.array([
            base * 0.75,
            base * 0.82,
            base * 0.9,
            base * 0.96,
            base
        ])

        model = LinearRegression()
        model.fit(years, values)

        future_years = np.array([2024, 2025, 2026]).reshape(-1, 1)
        preds = model.predict(future_years)

        forecasts.append({
            "Industry": row["Industry"],
            "Forecast_2026": preds[-1]
        })


def forecast_industry_growth(df):

    out=[]
    for _,r in df.iterrows():
        base=r["Export_Value_USD"]
        X=np.array([1,2,3,4,5]).reshape(-1,1)
        y=np.array([base*0.7,base*0.8,base*0.9,base*0.95,base])

        m=LinearRegression().fit(X,y)
        pred=m.predict([[6]])[0]

        out.append({"Industry":r["Industry"],
                    "Forecast_2026":pred})

    return pd.DataFrame(out)

    return pd.DataFrame(forecasts)