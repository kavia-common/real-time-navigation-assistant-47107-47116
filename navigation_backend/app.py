import os
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

# PUBLIC_INTERFACE
def create_app():
    """
    This is the Flask application factory.

    Returns:
        Flask: Configured Flask application with REST endpoints for routes, history, and user.
    """
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    # Allow frontend calls
    cors_origins = os.getenv("FRONTEND_ORIGIN", "*")
    CORS(app, resources={r"/api/*": {"origins": cors_origins}})

    # In-memory storage for demo purposes
    app.state = {
        "history": [],
        "user": {
            "id": "demo-user",
            "name": "Ocean Navigator",
            "email": "ocean.navigator@example.com",
            "preferences": {"units": "metric"},
        },
    }

    @app.get("/api/health")
    def health():
        """
        Health check endpoint.

        Returns:
            application/json: {"status": "ok"}
        """
        return jsonify({"status": "ok"})

    @app.get("/api/user")
    def get_user():
        """
        Get current user profile.

        Returns:
            application/json: user profile object
        """
        return jsonify(app.state["user"])

    @app.post("/api/user")
    def update_user():
        """
        Update basic user profile fields.

        Body:
            application/json: Partial user object with fields to update.

        Returns:
            application/json: Updated user profile
        """
        data = request.get_json(silent=True) or {}
        app.state["user"].update({k: v for k, v in data.items() if k in {"name", "email", "preferences"}})
        return jsonify(app.state["user"])

    @app.get("/api/history")
    def get_history():
        """
        Get recent route queries.

        Returns:
            application/json: { items: [ ... ] }
        """
        return jsonify({"items": app.state["history"][-25:][::-1]})

    @app.post("/api/routes")
    def compute_route():
        """
        Compute a route between origin and destination.
        This is a stub that echoes inputs and returns a mock polyline and steps.
        Integrate with real Directions API in future.

        Body:
            application/json:
                origin: string (required)
                destination: string (required)
                waypoints: list[string] (optional)

        Returns:
            application/json:
                polyline: string
                distanceText: string
                durationText: string
                steps: list[ { instruction, distanceText, durationText } ]
        """
        data = request.get_json(silent=True) or {}
        origin = data.get("origin")
        destination = data.get("destination")
        waypoints = data.get("waypoints", [])

        if not origin or not destination:
            return jsonify({"error": "origin and destination are required"}), 400

        # Mock response shape aligned with contract
        mock = {
            "polyline": "mock_polyline_string_for_demo_only",
            "distanceText": "5.2 km",
            "durationText": "13 mins",
            "steps": [
                {"instruction": f"Start at {origin}", "distanceText": "0.5 km", "durationText": "2 mins"},
                {"instruction": "Head north", "distanceText": "2.0 km", "durationText": "5 mins"},
                {"instruction": "Turn right onto Ocean Ave", "distanceText": "1.5 km", "durationText": "4 mins"},
                {"instruction": f"Arrive at {destination}", "distanceText": "1.2 km", "durationText": "2 mins"},
            ],
            "waypoints": waypoints,
        }

        # Append to in-memory history
        app.state["history"].append(
            {
                "id": f"hist_{len(app.state['history'])+1}",
                "origin": origin,
                "destination": destination,
                "waypoints": waypoints,
                "createdAt": datetime.utcnow().isoformat() + "Z",
                "summary": {"distanceText": mock["distanceText"], "durationText": mock["durationText"]},
            }
        )

        return jsonify(mock)

    # Simple OpenAPI-style metadata endpoint for discoverability
    @app.get("/docs")
    def docs():
        """
        API documentation pointer.

        Returns:
            application/json: basic metadata and endpoints
        """
        return jsonify(
            {
                "title": "Navigation Backend API",
                "version": "v1",
                "endpoints": {
                    "health": "/api/health",
                    "routes": "/api/routes",
                    "history": "/api/history",
                    "user_get": "/api/user",
                    "user_post": "/api/user",
                },
            }
        )

    return app


if __name__ == "__main__":
    # Allow port override via env
    port = int(os.getenv("PORT", "3001"))
    app = create_app()
    app.run(host="0.0.0.0", port=port)
