import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler, LabelEncoder

class FeatureEngineer:
    def __init__(self, db):
        self.db = db
        self.scaler = StandardScaler()
        self.driver_encoder = LabelEncoder()
        self.team_encoder = LabelEncoder()
        self.circuit_encoder = LabelEncoder()
        
    def get_driver_features(self, driver_id, year, round):
        """Extract features for a specific driver"""
        features = {}
        
        # Get driver's historical performance
        driver_races = list(self.db.races.find({
            'results.driver_id': driver_id,
            'year': {'$lt': year}
        }))
        
        # Calculate average finishing position
        positions = [int(r['position']) for race in driver_races 
                    for r in race['results'] if r['driver_id'] == driver_id]
        features['avg_position'] = np.mean(positions) if positions else 20
        
        # Calculate win rate
        wins = sum(1 for p in positions if p == 1)
        features['win_rate'] = wins / len(positions) if positions else 0
        
        # Calculate podium rate
        podiums = sum(1 for p in positions if p <= 3)
        features['podium_rate'] = podiums / len(positions) if positions else 0
        
        # Get track-specific performance
        current_race = self.db.races.find_one({'year': year, 'round': round})
        circuit = current_race['circuit']
        
        circuit_races = [race for race in driver_races 
                        if race['circuit'] == circuit]
        circuit_positions = [int(r['position']) for race in circuit_races 
                           for r in race['results'] if r['driver_id'] == driver_id]
        
        features['circuit_avg_position'] = np.mean(circuit_positions) if circuit_positions else 20
        features['circuit_podium_rate'] = sum(1 for p in circuit_positions if p <= 3) / len(circuit_positions) if circuit_positions else 0
        
        # Get recent form (last 5 races)
        recent_races = sorted(driver_races, key=lambda x: (x['year'], x['round']))[-5:]
        recent_positions = [int(r['position']) for race in recent_races 
                          for r in race['results'] if r['driver_id'] == driver_id]
        
        features['recent_avg_position'] = np.mean(recent_positions) if recent_positions else 20
        features['recent_podium_rate'] = sum(1 for p in recent_positions if p <= 3) / len(recent_positions) if recent_positions else 0
        
        # Get qualifying performance
        qualifying_positions = [int(r['grid']) for race in recent_races 
                              for r in race['results'] if r['driver_id'] == driver_id]
        features['avg_qualifying_position'] = np.mean(qualifying_positions) if qualifying_positions else 20
        
        # Get team performance
        current_team = next((r['constructor_name'] for race in recent_races 
                           for r in race['results'] if r['driver_id'] == driver_id), None)
        
        if current_team:
            team_races = list(self.db.races.find({
                'results.constructor_name': current_team,
                'year': year
            }))
            
            team_positions = [int(r['position']) for race in team_races 
                            for r in race['results'] if r['constructor_name'] == current_team]
            
            features['team_avg_position'] = np.mean(team_positions) if team_positions else 20
            features['team_podium_rate'] = sum(1 for p in team_positions if p <= 3) / len(team_positions) if team_positions else 0
        
        return features
    
    def prepare_training_data(self, start_year=2000, end_year=2024):
        """Prepare training data for the model"""
        X = []
        y = []
        
        for year in range(start_year, end_year + 1):
            races = list(self.db.races.find({'year': year}))
            
            for race in races:
                # Get all drivers in the race
                drivers = [r['driver_id'] for r in race['results']]
                
                # Prepare features for each driver
                for driver_id in drivers:
                    features = self.get_driver_features(driver_id, year, race['round'])
                    
                    # Add encoded categorical features
                    features['driver_encoded'] = self.driver_encoder.fit_transform([driver_id])[0]
                    features['circuit_encoded'] = self.circuit_encoder.fit_transform([race['circuit']])[0]
                    
                    # Get the actual finishing position
                    position = next(int(r['position']) for r in race['results'] 
                                  if r['driver_id'] == driver_id)
                    
                    # Convert position to podium indicator (1 for podium, 0 otherwise)
                    podium = 1 if position <= 3 else 0
                    
                    X.append(features)
                    y.append(podium)
        
        # Convert to DataFrame
        X_df = pd.DataFrame(X)
        
        # Scale numerical features
        numerical_features = ['avg_position', 'win_rate', 'podium_rate', 
                            'circuit_avg_position', 'circuit_podium_rate',
                            'recent_avg_position', 'recent_podium_rate',
                            'avg_qualifying_position', 'team_avg_position', 
                            'team_podium_rate']
        
        X_df[numerical_features] = self.scaler.fit_transform(X_df[numerical_features])
        
        return X_df, np.array(y)
    
    def prepare_prediction_data(self, year, round):
        """Prepare data for making predictions"""
        race = self.db.races.find_one({'year': year, 'round': round})
        if not race:
            raise ValueError(f"Race not found for year {year} and round {round}")
        
        X = []
        driver_ids = []
        
        # Get all drivers in the race
        drivers = [r['driver_id'] for r in race['results']]
        
        # Prepare features for each driver
        for driver_id in drivers:
            features = self.get_driver_features(driver_id, year, round)
            
            # Add encoded categorical features
            features['driver_encoded'] = self.driver_encoder.transform([driver_id])[0]
            features['circuit_encoded'] = self.circuit_encoder.transform([race['circuit']])[0]
            
            X.append(features)
            driver_ids.append(driver_id)
        
        # Convert to DataFrame
        X_df = pd.DataFrame(X)
        
        # Scale numerical features
        numerical_features = ['avg_position', 'win_rate', 'podium_rate', 
                            'circuit_avg_position', 'circuit_podium_rate',
                            'recent_avg_position', 'recent_podium_rate',
                            'avg_qualifying_position', 'team_avg_position', 
                            'team_podium_rate']
        
        X_df[numerical_features] = self.scaler.transform(X_df[numerical_features])
        
        return X_df, driver_ids 