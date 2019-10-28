from flask import render_template,url_for,flash,redirect,make_response
from webroot.forms import RegistrationForm, LoginForm, SpellScheckForm
from webroot import app, db, bcrypt
from webroot.models import User
from flask_login import login_user, login_required
from subprocess import check_output

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.fc2 == form.fc2.data:
               login_user(user,remember=form.remember.data)
               flash(f'Success login account for {form.username.data}!', 'success')
               return redirect(url_for('spell_check'))
            else:
                flash(f'Failure login account for {form.username.data}! Two-factor Authentication Failed', 'error')
        else:
            flash(f'Failure login account for {form.username.data}! Incorrect Username or Password', 'error')
    response = make_response(render_template('login.html', title='Login',form = form))
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password, fc2 = form.fc2.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Success created account for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    elif(form.username.data != None):
        flash(f'Failure create account for {form.username.data}!', 'fail')
        return redirect(url_for('register'))
    response = make_response(render_template('register.html', title='Register',form = form))
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

@app.route('/spell_check', methods=['GET','POST'])
@login_required
def spell_check():
    form = SpellScheckForm()
    if form.validate_on_submit():
        content = form.content.data
        file1 = open("content.txt", "w")  # write mode
        file1.write(content)
        file1.close()
        cmd = ["./a.out", "content.txt", "wordlist.txt"]
        subout = check_output(cmd).decode("utf-8")
        form.outcontent.data = form.content.data
        form.misspelled.data = subout
    response = make_response(render_template('spell_check.html', title='Spell Check', form=form))
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

