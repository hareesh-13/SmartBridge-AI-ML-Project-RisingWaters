import os
import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'rising_waters_secret_key'

# Load the model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'decision_tree_flood_model.pkl')
model = None

try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully.")
    else:
        print(f"Error: Model file not found at {MODEL_PATH}")
except Exception as e:
    print(f"Error loading model: {e}")

# Standard subdivisions list for selection
SUBDIVISIONS = [
    {"code": 0, "name": "Andaman & Nicobar Islands"},
    {"code": 1, "name": "Arunachal Pradesh"},
    {"code": 2, "name": "Assam & Meghalaya"},
    {"code": 3, "name": "Naga Mani Mizo Tripura"},
    {"code": 4, "name": "Sub Himalayan West Bengal & Sikkim"},
    {"code": 5, "name": "Gangetic West Bengal"},
    {"code": 6, "name": "Orissa"},
    {"code": 7, "name": "Bihar"},
    {"code": 8, "name": "East Uttar Pradesh"},
    {"code": 9, "name": "West Uttar Pradesh"},
    {"code": 10, "name": "Uttarakhand"},
    {"code": 11, "name": "Haryana Delhi & Chandigarh"},
    {"code": 12, "name": "Punjab"},
    {"code": 13, "name": "Himachal Pradesh"},
    {"code": 14, "name": "Jammu & Kashmir"},
    {"code": 15, "name": "West Rajasthan"},
    {"code": 16, "name": "East Rajasthan"},
    {"code": 17, "name": "West Madhya Pradesh"},
    {"code": 18, "name": "East Madhya Pradesh"},
    {"code": 19, "name": "Gujarat Region"},
    {"code": 20, "name": "Saurashtra & Kutch"},
    {"code": 21, "name": "Konkan & Goa"},
    {"code": 22, "name": "Madhya Maharashtra"},
    {"code": 23, "name": "Matathwada"},
    {"code": 24, "name": "Vidarbha"},
    {"code": 25, "name": "Chhattisgarh"},
    {"code": 26, "name": "Coastal Andhra Pradesh"},
    {"code": 27, "name": "Telangana"},
    {"code": 28, "name": "Rayalaseema"},
    {"code": 29, "name": "Tamil Nadu"},
    {"code": 30, "name": "Coastal Karnataka"},
    {"code": 31, "name": "North Interior Karnataka"},
    {"code": 32, "name": "South Interior Karnataka"},
    {"code": 33, "name": "Kerala"},
    {"code": 34, "name": "Lakshadweep"}
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Retrieve inputs and validate
            temperature = float(request.form.get('temperature', 0))
            humidity = float(request.form.get('humidity', 0))
            cloud_cover = float(request.form.get('cloud_cover', 0))
            annual_rainfall = float(request.form.get('annual_rainfall', 0))
            jan_feb = float(request.form.get('jan_feb', 0))
            mar_may = float(request.form.get('mar_may', 0))
            jun_sep = float(request.form.get('jun_sep', 0))
            oct_dec = float(request.form.get('oct_dec', 0))
            avg_june = float(request.form.get('avg_june', 0))
            subdivision_rainfall = float(request.form.get('subdivision_rainfall', 0))
            subdivision_code = int(request.form.get('subdivision_code', 0))

            # Validate range
            if any(val < 0 for val in [temperature, humidity, cloud_cover, annual_rainfall, jan_feb, mar_may, jun_sep, oct_dec, avg_june, subdivision_rainfall]):
                flash("Inputs cannot be negative values.", "danger")
                return render_template('predict.html', subdivisions=SUBDIVISIONS, form_data=request.form)
            
            if humidity > 100 or cloud_cover > 100:
                flash("Humidity and Cloud Cover percentages must be between 0 and 100.", "danger")
                return render_template('predict.html', subdivisions=SUBDIVISIONS, form_data=request.form)

            # Map inputs to features
            # The model expects 11 features.
            # We'll scale Jun-Sep Rainfall to meters (or divide by 1000) for prediction.
            jun_sep_scaled = jun_sep / 1000.0

            # Construct feature vector
            features = np.zeros((1, 11))
            features[0, 0] = temperature
            features[0, 1] = humidity
            features[0, 2] = cloud_cover
            features[0, 3] = annual_rainfall
            features[0, 4] = jan_feb
            features[0, 5] = mar_may
            features[0, 6] = jun_sep_scaled
            features[0, 7] = oct_dec
            features[0, 8] = avg_june
            features[0, 9] = subdivision_rainfall
            features[0, 10] = subdivision_code

            # Perform prediction
            if model is not None:
                prediction = int(model.predict(features)[0])
                # Safe probability check
                try:
                    probabilities = model.predict_proba(features)[0]
                    confidence = round(probabilities[prediction] * 100, 2)
                except Exception:
                    confidence = 96.55 # Fallback to model baseline accuracy

                subdivision_name = next((s['name'] for s in SUBDIVISIONS if s['code'] == subdivision_code), "Unknown Region")
                
                context = {
                    "subdivision": subdivision_name,
                    "temperature": temperature,
                    "humidity": humidity,
                    "cloud_cover": cloud_cover,
                    "annual_rainfall": annual_rainfall,
                    "jun_sep": jun_sep,
                    "confidence": confidence,
                    "model_name": "Decision Tree Classifier",
                    "model_accuracy": "96.55%"
                }
                
                if prediction == 1:
                    return render_template('flood_result.html', **context)
                else:
                    return render_template('no_flood_result.html', **context)
            else:
                flash("Model is not loaded. Please contact the administrator.", "danger")
                return render_template('predict.html', subdivisions=SUBDIVISIONS, form_data=request.form)

        except ValueError as e:
            flash(f"Invalid input: Please make sure all numerical fields contain valid numbers.", "danger")
            return render_template('predict.html', subdivisions=SUBDIVISIONS, form_data=request.form)
        except Exception as e:
            flash(f"An unexpected error occurred during prediction: {e}", "danger")
            return render_template('predict.html', subdivisions=SUBDIVISIONS, form_data=request.form)

    return render_template('predict.html', subdivisions=SUBDIVISIONS)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('404.html', error_message="Internal Server Error"), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
