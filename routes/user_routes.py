from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import app, db
from models.user import User

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        new_username = request.form['username']
        new_email = request.form['email']
        new_first_name = request.form['first_name']
        new_last_name = request.form['last_name']
        new_password = request.form['password']
        new_password_confirmation = request.form['password_confirmation']

        if new_password != new_password_confirmation:
            flash('Passwords do not match!')
            return redirect(url_for('profile'))

        user = User.query.get(current_user.id)
        if not user:
            flash('User not found!')
            return redirect(url_for('profile'))

        user.username = new_username
        user.email = new_email
        user.first_name = new_first_name
        user.last_name = new_last_name

        if new_password:
            user.password = new_password 

        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('profile'))

    return render_template('profile.html', user=current_user)
