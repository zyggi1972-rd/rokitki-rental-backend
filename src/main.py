import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.property import property_bp
from src.routes.payment import payment_bp

# Import all models to ensure they're registered with SQLAlchemy
from src.models.property import Property, PropertyImage
from src.models.booking import Booking, Availability
from src.models.payment import Payment, ListingPlan

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app, supports_credentials=True)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(property_bp, url_prefix='/api')
app.register_blueprint(payment_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create tables and seed data
with app.app_context():
    db.create_all()
    
    # Seed listing plans if they don't exist
    if not ListingPlan.query.first():
        plans = [
            ListingPlan(
                name="Plan Podstawowy",
                price=29.0,
                duration_days=30,
                is_featured=False,
                max_images=5,
                description="Standardowe ogłoszenie na 30 dni"
            ),
            ListingPlan(
                name="Plan Premium",
                price=49.0,
                duration_days=30,
                is_featured=True,
                max_images=15,
                description="Wyróżnione ogłoszenie na 30 dni z większą liczbą zdjęć"
            ),
            ListingPlan(
                name="Plan Sezonowy",
                price=99.0,
                duration_days=90,
                is_featured=True,
                max_images=20,
                description="Wyróżnione ogłoszenie na cały sezon (90 dni)"
            )
        ]
        
        for plan in plans:
            db.session.add(plan)
        
        db.session.commit()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
