from flask import render_template,url_for,flash,redirect
from webroot.forms import RegistrationForm, LoginForm
from webroot import app

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
    elif(form.username.data != None):
        flash(f'Failure create account for {form.username.data}!', 'fail')
        #return redirect(url_for('register'))
    return render_template('register.html', title='Register',form = form)

@app.route('/spell_check')
def spell_check():
    return "<h1>Check</h1>"

