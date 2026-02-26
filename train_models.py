import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score


def train_solar_model():
    solar_df = pd.read_csv("data/solar_forecast_dataset.csv")

    X = solar_df[[
        "temperature_c",
        "irradiance_wm2",
        "humidity_percent",
        "cloud_cover_percent"
    ]]
    y = solar_df["solar_generation_kw"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("Solar R2:", r2_score(y_test, predictions))
    joblib.dump(model, "models/solar_model.pkl")


def train_load_model():
    load_df = pd.read_csv("data/load_forecast_dataset.csv")

    X = load_df[[
        "temperature_c",
        "humidity_percent",
        "hour",
        "day_of_week"
    ]]
    y = load_df["energy_consumption_kw"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("Load R2:", r2_score(y_test, predictions))
    joblib.dump(model, "models/load_model.pkl")


def train_outage_model():
    outage_df = pd.read_csv("data/outage_prediction_dataset.csv")

    X = outage_df[[
        "wind_speed_kmh",
        "rainfall_mm",
        "temperature_c",
        "storm_indicator"
    ]]
    y = outage_df["outage"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("Outage Accuracy:", accuracy_score(y_test, predictions))
    joblib.dump(model, "models/outage_model.pkl")


if __name__ == "__main__":
    train_solar_model()
    train_load_model()
    train_outage_model()