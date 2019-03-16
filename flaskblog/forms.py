from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2,max=15)])
    email = StringField('Email', 
                            validators= [DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired(), Length(min=8, max=20, message="Password must be at least 8 characters long")])
    confirm_password = PasswordField('Confirm Password', 
                            validators=[DataRequired(), EqualTo('password', message="Password is not the same")])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username taken use a different username')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email taken use a different email')
    

class LoginForm(FlaskForm):  
    email = StringField('Email', 
                            validators= [DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired(), Length(min=8, max=20, message="Password must be at least 8 characters long")])
    remember = BooleanField('Remember me')

    submit = SubmitField('Login')


class UpdateForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2,max=15)])
    email = StringField('Email', 
                            validators= [DataRequired(), Email()])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg','png','svg'])])

    submit = SubmitField('Update')

def validate_username(self, username):
    if username.data != current_user.username:
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username taken use a different username')

def validate_email(self, email):
    if email.data != current_user.email:
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email taken use a different email')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')