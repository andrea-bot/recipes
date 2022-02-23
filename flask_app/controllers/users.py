from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/create', methods = ['post'])
def create_user():

    if not User.validate_user(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash,
    }

    user_id = User.save(data)

    session['logged_user'] = user_id

    return redirect('/dashboard')

@app.route('/user/login', methods = ['post'])
def login_user():
    data = {
        "email" : request.form['email']
    }

    retrieved_user = User.get_by_email(data)

    if not retrieved_user:
        flash("Invalid email/password", "login_error")
        return redirect('/')

    if not bcrypt.check_password_hash(retrieved_user.password, request.form['password']):
        flash("Invalid email/password", "login_error")
        return redirect('/')

    session['logged_user'] = retrieved_user.id

    return redirect('/dashboard')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/') 