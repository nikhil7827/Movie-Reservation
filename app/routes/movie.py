from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.movie import Movie

bp = Blueprint('movie', __name__)

@bp.route('/movies', methods=['GET', 'POST'])
def get_movies():
    if request.method == 'POST' and current_user.role == 'admin':
        data = request.form
        movie = Movie(title=data['title'], description=data['description'],
                      genre=data['genre'], poster_url=data.get('poster_url', ''))
        db.session.add(movie)
        db.session.commit()
        flash('Movie added successfully!')
        return redirect(url_for('movie.get_movies'))
    movies = Movie.query.all()
    return render_template('movies.html', movies=movies)