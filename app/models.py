from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    bookings = db.relationship('Booking', backref='customer', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer)  # in minutes
    genre = db.Column(db.String(50))
    poster_url = db.Column(db.String(200))
    release_date = db.Column(db.Date)
    showtimes = db.relationship('Showtime', backref='movie', lazy='dynamic')

    def __repr__(self):
        return f'<Movie {self.title}>'

class Showtime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    start_time = db.Column(db.DateTime, nullable=False)
    hall_id = db.Column(db.Integer, db.ForeignKey('hall.id'))
    price = db.Column(db.Float, nullable=False)
    bookings = db.relationship('Booking', backref='showtime', lazy='dynamic')
    available_seats = db.relationship('Seat', backref='showtime', lazy='dynamic')

    def __repr__(self):
        return f'<Showtime {self.movie.title} at {self.start_time}>'

class Hall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    rows = db.Column(db.Integer, nullable=False)
    cols = db.Column(db.Integer, nullable=False)
    showtimes = db.relationship('Showtime', backref='hall', lazy='dynamic')

    def __repr__(self):
        return f'<Hall {self.name}>'

class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    row = db.Column(db.String(2), nullable=False)  # A, B, C, etc.
    number = db.Column(db.Integer, nullable=False)  # 1, 2, 3, etc.
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtime.id'))
    is_reserved = db.Column(db.Boolean, default=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=True)

    def __repr__(self):
        return f'<Seat {self.row}{self.number}>'

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    showtime_id = db.Column(db.Integer, db.ForeignKey('showtime.id'))
    booking_time = db.Column(db.DateTime, default=datetime.utcnow)
    seats = db.relationship('Seat', backref='booking', lazy='dynamic')
    total_price = db.Column(db.Float)
    payment_status = db.Column(db.String(20), default='pending')  # pending, completed, cancelled

    def __repr__(self):
        return f'<Booking {self.id} by {self.customer.username}>'