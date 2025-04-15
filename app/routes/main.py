from flask import Blueprint, render_template, jsonify
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/races/<int:year>/<int:round>')
def race_details(year, round):
    race = bp.db.races.find_one({'year': year, 'round': round})
    if not race:
        return render_template('error.html', message='Race not found'), 404
    return render_template('race_details.html', race=race)

@bp.route('/drivers/<driver_id>')
def driver_details(driver_id):
    driver = bp.db.drivers.find_one({'driver_id': driver_id})
    if not driver:
        return render_template('error.html', message='Driver not found'), 404
    
    # Calculate age
    dob = datetime.strptime(driver['date_of_birth'], '%Y-%m-%d')
    age = (datetime(2025, 4, 15) - dob).days // 365
    
    # Get recent races
    recent_races = list(bp.db.races.find(
        {'results.driver_id': driver_id},
        {'year': 1, 'round': 1, 'circuit': 1, 'results.$': 1}
    ).sort([('year', -1), ('round', -1)]).limit(5))
    
    return render_template('driver_details.html',
                         driver=driver,
                         age=age,
                         recent_races=recent_races)

@bp.route('/upcoming')
def upcoming_race():
    # Get the next race based on current date
    current_date = datetime(2025, 4, 15)  # Using the specified date
    next_race = bp.db.races.find_one(
        {'date': {'$gt': current_date.strftime('%Y-%m-%d')}},
        sort=[('date', 1)]
    )
    
    if not next_race:
        return render_template('error.html', message='No upcoming races found'), 404
    
    # Get circuit details
    circuit = bp.db.circuits.find_one({'name': next_race['circuit']})
    
    return render_template('upcoming_race.html',
                         race=next_race,
                         circuit=circuit) 