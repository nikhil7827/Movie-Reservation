from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.movie import Movie

bp = Blueprint('movie', __name__)

@bp.route('/')
def home():
    all_movies = Movie.query.all()
    seen_titles = set()
    movies = []
    for movie in all_movies:
        if movie.title not in seen_titles:
            seen_titles.add(movie.title)
            showtimes = getattr(movie, 'showtimes', None)  # Safe access
            print(f"Movie: {movie.title}, Showtimes: {movie.showtimes}")
            movies.append(movie)
    return render_template('home.html', movies=movies)

@bp.route('/movies')
@login_required
def view_movies():
    if current_user.role != 'admin':
        flash('Permission denied.', 'error')
        return redirect(url_for('home'))
    movies = Movie.query.all()
    return render_template('view_movies.html', movies=movies)

@bp.route('/add_movie', methods=['GET'])
@login_required
def show_add_movie():
    if current_user.role != 'admin':
        flash('Permission denied.', 'error')
        return redirect(url_for('home'))
    return render_template('add_movie.html')

@bp.route('/add_movie', methods=['POST'])
@login_required
def add_movie():
    if current_user.role != 'admin':
        flash('Permission denied.', 'error')
        return redirect(url_for('home'))
    data = request.form
    existing_movie = Movie.query.filter_by(title=data['title']).first()
    if existing_movie:
        flash('A movie with this title already exists.', 'error')
        return redirect(url_for('movie.show_add_movie'))
    new_movie = Movie(
        title=data['title'],
        description=data['description'],
        genre=data['genre'],
        poster_url=data.get('poster_url', ''),
        ticket_price=float(data.get('ticket_price', 10.00)),
        showtimes=data.get('showtimes', '')
    )
    try:
        db.session.add(new_movie)
        db.session.commit()
        flash('Movie added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('movie.view_movies'))

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
    return redirect(url_for('movie.view_movies'))

@bp.route('/movie/<int:movie_id>', methods=['GET'])
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    print(f"Movie: {movie.title}, Showtime: {movie.showtimes}")
    seats = [[f'{row}{col}' for col in range(1, 6)] for row in 'ABCDE']
    return render_template('movie_detail.html', movie=movie, seats=seats)

@bp.route('/payment/<int:movie_id>', methods=['POST'])
@login_required
def payment(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    selected_seats = request.form.getlist('seats')
    if not selected_seats:
        flash('Please select at least one seat to proceed.', 'error')
        return redirect(url_for('movie.movie_detail', movie_id=movie.id))
    total_price = len(selected_seats) * movie.ticket_price
    return render_template('payment.html', movie=movie, selected_seats=selected_seats, total_price=total_price)

@bp.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit_movie(movie_id):
    if current_user.role != 'admin':
        flash('Permission denied.', 'error')
        return redirect(url_for('home'))
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        movie.title = request.form['title']
        movie.description = request.form['description']
        movie.genre = request.form['genre']
        movie.poster_url = request.form.get('poster_url', '')
        movie.ticket_price = float(request.form.get('ticket_price', 10.00))
        movie.showtime = request.form.get('showtimes', '')
        try:
            db.session.commit()
            flash('Movie updated successfully!', 'success')
            return redirect(url_for('movie.view_movies'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating movie: {str(e)}', 'error')
    return render_template('edit_movie.html', movie=movie)

@bp.route('/showtime/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def manage_showtimes(movie_id):
    if current_user.role != 'admin':
        flash('Permission denied.', 'error')
        return redirect(url_for('home'))
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        showtime = request.form.get('showtimes', '').strip()
        if showtime:
            movie.showtime = showtime
        else:
            movie.showtime = None
        try:
            db.session.commit()
            flash('Showtime updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating showtimes: {str(e)}', 'error')
        return redirect(url_for('movie.view_movies'))
    return render_template('showtimes.html', movie=movie)