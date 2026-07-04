# Rising Waters: Intelligent Flood Prediction & Early Warning System

Rising Waters is a production-ready Machine Learning web application designed to predict flood occurrences based on historical meteorological statistics and sub-divisional rainfall distribution. By utilizing an optimized Decision Tree Classifier, the system provides real-time risk assessments to aid disaster response planners, meteorologists, and civil defense agencies in taking timely preventative measures.

## 🚀 Key Features

* **Machine Learning Predictions**: Leverages a local Decision Tree model to classify high-risk precipitation indices.
* **Responsive Visuals**: A beautiful, modern interface with glassmorphism panels, CSS gradient accents, and dynamic animations.
* **Model Accuracy Metrics**: Displays the 96.55% accuracy evaluation and detailed risk confidence for transparency.
* **Auto-fill Presets**: Quick demo buttons to immediately load extreme flood thresholds or safe weather parameters.
* **Early Warning Guides**: Integrated emergency preparation steps and safety procedures depending on risk levels.
* **Fully Responsive**: Tailored grid layout compatible with desktop workstations and smartphones.

---

## 🛠️ Technology Stack

* **Backend Framework**: Python (Flask)
* **ML Integration**: Scikit-Learn, Joblib, NumPy, Pandas
* **UI/UX Core**: HTML5, CSS3 (Vanilla design variables), JavaScript (Vanilla ES6)
* **CSS Framework**: Bootstrap 5
* **Iconography**: Font Awesome 6

---

## 📁 Project Structure

```text
Rising_Waters/
│
├── app.py
├── requirements.txt
├── README.md
│
├── model/
│   └── decision_tree_flood_model.pkl
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│       ├── hero.jpg
│       ├── flood.jpg
│       └── logo.png
│
└── templates/
    ├── base.html
    ├── home.html
    ├── predict.html
    ├── flood_result.html
    ├── no_flood_result.html
    └── 404.html
```

---

## ⚙️ Installation & Execution

Follow these steps to run the application locally on your machine:

### 1. Set Up a Virtual Environment
Initialize a clean environment to isolate project packages:
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Project Dependencies
Install Flask, Pandas, NumPy, Scikit-learn, and Joblib:
```bash
pip install -r requirements.txt
```

### 3. Start the Web Server
Launch the development server:
```bash
python app.py
```
By default, the application will start at `http://127.0.0.1:5000/`.

---

## 🧠 Model Specifications

The predictive engine uses a **Decision Tree Classifier** trained on historical sub-divisional rainfall data. 

* **Accuracy**: 96.55%
* **Feature Vector**: Accepts 11 inputs including temperature, humidity, cloud cover, annual rain, and quarterly seasonal splits.
* **Key Threshold**: The model splits primary decisions on the **June-September Cumulative Rainfall** parameter (Feature Index 6), identifying that rainfall levels scaling above `1091.89 mm` during monsoon months heavily correlate to region-wide flood situations.
