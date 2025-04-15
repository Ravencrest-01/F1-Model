from flask import Blueprint, jsonify
from datetime import datetime

bp = Blueprint('api', __name__)

@bp.route('/races/<int:year>/<int:round>')
def get_race(year, round):
    race = bp.db.races.find_one({'year': year, 'round': round})
    if not race:
        return jsonify({'error': 'Race not found'}), 404
    return jsonify(race)

@bp.route('/drivers/<driver_id>')
def get_driver(driver_id):
    driver = bp.db.drivers.find_one({'driver_id': driver_id})
    if not driver:
        return jsonify({'error': 'Driver not found'}), 404
    
    # Calculate age
    dob = datetime.strptime(driver['date_of_birth'], '%Y-%m-%d')
    age = (datetime(2025, 4, 15) - dob).days // 365
    
    # Get recent races
    recent_races = list(bp.db.races.find(
        {'results.driver_id': driver_id},
        {'year': 1, 'round': 1, 'circuit': 1, 'results.$': 1}
    ).sort([('year', -1), ('round', -1)]).limit(5))
    
    response = {
        'driver': driver,
        'age': age,
        'recent_races': recent_races
    }
    
    return jsonify(response)

@bp.route('/upcoming')
def get_upcoming_race():
    current_date = datetime(2025, 4, 15)  # Using the specified date
    next_race = bp.db.races.find_one(
        {'date': {'$gt': current_date.strftime('%Y-%m-%d')}},
        sort=[('date', 1)]
    )
    
    if not next_race:
        return jsonify({'error': 'No upcoming races found'}), 404
    
    circuit = bp.db.circuits.find_one({'name': next_race['circuit']})
    
    response = {
        'race': next_race,
        'circuit': circuit
    }
    
    return jsonify(response)

@bp.route('/predictions/<int:year>/<int:round>')
def get_predictions(year, round):
    # This endpoint will be implemented once we have the ML model
    return jsonify({'error': 'Predictions not yet available'}), 501 