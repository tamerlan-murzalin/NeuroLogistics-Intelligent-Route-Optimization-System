from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    start = {"lat": 47.4979, "lng": 19.0402}  # Budapest
    end = {"lat": 46.2530, "lng": 20.1414}    # Szeged

    if request.method == 'POST':
        start = {"lat": float(request.form['start_lat']), "lng": float(request.form['start_lng'])}
        end = {"lat": float(request.form['end_lat']), "lng": float(request.form['end_lng'])}

    # Запрос маршрута к OSRM
    url = f"http://router.project-osrm.org/route/v1/driving/{start['lng']},{start['lat']};{end['lng']},{end['lat']}?overview=full&geometries=geojson"
    response = requests.get(url).json()
    route_points = response['routes'][0]['geometry']['coordinates']
    # меняем местами координаты для Leaflet [lat, lon]
    route_points = [[p[1], p[0]] for p in route_points]

    return render_template("index.html", route_points=route_points)

if __name__ == '__main__':
    app.run(debug=True)