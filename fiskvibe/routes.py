from flask import render_template, url_for, flash, redirect, request
from fiskvibe import app, db, bcrypt
from fiskvibe.forms import RegistrationForm, LoginForm
from fiskvibe.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        'author': 'Suyog Gaire',
        'title': 'Blog Post 1',
        'content': 'Hello This is my first post on Fisk Vibe. Welcome y\'all',
        'date_posted': 'April 20, 2026'
    },
    {
        'author': 'Manoj Bagale',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2024'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/feed")
def feed():
    return render_template('feed.html', title='Feed', posts=posts)

@app.route("/events")
def events():
    return render_template('events.html', title='Events')

@app.route("/mmp")
def mmp():
    return render_template('mmp.html', title='MMP')

@app.route("/dining")
def dining():
    return render_template('dining.html', title='Dining')

@app.route("/resources")
def resources():
    return render_template('resources.html', title='Resources')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Congrats! Your account has been created! You can log in now!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')