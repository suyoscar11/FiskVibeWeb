from flask import render_template, url_for, flash, redirect, request
from fiskvibe import app, db, bcrypt, mail
from fiskvibe.forms import RegistrationForm, LoginForm, ResetPasswordForm, RequestResetForm
from fiskvibe.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


#creating some dummy posts here for now!
posts = [
    {
        'author': 'Suyog Gaire',
        'title': 'Post 1',
        'content': 'Hello, this is my first post on Fisk Vibe. Welcome y\'all!',
        'date_posted': 'April 20, 2026'
    },

    {
        'author': 'Jessica Xu',
        'title': 'Reflections on My First Semester',
        'content': 'As my first semester comes to an end, I’m reflecting on all the incredible experiences I’ve had. From great classes to amazing students, Fisk University has exceeded my expectations!',
        'date_posted': 'Dec 1, 2024'
    },
    {
        'author': 'Rohan Yadav',
        'title': 'Exploring the Fisk Campus',
        'content': 'Today, I took a long walk around the Fisk campus, and it was amazing! The historic buildings and the atmosphere here are just incredible. Looking forward to my time here.',
        'date_posted': 'May 1, 2024'
    },
    {
        'author': 'Remi Ore',
        'title': 'The Importance of Networking',
        'content': 'Networking has opened up so many opportunities for me during my time at Fisk. Whether it’s connecting with fellow students, professors, or attending guest speaker events, building relationships is key to success in college and beyond!',
        'date_posted': 'May 5, 2024'
    },
    {
        'author': 'Amanda Clark',
        'title': 'Why I Love Fisk Dining',
        'content': 'The food here at Fisk is amazing! From healthy options to comfort food, Sodexo offers it all. My favorite dish has to be the pasta station, but the daily specials always surprise me.',
        'date_posted': 'May 10, 2024'
    },
    {
        'author': 'Michael Thompson',
        'title': 'Balancing Academics and Social Life',
        'content': 'One of the biggest challenges for any college student is finding the right balance between studying and enjoying the college experience. Here are a few tips that have helped me stay on top of my coursework while still having fun with friends.',
        'date_posted': 'May 15, 2024'
    },
    {
        'author': 'Manoj Bagale',
        'title': 'Post 2',
        'content': 'I have nothing to tell! :)',
        'date_posted': 'April 21, 2024'
    },
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

@app.route("/account")
def account():
    return render_template('account.html', title='Account')



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data, password=hashed_password, fisk_id=form.fisk_id.data)
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


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)