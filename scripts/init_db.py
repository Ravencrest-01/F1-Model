import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_database():
    # Connect to MongoDB Atlas
    client = MongoClient(os.getenv('MONGODB_URI'))
    db = client.f1_predictor
    
    # Create collections with validation schemas
    collections = {
        'races': {
            'validator': {
                '$jsonSchema': {
                    'bsonType': 'object',
                    'required': ['year', 'round', 'circuit', 'date', 'results'],
                    'properties': {
                        'year': {'bsonType': 'int'},
                        'round': {'bsonType': 'int'},
                        'circuit': {'bsonType': 'string'},
                        'date': {'bsonType': 'string'},
                        'results': {
                            'bsonType': 'array',
                            'items': {
                                'bsonType': 'object',
                                'required': ['position', 'driver_id', 'driver_name', 'constructor_id', 'constructor_name'],
                                'properties': {
                                    'position': {'bsonType': 'string'},
                                    'driver_id': {'bsonType': 'string'},
                                    'driver_name': {'bsonType': 'string'},
                                    'constructor_id': {'bsonType': 'string'},
                                    'constructor_name': {'bsonType': 'string'},
                                    'grid': {'bsonType': 'string'},
                                    'laps': {'bsonType': 'string'},
                                    'status': {'bsonType': 'string'},
                                    'points': {'bsonType': 'string'}
                                }
                            }
                        }
                    }
                }
            }
        },
        'drivers': {
            'validator': {
                '$jsonSchema': {
                    'bsonType': 'object',
                    'required': ['driver_id', 'name', 'nationality', 'date_of_birth'],
                    'properties': {
                        'driver_id': {'bsonType': 'string'},
                        'name': {'bsonType': 'string'},
                        'nationality': {'bsonType': 'string'},
                        'date_of_birth': {'bsonType': 'string'},
                        'teams': {
                            'bsonType': 'array',
                            'items': {
                                'bsonType': 'object',
                                'required': ['constructor_id', 'constructor_name', 'year'],
                                'properties': {
                                    'constructor_id': {'bsonType': 'string'},
                                    'constructor_name': {'bsonType': 'string'},
                                    'year': {'bsonType': 'int'}
                                }
                            }
                        },
                        'championships': {'bsonType': 'int'},
                        'wins': {'bsonType': 'int'},
                        'podiums': {'bsonType': 'int'}
                    }
                }
            }
        },
        'circuits': {
            'validator': {
                '$jsonSchema': {
                    'bsonType': 'object',
                    'required': ['circuit_id', 'name', 'location', 'country'],
                    'properties': {
                        'circuit_id': {'bsonType': 'string'},
                        'name': {'bsonType': 'string'},
                        'location': {'bsonType': 'string'},
                        'country': {'bsonType': 'string'},
                        'map_url': {'bsonType': 'string'},
                        'first_grand_prix': {'bsonType': 'int'}
                    }
                }
            }
        },
        'telemetry': {
            'validator': {
                '$jsonSchema': {
                    'bsonType': 'object',
                    'required': ['year', 'round', 'event'],
                    'properties': {
                        'year': {'bsonType': 'int'},
                        'round': {'bsonType': 'int'},
                        'event': {'bsonType': 'string'},
                        'laps': {'bsonType': 'object'},
                        'weather': {'bsonType': 'object'},
                        'drivers': {'bsonType': 'array'}
                    }
                }
            }
        }
    }
    
    # Create collections with validation
    for collection_name, schema in collections.items():
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            db.command({
                'collMod': collection_name,
                'validator': schema['validator']
            })
            print(f"Created collection {collection_name} with validation schema")
        else:
            print(f"Collection {collection_name} already exists")
    
    # Create indexes
    db.races.create_index([('year', 1), ('round', 1)])
    db.drivers.create_index('driver_id')
    db.circuits.create_index('circuit_id')
    db.telemetry.create_index([('year', 1), ('round', 1)])
    
    print("Database initialization complete!")

if __name__ == "__main__":
    init_database() 