import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# Load the synthetic traffic data
df = pd.read_csv('synthetic_traffic_data.csv')

# Convert 'start_time' to hours (numeric)
def time_to_numeric(time_str):
    hour, minute = map(int, time_str.split(':'))
    return hour + minute / 60

df['start_time'] = df['start_time'].apply(time_to_numeric)

# Convert categorical 'road_type' to numerical values
df['road_type'] = df['road_type'].map({'highway': 1, 'city': 0.8, 'rural': 1.0})

# Prepare features (X) and target variable (y)
X = df[['start_time', 'route_distance', 'day_of_week', 'avg_speed', 'road_type']]
y = df['travel_time']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Save the trained model
joblib.dump(model, 'delay_prediction_model.pkl')