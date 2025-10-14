# NeuroLogistics – Intelligent Route Optimization System

NeuroLogistics is a web-based logistics assistant built with **Flask** and **Leaflet.js**.  
It allows users to enter start and end coordinates and displays an optimized road route using the public **OSRM API** (Open Source Routing Machine).

## 🚀 Features
- ✅ Flask backend with dynamic route rendering  
- ✅ Integration with OSRM for real driving routes  
- ✅ Interactive map using Leaflet.js + OpenStreetMap  
- ✅ Input form for custom coordinates  
- ✅ Markers and auto-zoom on the route

## 📂 Tech Stack
- **Backend:** Python (Flask)  
- **Frontend:** HTML, CSS, JavaScript  
- **Maps:** Leaflet.js + OpenStreetMap  
- **Routing API:** OSRM (public endpoint)

## ▶️ How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/your-username/NeuroLogistics.git
cd NeuroLogistics

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# OR on Windows: venv\Scripts\activate

# 3. Install dependencies
pip install flask requests folium

# 4. Run the app
python app.py
