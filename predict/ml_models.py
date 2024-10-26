# predict/ml_models.py

import joblib  # For loading the scaler
import numpy as np
from tensorflow.keras.models import load_model


class HealthRiskModel:
    def __init__(self, model_path, scaler_path):
        """Initialize the HealthRiskModel with the specified model and scaler paths."""
        self.model_path = model_path
        self.scaler_path = scaler_path
        self.model = self.load_health_risk_model()
        self.scaler = self.load_scaler()

    def load_health_risk_model(self):
        """Load the trained TensorFlow model from the specified path."""
        try:
            return load_model(self.model_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")

    def load_scaler(self):
        """Load the scaler from the specified path."""
        try:
            return joblib.load(self.scaler_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load scaler: {e}")

    def preprocess_data(self, health_data):
        """Preprocess health data for model input."""
        # Ensure that input health_data is valid
        required_keys = ['diet', 'stress', 'activity', 'sleep', 'biometrics', 'medications', 'family_history',
                         'genetic_markers', 'environmental_factors']
        if not all(key in health_data for key in required_keys):
            raise ValueError("Health data is missing required fields.")

        data = np.array([
            health_data['diet'],
            health_data['stress'],
            health_data['activity'],
            health_data['sleep'],
            health_data['biometrics'],
            health_data['medications'],
            health_data['genetic_markers'],  # Assuming this is a numeric representation of genetic risk factors
            health_data['environmental_factors'],  # Numeric values for environmental influences
            1 if 'cardiovascular' in health_data['family_history'].lower() else 0,
            1 if 'diabetes' in health_data['family_history'].lower() else 0,
        ]).reshape(1, -1)

        return self.scaler.transform(data)

    def predict_health_risk(self, health_data):
        """Make health risk predictions for multiple diseases based on the provided health data."""
        processed_data = self.preprocess_data(health_data)
        risk_scores = self.model.predict(processed_data)  # Returns an array of risk scores for multiple diseases
        return risk_scores

    def generate_risk_report(self, risk_scores):
        """Generate health risk reports based on the predicted risk scores for multiple diseases."""
        disease_names = ['Diabetes', 'Cardiovascular Disease', 'Hypertension']  # Example diseases
        reports = []

        for disease, score in zip(disease_names, risk_scores[0]):  # Assuming risk_scores is a 2D array
            if score > 8:
                reports.append(f"{disease} risk is high. Consider consulting a healthcare provider.")
            elif 5 <= score <= 8:
                reports.append(f"{disease} risk is moderate. Keep monitoring your health parameters.")
            else:
                reports.append(f"{disease} risk is low. Keep up the good work!")

        return reports

    def generate_personalized_recommendations(self, risk_scores):
        """Provide personalized recommendations based on risk scores."""
        recommendations = []
        for score in risk_scores[0]:
            if score > 8:
                recommendations.append("Increase physical activity and consult a healthcare provider.")
            elif 5 <= score <= 8:
                recommendations.append("Maintain a balanced diet and regular health check-ups.")
            else:
                recommendations.append("Continue healthy lifestyle habits.")

        return recommendations

# Usage
# health_risk_model = HealthRiskModel('path/to/health_risk_model.h5', 'path/to/scaler.pkl')
# risk_scores = health_risk_model.predict_health_risk(health_data_dict)
# reports = health_risk_model.generate_risk_report(risk_scores)
# recommendations = health_risk_model.generate_personalized_recommendations(risk_scores)
