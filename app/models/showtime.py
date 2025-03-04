from app import db

class Showtime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    showtime = db.Column(db.DateTime, nullable=False)
    total_seats = db.Column(db.Integer, default=100)
    reserved_seats = db.Column(db.Integer, default=0)
    reservations = db.relationship('Reservation', backref='showtime', lazy=True)