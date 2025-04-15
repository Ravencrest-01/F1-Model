import os
import json
import requests
import pandas as pd
import fastf1
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DataAcquisition:
    def __init__(self):
        self.ergast_base_url = os.getenv('ERGAST_API_BASE_URL')
        self.cache_dir = os.getenv('FASTF1_CACHE_DIR')
        
        # Set up FastF1 cache
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        fastf1.Cache.enable_cache(self.cache_dir)

    def get_historical_data(self, start_year=2000, end_year=2024):
        """Fetch historical race data from Ergast API"""
        all_races = []
        
        for year in range(start_year, end_year + 1):
            url = f"{self.ergast_base_url}/{year}/results.json?limit=1000"
            response = requests.get(url)
            data = response.json()
            
            if 'MRData' in data and 'RaceTable' in data['MRData']:
                races = data['MRData']['RaceTable']['Races']
                all_races.extend(races)
                
        return all_races

    def get_recent_telemetry(self, year=2023):
        """Fetch recent telemetry data using FastF1"""
        schedule = fastf1.get_event_schedule(year)
        telemetry_data = []
        
        for event in schedule.itertuples():
            try:
                session = fastf1.get_session(year, event.RoundNumber, 'R')
                session.load()
                
                # Get lap times and telemetry
                laps = session.laps
                weather = session.weather_data
                
                # Get driver info
                drivers = session.drivers
                
                telemetry_data.append({
                    'event': event.EventName,
                    'round': event.RoundNumber,
                    'laps': laps,
                    'weather': weather,
                    'drivers': drivers
                })
                
            except Exception as e:
                print(f"Error fetching data for {event.EventName}: {str(e)}")
                
        return telemetry_data

    def process_historical_data(self, races):
        """Process historical race data into a structured format"""
        processed_data = []
        
        for race in races:
            race_data = {
                'year': race['season'],
                'round': race['round'],
                'circuit': race['Circuit']['circuitName'],
                'date': race['date'],
                'results': []
            }
            
            for result in race['Results']:
                driver = result['Driver']
                constructor = result['Constructor']
                
                race_data['results'].append({
                    'position': result['position'],
                    'driver_id': driver['driverId'],
                    'driver_name': f"{driver['givenName']} {driver['familyName']}",
                    'constructor_id': constructor['constructorId'],
                    'constructor_name': constructor['name'],
                    'grid': result['grid'],
                    'laps': result['laps'],
                    'status': result['status'],
                    'points': result['points']
                })
                
            processed_data.append(race_data)
            
        return processed_data

    def process_telemetry_data(self, telemetry_data):
        """Process telemetry data into a structured format"""
        processed_data = []
        
        for event in telemetry_data:
            event_data = {
                'event': event['event'],
                'round': event['round'],
                'laps': [],
                'weather': event['weather'].to_dict() if event['weather'] is not None else None,
                'drivers': event['drivers']
            }
            
            if event['laps'] is not None:
                event_data['laps'] = event['laps'].to_dict()
                
            processed_data.append(event_data)
            
        return processed_data

    def save_to_json(self, data, filename):
        """Save data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_from_json(self, filename):
        """Load data from JSON file"""
        with open(filename, 'r') as f:
            return json.load(f)

if __name__ == "__main__":
    # Example usage
    da = DataAcquisition()
    
    # Fetch historical data
    print("Fetching historical data...")
    historical_data = da.get_historical_data()
    processed_historical = da.process_historical_data(historical_data)
    da.save_to_json(processed_historical, 'historical_data.json')
    
    # Fetch recent telemetry
    print("Fetching recent telemetry data...")
    telemetry_data = da.get_recent_telemetry()
    processed_telemetry = da.process_telemetry_data(telemetry_data)
    da.save_to_json(processed_telemetry, 'telemetry_data.json') 