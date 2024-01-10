from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from . import db

class SignupForm_user(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(max=20)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6)])
    display_name = StringField('display_name', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Continue')

class SignupForm_driver(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(max=20)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6)])
    display_name = StringField('display_name', validators=[DataRequired(), Length(max=20)])
    vehicle_type = StringField('vehicle_type', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Continue')

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('LogIn')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    display_name = db.Column(db.String(20), nullable=False)

class Driver(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    display_name = db.Column(db.String(20), nullable=False)
    vehicle_type = db.Column(db.String(20), nullable=False)

class googleUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)