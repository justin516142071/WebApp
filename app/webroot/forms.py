from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),Length(min=5,max=15)])
    fc2 = StringField('Two Factor',
                      validators=[DataRequired(),Length(min=10,max=10)])
    password = PasswordField('Password',
                             validators=[DataRequired(),Length(min=6,max=12)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),Length(min=5,max=15)])
    fc2 = StringField('Two Factor',
                      validators=[DataRequired(),Length(min=10,max=10)])
    password = PasswordField('Password',
                             validators=[DataRequired(),Length(min=6,max=12)])
    remember = BooleanField('Remember Me')
    login = SubmitField('Login')