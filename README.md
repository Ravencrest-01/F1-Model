# F1 Podium Predictor

A machine learning model and web application for predicting Formula 1 race podium finishers.

## Project Overview

This project combines historical F1 data (2000-2024) from the Ergast API with recent telemetry data (2023-2025) from FastF1 to predict podium finishers for upcoming Grand Prix races. The system includes:

- Machine learning model for podium predictions
- Web application for viewing historical data and predictions
- MongoDB database for data storage
- RESTful API for data access

## Features

### Machine Learning Model
- Predicts top 3 finishers for upcoming races
- Considers driver performance history, track-specific performance, recent form, and team performance
- Uses neural networks for prediction

### Web Application
- View historical race data
- View detailed driver statistics
- View upcoming race information
- Display circuit maps and race details

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Create a `.env` file
   - Add your MongoDB Atlas connection string
   - Add any API keys if needed

5. Initialize the database:
   ```bash
   python scripts/init_db.py
   ```

6. Run the web application:
   ```bash
   python app.py
   ```

## Project Structure

```
f1-model/
├── app/                    # Web application
│   ├── static/            # Static files (CSS, JS, images)
│   ├── templates/         # HTML templates
│   └── routes/            # Flask routes
├── ml/                    # Machine learning code
│   ├── data/             # Data processing scripts
│   ├── models/           # ML model definitions
│   └── training/         # Training scripts
├── scripts/              # Utility scripts
├── tests/               # Test files
├── .env                 # Environment variables
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## Data Sources

- Historical Data (2000-2024): Ergast API
- Recent Data (2023-2025): FastF1 library
- Circuit Maps: F1 official website
- Additional Driver Information: Ergast API

## Contributing

Feel free to submit issues and enhancement requests! 