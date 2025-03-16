from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

bp = Blueprint('reservation', __name__)

@bp.route('/')
@login_required
def reservation_details():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('movie.home'))

    reservations = []  # Replace with actual database query
    return render_template('reservation_details.html', reservations=reservations, user=current_user)