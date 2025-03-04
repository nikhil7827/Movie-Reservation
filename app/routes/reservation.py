from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.showtime import Showtime
from app.models.reservation import Reservation
from datetime import datetime

bp = Blueprint('reservation', __name__)

@bp.route('/showtimes/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def showtimes(movie_id):
    from app.models.movie import Movie
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST' and current_user.role == 'admin':
        data = request.form
        showtime = Showtime(movie_id=movie_id, showtime=data['showtime'],
                            total_seats=data.get('total_seats', 100))
        db.session.add(showtime)
        db.session.commit()
        flash('Showtime added!')
        return redirect(url_for('reservation.showtimes', movie_id=movie_id))
    showtimes = Showtime.query.filter_by(movie_id=movie_id).all()
    return render_template('showtimes.html', movie=movie, showtimes=showtimes)

@bp.route('/reservations', methods=['GET'])
@login_required
def get_user_reservations():
    reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    return render_template('reservations.html', reservations=reservations, now=datetime.utcnow())