from flask import Flask, render_template,url_for,flash,redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '36bcc3a76770d2c6d91e2c014208b2e6'

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login',form = form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Success created account for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register',form = form)

@app.route('/spell_check')
def spell_check():
    return "<h1>Check</h1>"

if __name__ == '__main__':
    app.run()