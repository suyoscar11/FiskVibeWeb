from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from fiskvibe.models import User

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    last_name = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    fisk_id = StringField('Fisk ID',
                           validators=[DataRequired(), Length(min=6, max=7)])
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email (@my.fisk.edu)',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_fisk_id(self, fisk_id):
        user = User.query.filter_by(fisk_id=fisk_id.data).first()
        if user:
            raise ValidationError('Your ID has already been used to register.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
        if not email.data.endswith('@my.fisk.edu'):
            raise ValidationError('Please use your Fisk email address (@my.fisk.edu).')
        
        

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    last_name = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=100)])
    fisk_id = StringField('Fisk ID',
                           validators=[DataRequired(), Length(min=6, max=7)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
            
    def validate_fisk_id(self, fisk_id):
        if fisk_id.data != current_user.fisk_id:
            user = User.query.filter_by(fisk_id=fisk_id.data).first()
            if user:
                raise ValidationError('That ID is taken. Please use your valid ID number.')
    

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
    
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

        
class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. Please register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')