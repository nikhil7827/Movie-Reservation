import os
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    try:
        app = Flask(__name__)

        load_dotenv()
        secret_key = os.getenv('SECRET_KEY')
        if not secret_key:
            raise ValueError("SECRET_KEY not found in environment variables.")
        app.config['SECRET_KEY'] = secret_key

        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_name = os.getenv('DB_NAME')
        if not all([db_user, db_password, db_host, db_name]):
            raise ValueError("Database configuration missing in environment variables.")
        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db.init_app(app)
        login_manager.init_app(app)
        migrate.init_app(app, db)
        login_manager.login_view = 'auth.user_login'  # Updated to match new endpoint

        from app.models.user import User
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # Defer blueprint registration
        with app.app_context():
            from app.routes import auth, movie, reservation
            print("Registering blueprints...")
            app.register_blueprint(auth.bp)
            app.register_blueprint(movie.bp)
            app.register_blueprint(reservation.bp, url_prefix='/reservations')

            from app.models.movie import Movie
            from app.models.user import User

            print("Registered endpoints:", [rule.endpoint for rule in app.url_map.iter_rules()])
            print("Flask app successfully initialized.")
        return app

    except Exception as e:
        print(f"Error in create_app(): {str(e)}")
        return None

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
