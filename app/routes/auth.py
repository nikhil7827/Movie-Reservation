from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from app import db
from app.models.user import User

bp = Blueprint('auth', __name__)

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        if User.query.filter_by(username=data['username']).first():
            flash('Username already exists')
            return redirect(url_for('auth.signup'))
        user = User(username=data['username'], email=data['email'], role='user')
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        flash('User created! Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('signup.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            if user.role == 'admin':
                return redirect(url_for('movie.view_movies'))
            return redirect(url_for('home'))
        flash('Invalid username or password.', 'error')
    return render_template('login.html')

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('auth.login'))