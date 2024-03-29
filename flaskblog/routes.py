import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

post = [
    {
        'author': 'By James Sa Corey',
        'title': 'Blog 1',
        'content': 'Post number 1 ' ,
        'date_posted': '6-2-2019'

    }, 

    {
        'author': 'By Cammie',
        'title': 'Blog me',
        'content': 'Post number 2' ,
        'date_posted': '6-5-2019'

    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=post)

@app.route("/about")
def about():
    return render_template('about.html', title='About me')

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data.lower(), password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created, you can now log in','success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit:
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else  redirect(url_for('home'))
        else:
            flash('Login Unsuccessful, check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
        logout_user()
        return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
           picture_file = save_picture(form.picture.data)
           current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    imagefile = url_for('static', filename='pics/' + current_user.image_file)
    return render_template('account.html', title='Account', imagefile=imagefile, form=form)

    @app.route('/post/new', method=['Post','GET','DELETE'])
    @login_required
    def post():
        form = PostForm()
        if form.validate_on_submit():
                flash('Post has been created', 'success')
                return redirect(url_for('home'))
        return render_template('create_post.html', title='New Post', form=form)
