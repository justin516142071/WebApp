from flask import render_template,url_for,flash,redirect,make_response
from webroot.forms import RegistrationForm, LoginForm, SpellScheckForm,LoginHistoryForm
from webroot import app, db, bcrypt
from webroot.models import User,History,Query
from flask_login import login_user, login_required, current_user,logout_user
from subprocess import check_output
from datetime import datetime

@app.route("/")
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.fc2 == form.fc2.data:
               login_user(user, remember=form.remember.data)
               history = History(user=current_user,logintime=str(datetime.now()),logouttime='N/A')
               current_user.currentLoginTime = history.logintime
               db.session.add(history)
               db.session.commit()
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
        user = User(username=form.username.data, password=hashed_password, fc2 = form.fc2.data, role = 'User')
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
        query = Query(querytext=content,queryresults=subout,user=current_user)
        db.session.add(query)
        db.session.commit()
    response = make_response(render_template('spell_check.html', title='Spell Check', form=form))
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response


@app.route("/logout")
@login_required
def logout():
    history = History.query.filter_by(logintime=current_user.currentLoginTime)
    history.logouttime = str(datetime.now())
    db.session.commit()
    logout_user()
    return redirect(url_for('login'))

@app.route("/history")
@login_required
def history():
    if current_user.role == 'User':
        queries = Query.query.filter_by(user=current_user)
        numqueries = len(list(queries))
        response = make_response(render_template('history.html', title='History', posts=queries,num=numqueries))
    elif current_user.role == 'Admin':
        queries = Query.query.all()
        numqueries = len(list(queries))
        response = make_response(render_template('history.html', title='History', posts=queries,num=numqueries))
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

@app.route("/history/query<int:queryid>")
@login_required
def query(queryid):
    if(current_user!= Query.query.get_or_404(queryid - 5).user and current_user.role != 'Admin'):
        return make_response("Unauthorized", 401)
    else:
        query = Query.query.get_or_404(queryid - 5)
        return render_template('query.html', title='Query', post=query)

@app.route("/login_history", methods=['GET','POST'])
@login_required
def loginhistory():
    if current_user.role != 'Admin':
        return make_response("Unauthorized",401)
    else:
        form = LoginHistoryForm()
        if form.validate_on_submit():
            userid = User.query.filter_by(username=form.userid.data).first().id
            histories = History.query.filter_by(user_id=userid)
            return render_template('login_history.html', title='Login History', posts=histories,form=form)
        return render_template('login_history.html', title='Login History', form=form)

