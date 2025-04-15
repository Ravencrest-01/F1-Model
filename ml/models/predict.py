import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
import tensorflow as tf
import numpy as np

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.feature_engineering import FeatureEngineer
from models.podium_predictor import PodiumPredictor

class RacePrediction:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Connect to MongoDB
        self.client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.client.f1_predictor
        
        # Initialize feature engineering
        self.feature_engineer = FeatureEngineer(self.db)
        
        # Load the model
        self.model = None
    
    def load_model(self, model_path='models/podium_predictor.h5'):
        """Load the trained model"""
        self.model = tf.keras.models.load_model(model_path)
    
    def predict_race(self, year, round):
        """Make predictions for a specific race"""
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        # Prepare prediction data
        X, driver_ids = self.feature_engineer.prepare_prediction_data(year, round)
        
        # Get predictions
        probabilities = self.model.predict(X)
        
        # Sort drivers by probability
        driver_probs = list(zip(driver_ids, probabilities.flatten()))
        driver_probs.sort(key=lambda x: x[1], reverse=True)
        
        # Get top 3 predictions
        top_3 = driver_probs[:3]
        
        # Get driver details
        predictions = []
        for driver_id, prob in top_3:
            driver = self.db.drivers.find_one({'driver_id': driver_id})
            predictions.append({
                'position': len(predictions) + 1,
                'driver_id': driver_id,
                'driver_name': driver['name'],
                'probability': float(prob)
            })
        
        return predictions
    
    def get_driver_chances(self, driver_id, year, round):
        """Get podium chances for a specific driver"""
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        # Prepare prediction data
        X, driver_ids = self.feature_engineer.prepare_prediction_data(year, round)
        
        # Find index of the driver
        try:
            driver_index = driver_ids.index(driver_id)
        except ValueError:
            return None
        
        # Get prediction for the driver
        probability = float(self.model.predict(X[driver_index:driver_index+1])[0])
        
        return {
            'driver_id': driver_id,
            'podium_probability': probability
        }
    
    def get_all_driver_chances(self, year, round):
        """Get podium chances for all drivers"""
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        # Prepare prediction data
        X, driver_ids = self.feature_engineer.prepare_prediction_data(year, round)
        
        # Get predictions for all drivers
        probabilities = self.model.predict(X).flatten()
        
        # Create results
        results = []
        for driver_id, prob in zip(driver_ids, probabilities):
            driver = self.db.drivers.find_one({'driver_id': driver_id})
            results.append({
                'driver_id': driver_id,
                'driver_name': driver['name'],
                'podium_probability': float(prob)
            })
        
        # Sort by probability
        results.sort(key=lambda x: x['podium_probability'], reverse=True)
        
        return results

if __name__ == "__main__":
    # Example usage
    predictor = RacePrediction()
    predictor.load_model()
    
    # Example: Predict next race
    year = 2025
    round = 1
    predictions = predictor.predict_race(year, round)
    
    print("\nPredicted Podium:")
    for pred in predictions:
        print(f"{pred['position']}. {pred['driver_name']} ({pred['probability']:.2%})") 