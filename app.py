from flask import Flask, render_template

from config import Config
from extensions import db

# Blueprints
from routes.volunteer_routes import volunteer_bp
from routes.admin_routes import admin_bp
from routes.beneficiary_routes import beneficiary_bp

# Models
from models.beneficiary import Beneficiary
from models.distribution import Distribution
from models.admin import Admin


def create_app():

    app = Flask(__name__)

    # Secret Key
    app.secret_key = "genesis-secret-key"

    # Configuration
    app.config.from_object(Config)

    # Database
    db.init_app(app)

    # Blueprints
    app.register_blueprint(volunteer_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(beneficiary_bp)

    # Create Tables
    with app.app_context():
        db.create_all()

    # Home Page
    @app.route("/")
    def home():
        return render_template("home.html")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)