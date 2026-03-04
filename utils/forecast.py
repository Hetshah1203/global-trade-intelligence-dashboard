from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

def forecast_exports(df):

    X = df["Year"].values.reshape(-1,1)
    y = df["Export_Value"].values

    model = LinearRegression()
    model.fit(X,y)

    future_years = np.arange(df["Year"].max()+1,
                             df["Year"].max()+6)

    preds = model.predict(future_years.reshape(-1,1))

    forecast = pd.DataFrame({
        "Year":future_years,
        "Export_Value":preds
    })

def forecast_exports(df):
    last=df.iloc[-1]["Export_Value"]
    return pd.DataFrame({
        "Year":[2024,2025],
        "Export_Value":[last*1.05,last*1.1]
    })

    return forecast