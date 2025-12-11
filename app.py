from flask import Flask, render_template, request
import requests
import joblib
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Load the trained ML model for delay prediction
model = joblib.load('delay_prediction_model.pkl')

@app.route('/', methods=['GET', 'POST'])
def index():
    # Default start and end coordinates (Budapest and Szeged)
    start = {"lat": 47.4979, "lng": 19.0402}  # Budapest
    end = {"lat": 46.2530, "lng": 20.1414}    # Szeged
    start_time = 8  # Default start time in HH:MM format
    date = None  # Default date is None
    vehicle_type = "car"  # Default vehicle type
    avg_speed = 50  # Default average speed (km/h)

    # Initialize route_distance and base_travel_time to avoid errors
    route_distance = 0
    base_travel_time = 0
    route_points = []
    day_of_week = 1  # Default to Monday if no date is selected

    # If the form is submitted (POST method)
    if request.method == 'POST':
        # Get the coordinates entered by the user
        start = {"lat": float(request.form.get('start_lat', 47.4979)), "lng": float(request.form.get('start_lng', 19.0402))}
        end = {"lat": float(request.form.get('end_lat', 46.2530)), "lng": float(request.form.get('end_lng', 20.1414))}
        
        # Get the start time (HH:MM format) as a string
        start_time_str = request.form.get('start_time', '08:00')
        
        # Convert the start time string 'HH:MM' into decimal hours
        start_time_hour = int(start_time_str.split(":")[0])  # Get the hour part
        start_time_minute = int(start_time_str.split(":")[1])  # Get the minute part
        start_time = start_time_hour + (start_time_minute / 60)  # Convert to decimal hours

        # Get the selected date and convert it to a day of the week
        date_str = request.form.get('date', None)
        if date_str:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            day_of_week = date.weekday() + 1  # Python's weekday: Monday=0, Sunday=6, so we add 1
        else:
            day_of_week = 1  # Default to Monday if no date is selected

        vehicle_type = request.form.get('vehicle_type', 'car')  # Vehicle type
        avg_speed = float(request.form.get('avg_speed', 50))  # Average speed (can be adjusted)

    # Request route from OpenRouteService API with error handling
    try:
        # Update this URL with your correct API key
        api_key = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImE1YTNhMzliODg0ZDQ4NzBiYzgwMDU1NTkxYjNlNmIwIiwiaCI6Im11cm11cjY0In0="  # Replace with your actual API key
        url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={start['lng']},{start['lat']}&end={end['lng']},{end['lat']}"
        
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful (status code 200)
        
        route_data = response.json()  # Parse the JSON response
        
        if 'features' in route_data and len(route_data['features']) > 0:
            route_points = route_data['features'][0]['geometry']['coordinates']
            route_points = [[p[1], p[0]] for p in route_points]  # Swap lat/lng for Leaflet

            # Calculate the route distance
            route_distance = route_data['features'][0]['properties']['segments'][0]['distance'] / 1000  # Convert meters to kilometers
            base_travel_time = (route_distance / avg_speed) * 60  # in minutes
        else:
            raise ValueError("Invalid response: No route data found")

    except requests.exceptions.RequestException as e:
        print(f"Error with the API request: {e}")
        route_points = []  # No route data
    except ValueError as e:
        print(f"Error parsing the JSON response or no route data: {e}")
        route_points = []  # No route data

    # Adjust average speed based on vehicle type
    if vehicle_type == "truck":
        avg_speed *= 0.7  # Trucks are slower, reduce speed
    elif vehicle_type == "bike":
        avg_speed *= 0.5  # Bikes are slower, further reduce speed

    # Prepare the input for the model (convert to a DataFrame)
    input_data = pd.DataFrame([[start_time, route_distance, day_of_week, avg_speed]], 
                              columns=['start_time', 'route_distance', 'day_of_week', 'avg_speed'])

    # Predict delay using the trained ML model
    delay_pred = model.predict(input_data)[0]
    adjusted_time = base_travel_time + delay_pred  # Adjusted time with predicted delay

    # Convert adjusted time to a more readable format (days, hours, minutes)
    days = adjusted_time // (24 * 60)  # Days
    hours = (adjusted_time % (24 * 60)) // 60  # Hours
    minutes = adjusted_time % 60  # Minutes

    explanation = f"The model predicts a {round(delay_pred, 2)} minute delay due to traffic conditions on a {['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][day_of_week-1]}."

    return render_template("index.html", 
                           route_points=route_points, 
                           adjusted_time=f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes", 
                           base_travel_time=round(base_travel_time, 2),
                           explanation=explanation,
                           start_lat=start['lat'], start_lng=start['lng'],
                           end_lat=end['lat'], end_lng=end['lng'],
                           start_time=start_time, day_of_week=day_of_week,
                           vehicle_type=vehicle_type, avg_speed=avg_speed, date=date)

if __name__ == '__main__':
    app.run(debug=True)