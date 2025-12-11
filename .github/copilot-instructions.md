## Quick overview

- Project: NeuroLogistics — a small Flask web UI that requests driving routes from the public OSRM API and uses a trained ML model to predict traffic delay and adjust travel time.
- Entry point: `app.py` (Flask). Frontend: `templates/index.html` (Leaflet.js + OpenStreetMap).
- ML pipeline: `generate_synthetic_data.py` -> `train_model.py` -> produces `delay_prediction_model.pkl` (loaded by `app.py`). Data file: `synthetic_traffic_data.csv`.

## What an AI assistant should know first

- The web app calls OSRM via: `http://router.project-osrm.org/route/v1/driving/{lng1},{lat1};{lng2},{lat2}` and then swaps coordinates to [lat, lng] for Leaflet (see `app.py` route building and coordinate transform).
- The ML model is loaded with `joblib.load('delay_prediction_model.pkl')` in `app.py`. If this file is missing, run the training pipeline (below).
- Important mismatch / gotcha to notice: `train_model.py` trains on features including `road_type` (it maps `road_type` to numeric values), but `app.py` currently prepares input DataFrame with only these columns: `['start_time','route_distance','day_of_week','avg_speed']` (no `road_type`). Investigate the model's expected feature shape before editing inference code — either add `road_type` to the web form / inference pipeline or retrain the model without that column.

## Common developer workflows (concrete commands)

1. Create venv and install deps (README lists primary libs):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt   # or: pip install Flask requests folium
```

2. Regenerate synthetic data and retrain model (safe development flow):

```bash
python generate_synthetic_data.py   # creates synthetic_traffic_data.csv
python train_model.py               # trains and writes delay_prediction_model.pkl
```

3. Run the web app (dev):

```bash
python app.py   # runs Flask app with debug=True
```

## Project-specific patterns & conventions

- Time encoding: `generate_synthetic_data.py` writes `start_time` as `HH:MM` strings; `train_model.py` converts them to numeric hours via `time_to_numeric` before training. If you change the input format, update both training and inference conversions.
- Road-type handling: `generate_synthetic_data.py` includes `road_type` and `train_model.py` maps it to numeric factors (`{'highway':1,'city':0.8,'rural':1.0}`) — this affects `avg_speed`/travel time calculations.
- Vehicle-type adjustments: `app.py` mutates `avg_speed` for `truck` and `bike` in a small ad-hoc way (multipliers 0.7 and 0.5). If you modify vehicle handling, update both frontend form and server-side logic.
- OSRM responses are printed in `app.py` (debugging aid): `print("OSRM API Response:", response.json())` — useful when troubleshooting route failures.

## Key files to inspect for changes

- `app.py` — Flask routes, OSRM integration, model inference, prediction explanation text.
- `templates/index.html` — Leaflet rendering, map click handlers that populate the form; uses `route_points` from Flask templates.
- `generate_synthetic_data.py` — how synthetic samples are formed (rush-hour logic, road_type sampling).
- `train_model.py` — feature pipeline, model type (RandomForestRegressor), and saved artifact name.
- `synthetic_traffic_data.csv` — sample data format used by training and inference.

## Integration & external dependencies

- External routing: public OSRM endpoint (router.project-osrm.org). May be rate-limited or return unexpected payloads — consider running a local OSRM instance for high-volume testing.
- Model persistence: `joblib` pickles in project root. Make sure model and training code agree on feature names and ordering.

## Debugging tips specific to this repo

- If route rendering fails, check console output (the app prints the OSRM JSON). Confirm `routes` exists and `geometry.coordinates` are present.
- If model.predict raises a shape error, verify `delay_prediction_model.pkl` feature names/order (use `sklearn` utilities or inspect the original training script). Likely root cause: missing `road_type` column at inference.
- If web form values aren't updating map markers, inspect `templates/index.html` click handler which writes to `<input>` fields.

## Minimal edit checklist for common tasks

- Add a new input (e.g., `road_type`) to the UI: update `templates/index.html` form, update `app.py` to read form value into `input_data`, and ensure it's in the same order the model expects.
- Change model features: update `train_model.py` and re-run training; commit `delay_prediction_model.pkl` or add instructions to reproduce it.

## When in doubt

- Reproduce the error locally: run `generate_synthetic_data.py`, `train_model.py`, then `app.py` to create a clean, reproducible environment.
- Look at the small, explicit helper functions in the repo (time conversion and road type simulation) as canonical implementations for feature engineering.

---

If you'd like, I can (1) open a PR that (a) adds `road_type` to the web form and inference or (b) retrains the model without `road_type`; or (2) expand this guidance into a more detailed AGENT.md with troubleshooting scripts. Which would you prefer? 
