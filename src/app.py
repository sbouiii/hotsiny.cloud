from flask import Flask
from flask_cors import CORS
from src.config import Config
from src.routes.messages import messages_bp
from src.services.database import init_mongo

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Configure CORS
    CORS(app, resources={r"/api/*": {"origins": app.config['ALLOWED_ORIGIN']}})

    # Initialize MongoDB
    init_mongo(app)

    # Register blueprints (routes)
    app.register_blueprint(messages_bp, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)