from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.movie import Movie

bp = Blueprint('movie', __name__)


# Home page
@bp.route('/')
def home():
    movies = Movie.query.all()
    return render_template('home.html', movies=movies)


# View all movies (admin)
@bp.route('/movies')
@login_required
def view_movies():
    if current_user.role != 'admin':
        flash('Permission denied.', 'error')
        return redirect(url_for('home'))
    movies = Movie.query.all()
    return render_template('view_movies.html', movies=movies)


# Show add movie form
@bp.route('/add_movie', methods=['GET'])
@login_required
def show_add_movie():
    if current_user.role != 'admin':
        flash('Permission denied.', 'error')
        return redirect(url_for('home'))
    return render_template('add_movie.html')


# Handle movie addition (POST)
@bp.route('/add_movie', methods=['POST'])
@login_required
def add_movie():
    if current_user.role != 'admin':
        flash('Permission denied.', 'error')
        return redirect(url_for('home'))
    data = request.form
    new_movie = Movie(
        title=data['title'],
        description=data['description'],
        genre=data['genre'],
        poster_url=data.get('poster_url', ''),
        ticket_price=float(data.get('ticket_price', 10.00))
    )
    try:
        db.session.add(new_movie)
        db.session.commit()
        flash('Movie added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('view_movies'))


# Movie detail with seat selection
@bp.route('/movie/<int:movie_id>', methods=['GET'])
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    seats = [[f'{row}{col}' for col in range(1, 6)] for row in 'ABCDE']  # Simple 5x5 seat grid
    return render_template('movie_detail.html', movie=movie, seats=seats)

#Delete movie (admin)
@bp.route('/delete_movie/<int:movie_id>', methods=['POST'])
@login_required
def delete_movie(movie_id):
    if current_user.role != 'admin':
        flash('Permission denied.', 'error')
        return redirect(url_for('home'))
    movie = Movie.query.get_or_404(movie_id)
    try:
        db.session.delete(movie)
        db.session.commit()
        flash('Movie deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting movie: {str(e)}', 'error')
    return redirect(url_for('view_movies'))

# Payment page
@bp.route('/payment/<int:movie_id>', methods=['POST'])
@login_required
def payment(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    selected_seats = request.form.getlist('seats')  # Get list of selected seats
    if not selected_seats:
        flash('Please select at least one seat to proceed.', 'error')
        return redirect(url_for('movie.movie_detail', movie_id=movie.id))
    total_price = len(selected_seats) * movie.ticket_price
    return render_template('payment.html', movie=movie, selected_seats=selected_seats, total_price=total_price)