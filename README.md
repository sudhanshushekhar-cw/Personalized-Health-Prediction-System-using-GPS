# Personalized-Health-Prediction-System-using-GPS
 Personalized Health Prediction System using GPS – Developed an ML model using Decision Tree and Random Forest (87% accuracy) to predict health risks by analyzing real-time AQI of the user's current location and their health history (age, medical conditions), integrated with GPS and Firebase to deliver personalized alerts and health tips.
# 🩺 Personalized Health Prediction System using GPS

A machine learning-based system that predicts individual health risks by analyzing real-time **Air Quality Index (AQI)** data and user-specific health information (like age and medical conditions). The model uses the **user's current GPS location** to fetch environmental data and provide **personalized health alerts and suggestions**.

---

## 🚀 Features

- ✅ Predicts health risk levels (Low / Moderate / High)
- 📍 Uses **GPS** to fetch real-time user location
- 🌫️ Fetches **live AQI** based on location
- 🧬 Considers personal health data (age, medical history, etc.)
- 🤖 Trained with **Random Forest** and **Decision Tree** classifiers
- 📈 Achieved ~87% accuracy in predictions
- ☁️ Integrated with **Firebase Realtime Database**
- 🔔 Sends real-time health alerts and suggestions

---

## 🛠️ Technologies Used

| Component              | Tech Stack                         |
|------------------------|------------------------------------|
| Machine Learning       | Python, Scikit-learn               |
| Data Processing        | Pandas, NumPy                      |
| Backend Integration    | Firebase Realtime Database         |
| Location Services      | GPS, Geolocation API               |
| Environmental Data     | AQI APIs                           |

---

## 📊 Model Workflow

1. Collect real-time AQI using user’s current location
2. Accept user health profile inputs (age, medical history)
3. Predict health risk using trained ML models
4. Generate a risk level (Low, Moderate, High)
5. Display personalized suggestions and alerts

---

## 🧪 Accuracy & Results

- **Algorithms Used:** Random Forest, Decision Tree
- **Accuracy Achieved:** ~87%
- **Evaluation Metric:** Classification Report (Precision, Recall, F1-Score)

---

## 📁 Project Structure

