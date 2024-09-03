from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app import app, db
from models.user import User

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password_confirmation = request.form['password_confirmation']
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        if password != password_confirmation:
            flash('Passwords do not match!')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first() is not None:
            flash('Username already exists!')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email, password=password,
                        first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user) 
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user) 
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user() 
    return redirect(url_for('login'))
