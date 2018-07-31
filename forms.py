from flask_wtf.form import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,Length

class SingupForm(FlaskForm):
    first_name=StringField('First Name',validators=[DataRequired("Please enter your first name")])
    last_name=StringField('Last Name',validators=[DataRequired("Please enter your last name")])
    email=StringField('Email',validators=[DataRequired("Enter email address"),Email('Please enter your email address')])
    password=PasswordField('Password',validators=[DataRequired("Enter password"),Length(min=6,message='password must be 6 chars or more.')])
    submit=SubmitField('Sign up')

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired('Enter your email address'),Email('Please enter your email address')])
    password=PasswordField('Password',validators=[DataRequired('Please enter a password')])
    submit=SubmitField('Sign in')

class AddressForm(FlaskForm):
    address=StringField('Address',validators=[DataRequired("please enter an address")])
    submit=SubmitField('Search')