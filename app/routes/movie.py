from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models.movie import Movie
import os

bp = Blueprint('movie', __name__)

@bp.route('/', endpoint='movie_home')
def home():
    print("Attempting to render 'home.html'")
    print("Current working directory:", os.getcwd())
    all_movies = Movie.query.all()
    seen_titles = set()
    movies = []
    for movie in all_movies:
        if movie.title not in seen_titles:
            seen_titles.add(movie.title)
            showtimes = getattr(movie, 'showtimes', None)
            print(f"Movie: {movie.title}, Showtimes: {showtimes}")
            movies.append(movie)
    return render_template('home.html', movies=movies, user=current_user)

@bp.route('/movies', endpoint='view_movies')
def view_movies():
    movies = Movie.query.all()
    return render_template('view_movies.html', movies=movies, user=current_user)

@bp.route('/add_movie', methods=['GET', 'POST'], endpoint='movie_add_movie')
@login_required
def add_movie():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('movie.home'))
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        genre = request.form.get('genre')
        poster_url = request.form.get('poster_url')
        ticket_price = float(request.form.get('ticket_price', 10.00))
        showtimes = request.form.get('showtimes')
        if not title or not description or not genre:
            flash('Title, description, and genre are required.', 'danger')
            return redirect(url_for('movie.movie_add_movie'))
        movie = Movie(title=title, description=description, genre=genre, poster_url=poster_url, ticket_price=ticket_price, showtimes=showtimes)
        db.session.add(movie)
        db.session.commit()
        flash('Movie added successfully!', 'success')
        return redirect(url_for('auth.auth_user_dashboard'))
    return render_template('add_movie.html', user=current_user)

@bp.route('/delete_movie/<int:movie_id>', methods=['POST'], endpoint='delete_movie')
@login_required
def delete_movie(movie_id):
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('movie.home'))
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Movie deleted successfully!', 'success')
    return redirect(url_for('auth.auth_user_dashboard'))

@bp.route('/movie/<int:movie_id>', endpoint='movie_detail')
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template('movie_detail.html', movie=movie, user=current_user)

@bp.route('/payment/<int:movie_id>', methods=['GET', 'POST'], endpoint='payment')
@login_required
def payment(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        selected_seats = request.form.getlist('seats')
        showtime = request.form.get('showtime')
        if not selected_seats:
            flash('Please select at least one seat.', 'danger')
            return redirect(url_for('movie.movie_detail', movie_id=movie_id))
        if not showtime:
            flash('Please select a showtime.', 'danger')
            return redirect(url_for('movie.movie_detail', movie_id=movie_id))
        total_price = len(selected_seats) * movie.ticket_price
        return render_template('payment.html', movie=movie, user=current_user,
                             selected_seats=selected_seats, showtime=showtime, total_price=total_price)
    return redirect(url_for('movie.movie_detail', movie_id=movie_id))

@bp.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'], endpoint='edit_movie')
@login_required
def edit_movie(movie_id):
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('movie.home'))
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        movie.title = request.form.get('title')
        movie.description = request.form.get('description')
        movie.genre = request.form.get('genre')
        movie.poster_url = request.form.get('poster_url')
        movie.ticket_price = float(request.form.get('ticket_price', 10.00))
        movie.showtimes = request.form.get('showtimes')
        db.session.commit()
        flash('Movie updated successfully!', 'success')
        return redirect(url_for('auth.auth_user_dashboard'))
    return render_template('edit_movie.html', movie=movie, user=current_user)

@bp.route('/manage_showtimes/<int:movie_id>', methods=['GET', 'POST'], endpoint='manage_showtimes')
@login_required
def manage_showtimes(movie_id):
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('movie.home'))
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        movie.showtimes = request.form.get('showtimes')
        db.session.commit()
        flash('Showtimes updated successfully!', 'success')
        return redirect(url_for('auth.auth_user_dashboard'))
    return render_template('showtimes.html', movie=movie, user=current_user)