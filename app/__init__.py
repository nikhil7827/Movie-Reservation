from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Initialize extensions globally (but without an app yet)
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # Create the Flask app instance
    app = Flask(__name__)

    # Load environment variables
    load_dotenv()
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Define user loader for Flask-Login
    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register blueprints
    from app.routes import auth, movie, reservation
    app.register_blueprint(auth.bp)
    app.register_blueprint(movie.bp)
    app.register_blueprint(reservation.bp, url_prefix='/reservations')

    # Create database tables and seed initial data
    with app.app_context():
        db.create_all()
        seed_initial_data()

    return app

def seed_initial_data():
    from app.models.user import User
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('admin123')  # Change this in production
        db.session.add(admin)
        db.session.commit()