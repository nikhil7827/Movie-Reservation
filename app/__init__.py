import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions globally (but without an app yet)
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


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
    migrate.init_app(app, db)  # Initialize migrate with app and db
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

    return app


def seed_initial_data():
    from app.models.user import User
    from app import db
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Seeded initial admin user.")

if __name__ == '__main__':
    app = create_app()
    if app:
        with app.app_context():
            seed_initial_data()
        app.run(debug=True)
    else:
        print("Failed to create Flask app. Exiting.")


# If you want to run the app directly
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_initial_data()  # Seed data after app context is set
    app.run(debug=True)
