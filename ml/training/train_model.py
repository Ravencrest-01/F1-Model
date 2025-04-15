import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.feature_engineering import FeatureEngineer
from models.podium_predictor import PodiumPredictor

def train_model():
    # Load environment variables
    load_dotenv()
    
    # Connect to MongoDB
    client = MongoClient(os.getenv('MONGODB_URI'))
    db = client.f1_predictor
    
    # Initialize feature engineering
    feature_engineer = FeatureEngineer(db)
    
    # Prepare training data
    print("Preparing training data...")
    X, y = feature_engineer.prepare_training_data(start_year=2000, end_year=2024)
    
    # Initialize and train the model
    print("Training model...")
    model = PodiumPredictor(input_dim=X.shape[1])
    history = model.train(X, y)
    
    # Save the model
    print("Saving model...")
    model.save('models/podium_predictor.h5')
    
    # Get feature importance
    print("Calculating feature importance...")
    importance = model.get_feature_importance(X)
    
    # Print feature importance
    feature_names = X.columns
    for name, imp in zip(feature_names, importance):
        print(f"{name}: {imp}")
    
    print("Training complete!")

if __name__ == "__main__":
    train_model() 