import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import os

class HeartDiseasePredictor:
    def __init__(self):
        self.model = None
        self.load_or_train_model()
    
    def load_or_train_model(self):
        """Load existing model or train new one"""
        model_path = "backend/heart_disease_model.pkl"
        
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
        else:
            self.train_model()
            joblib.dump(self.model, model_path)
    
    def train_model(self):
        """Train the heart disease prediction model"""
        # Load the dataset
        heart_disease = pd.read_csv('heart_disease_data.csv')
        
        # Prepare features and target
        X = heart_disease.drop(columns='target', axis=1)
        y = heart_disease['target']
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train the model
        self.model = LogisticRegression(max_iter=1000, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Calculate accuracy
        train_accuracy = accuracy_score(y_train, self.model.predict(X_train))
        test_accuracy = accuracy_score(y_test, self.model.predict(X_test))
        
        print(f"Training Accuracy: {train_accuracy:.4f}")
        print(f"Testing Accuracy: {test_accuracy:.4f}")
    
    def predict(self, clinical_data):
        """
        Make prediction for heart disease
        
        Args:
            clinical_data: List of clinical parameters in order:
                [age, sex, cp, trestbps, chol, fbs, restecg, thalach, 
                 exang, oldpeak, slope, ca, thal]
        
        Returns:
            tuple: (probability, risk_level)
        """
        if self.model is None:
            raise ValueError("Model not trained or loaded")
        
        # Convert to numpy array and reshape
        input_data = np.array(clinical_data).reshape(1, -1)
        
        # Get prediction probability
        probability = self.model.predict_proba(input_data)[0][1]  # Probability of class 1 (disease)
        
        # Determine risk level
        if probability >= 0.5:
            risk_level = "High Risk"
        else:
            risk_level = "Low Risk"
        
        return float(probability), risk_level
    
    def get_feature_importance(self):
        """Get feature importance from the model"""
        if self.model is None:
            raise ValueError("Model not trained or loaded")
        
        feature_names = [
            'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
            'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
        ]
        
        importance = abs(self.model.coef_[0])
        feature_importance = dict(zip(feature_names, importance))
        
        return sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)