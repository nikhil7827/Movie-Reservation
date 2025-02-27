from SQLAlchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'admin' or 'user'

# Movie Model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    poster_url = db.Column(db.String(255), nullable=True)
    showtimes = db.relationship('Showtime', backref='movie', lazy=True)

# Showtime Model
class Showtime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    reservations = db.relationship('Reservation', backref='showtime', lazy=True)

# Reservation Model
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtime.id'), nullable=False)
    seat_number = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='reserved')  # reserved, canceled
