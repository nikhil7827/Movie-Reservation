from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.user import User

bp = Blueprint('auth', __name__)

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

@bp.route('/login', methods=['GET', 'POST'], endpoint='auth_user_login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('movie.home'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form, user=current_user)

@bp.route('/register', methods=['GET', 'POST'], endpoint='auth_user_register')
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists.', 'danger')
            return redirect(url_for('auth.auth_user_register'))
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now login.', 'success')
        return redirect(url_for('auth.auth_user_login'))
    return render_template('register.html', form=form, user=current_user)

@bp.route('/logout', endpoint='auth_user_logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('movie.home'))

@bp.route('/dashboard', endpoint='auth_user_dashboard')
@login_required
def admin_dashboard():  # Renamed from 'dashboard'
    return render_template('movies.html', user=current_user)