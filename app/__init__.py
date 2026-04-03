from flask import Flask
from flask_cors import CORS
from app.routes.order_routes import order_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "super_secret_key"

    # Enable CORS for all routes
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Register blueprints AFTER enabling CORS
    app.register_blueprint(order_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)