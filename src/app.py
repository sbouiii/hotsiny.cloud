from flask import Flask
from src.routes.messages import messages_bp
from src.routes.plans import plans_bp  # Import the plans blueprint
from src.services.database import init_mongo

def create_app():
    app = Flask(__name__)

    # Initialize MongoDB
    init_mongo(app)

    # Register blueprints (routes)
    app.register_blueprint(messages_bp, url_prefix='/api')
    app.register_blueprint(plans_bp, url_prefix='/api')  # Register plans blueprint

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)