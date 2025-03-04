from app import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    poster_url = db.Column(db.String(200))  # Path to poster image
    showtimes = db.relationship('Showtime', backref='movie', lazy=True)