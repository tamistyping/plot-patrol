from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import app, db
from models.user import User
from models.property import Property

@app.route('/profile')
@login_required
def user_profile():
    properties = Property.query.filter_by(owner_id=current_user.id).all()
    total_property_value = sum(property.value for property in properties)
    return render_template('user_profile.html', user=current_user, properties=properties, total_property_value=total_property_value)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        new_username = request.form['username']
        new_email = request.form['email']
        new_first_name = request.form['first_name']
        new_last_name = request.form['last_name']
        new_password = request.form['password']
        new_password_confirmation = request.form['password_confirmation']

        if new_password != new_password_confirmation:
            flash('Passwords do not match!')
            return redirect(url_for('edit_profile'))

        user = User.query.get(current_user.id)
        if not user:
            flash('User not found!')
            return redirect(url_for('edit_profile'))

        user.username = new_username
        user.email = new_email
        user.first_name = new_first_name
        user.last_name = new_last_name

        if new_password:
            user.password = new_password  

        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('user_profile'))

    return render_template('edit_profile.html', user=current_user)
