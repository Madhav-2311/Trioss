from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import datetime

app = Flask(__name__)

solar_model = joblib.load("models/solar_model.pkl")
load_model = joblib.load("models/load_model.pkl")
outage_model = joblib.load("models/outage_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict_solar", methods=["POST"])
def predict_solar():
    try:
        data = request.get_json()

        hour = float(data["hour"])
        temp = float(data["temperature"])
        irradiance = float(data["irradiance"])
        humidity = float(data["humidity"])

        features = np.array([[hour, temp, irradiance, humidity]])

        prediction = float(solar_model.predict(features)[0])

        return jsonify({"result": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/predict_load", methods=["POST"])
def predict_load():
    try:
        data = request.get_json()

        date = datetime.datetime.strptime(data["date"], "%Y-%m-%d")
        hour = float(data["hour"])
        temp = float(data["temperature"])
        humidity = float(data["humidity"])
        day_of_week = date.weekday()

        features = np.array([[hour, temp, humidity, day_of_week]])

        prediction = float(load_model.predict(features)[0])

        return jsonify({"result": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/predict_outage", methods=["POST"])
def predict_outage():
    try:
        data = request.get_json()

        wind = float(data["wind"])
        rainfall = float(data["rainfall"])
        temp = float(data["temperature"])
        storm = 1 if data["storm"] == "Yes" else 0

        features = np.array([[wind, rainfall, temp, storm]])

        if hasattr(outage_model, "predict_proba"):
            prediction = float(outage_model.predict_proba(features)[0][1])
        else:
            prediction = float(outage_model.predict(features)[0])

        return jsonify({"result": prediction})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)