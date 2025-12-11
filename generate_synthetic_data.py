import pandas as pd
import random
import numpy as np
from datetime import datetime, timedelta

# Function to generate random times between 6 AM and 9 PM
def generate_random_time():
    base_time = datetime.strptime('06:00', '%H:%M')
    random_minutes = random.randint(0, 900)  # Random minutes between 0 and 15 hours (900 minutes)
    return (base_time + timedelta(minutes=random_minutes)).strftime('%H:%M')

# Function to simulate traffic conditions based on the day and start time
def simulate_traffic(day_of_week, start_time):
    # Assume that traffic is lighter in the morning (8-9 AM) and heavier in the afternoon (4-6 PM)
    hour = int(start_time.split(':')[0])
    if 8 <= hour < 9 or 16 <= hour < 18:
        traffic_factor = random.uniform(1.2, 1.5)  # Increased traffic during rush hours
    else:
        traffic_factor = random.uniform(1.0, 1.2)  # Lighter traffic during non-rush hours
    return traffic_factor

# Function to simulate road type impact on speed
def simulate_road_type():
    road_types = ['highway', 'city', 'rural']
    road_type = random.choice(road_types)
    
    if road_type == 'highway':
        speed_factor = 1.2  # Higher speed on highways
    elif road_type == 'city':
        speed_factor = 0.8  # Lower speed in the city
    else:
        speed_factor = 1.0  # Normal speed on rural roads
    
    return road_type, speed_factor

# Generate synthetic data
def generate_data(num_samples):
    data = []
    
    for _ in range(num_samples):
        start_time = generate_random_time()  # Generate random start time
        route_distance = random.randint(5, 50)  # Random route distance (5 km to 50 km)
        day_of_week = random.randint(1, 7)  # Random day of the week (1 = Monday, 7 = Sunday)
        avg_speed = random.randint(30, 60)  # Random speed (30 km/h to 60 km/h)

        # Simulate traffic factor based on time of day and day of the week
        traffic_factor = simulate_traffic(day_of_week, start_time)
        
        # Simulate road type and its effect on speed
        road_type, road_speed_factor = simulate_road_type()
        adjusted_speed = avg_speed * road_speed_factor

        # Calculate travel time (in minutes) based on distance, speed, and traffic factor
        travel_time = (route_distance / adjusted_speed) * 60 * traffic_factor  # Convert hours to minutes

        data.append({
            'start_time': start_time,
            'route_distance': route_distance,
            'day_of_week': day_of_week,
            'avg_speed': avg_speed,
            'road_type': road_type,
            'travel_time': round(travel_time, 2)  # Rounded to 2 decimal places
        })
    
    # Convert to a pandas DataFrame
    df = pd.DataFrame(data)
    return df

# Generate 1000 samples of synthetic data
synthetic_data = generate_data(1000)

# Save the data to a CSV file
synthetic_data.to_csv('synthetic_traffic_data.csv', index=False)

# Show the first few rows of the generated data
print(synthetic_data.head())