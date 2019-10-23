from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,ValidationError,TextAreaField
from wtforms.validators import DataRequired,Length, EqualTo
from webroot.models import User

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

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired()],id = 'uname')
    fc2 = StringField('Two Factor',
                      validators=[DataRequired()],id= '2fa')
    password = PasswordField('Password',
                             validators=[DataRequired()], id ='pword')
    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

class SpellScheckForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Check')
