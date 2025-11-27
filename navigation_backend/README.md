# Navigation Backend (Flask)

Simple Flask API providing endpoints for demo navigation app.

## Endpoints
- GET /api/health
- GET /api/user
- POST /api/user
- GET /api/history
- POST /api/routes

## Run
pip install -r requirements.txt
export PORT=3001
python app.py

## Environment
- FRONTEND_ORIGIN: CORS allow-list (default "*")
