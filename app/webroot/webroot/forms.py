from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),Length(min=6,max=20)],id = 'uname')
    fc2 = StringField('Two Factor',
                      validators=[DataRequired(),Length(min=10,max=10)],id= '2fa')
    password = PasswordField('Password',
                             validators=[DataRequired(),Length(min=6,max=20)], id ='pword')
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(),Length(min=5,max=15)],id = 'uname')
    fc2 = StringField('Two Factor',
                      validators=[DataRequired(),Length(min=10,max=10)],id= '2fa')
    password = PasswordField('Password',
                             validators=[DataRequired(),Length(min=6,max=12)], id ='pword')
    remember = BooleanField('Remember Me')
    login = SubmitField('Login')