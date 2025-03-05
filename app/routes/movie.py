from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.movie import Movie  # Assuming 'movie' is the module, and 'Movie' is the class

bp = Blueprint('movie', __name__)


# Route to display all movies (GET only)
@bp.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return render_template('movies.html', movies=movies)


# Route to add a new movie (POST only, admin only)
@bp.route('/add_movie', methods=['POST'])
@login_required  # Ensure the user is logged in
def add_movie():
    if current_user.role != 'admin':  # Check if the user is an admin
        flash('You do not have permission to add movies.', 'error')
        return redirect(url_for('movie.get_movies'))

    data = request.form
    new_movie = Movie(
        title=data['title'],
        description=data['description'],
        genre=data['genre'],
        poster_url=data.get('poster_url', '')  # Optional field with default empty string
    )

    try:
        db.session.add(new_movie)
        db.session.commit()
        flash('Movie added successfully!', 'success')
    except Exception as e:
        db.session.rollback()  # Undo changes if something goes wrong
        flash(f'Error adding movie: {str(e)}', 'error')

    return redirect(url_for('movie.get_movies'))