from app import db


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    poster_url = db.Column(db.String(200), nullable=True, default='https://via.placeholder.com/150')
    ticket_price = db.Column(db.Float, nullable=False, default=10.00)
    showtimes = db.Column(db.String(200), nullable=True)
    def __repr__(self):
        return f'<Movie {self.title}>'
