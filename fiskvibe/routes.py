from flask import render_template, url_for, flash, redirect
from fiskvibe import app
from fiskvibe.forms import RegistrationForm, LoginForm
from fiskvibe.models import User, Post

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
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
