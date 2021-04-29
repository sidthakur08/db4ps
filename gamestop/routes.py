from flask import render_template, url_for, flash, redirect, request
from gamestop import app, db, bcrypt
from gamestop.forms import RegistrationForm, LoginForm, UpdateAccountForm
from gamestop.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from scipy import spatial
import json
import numpy as np

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

# loading games data
with open('./gamestop/games.txt','r') as f:
    games = json.load(f)

# loading the vector file
with open('gamestop/game_vector.txt','r') as f:
    game_vector = json.load(f)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account has been created! You can now log in', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/get_sim",methods = ['POST','GET'])
def get_sim():
    if request.method == 'GET':
        return render_template('get_similar.html', title='Similar Games', sim_games = "Enter the name of a game to get similar games.")
    
    else:
        name = [x for x in request.form.values()]

        try:
            def get_sim(a,b):
                return 1-spatial.distance.cosine(game_vector[a],game_vector[b])
        
            def get_5_sim(to_search):
                sim_measure = []
                for i in game_vector.keys():
                    try:
                        sim_measure.append(get_sim(to_search,i))
                    except:
                        sim_measure.append(0)
                sorted_sim_measure = np.argsort(sim_measure)[-6:-1][::-1]
                sim_games = [(games[s]['Name'],sim_measure[s]) for s in sorted_sim_measure]
                return sim_games
            
            sim_games = get_5_sim(name[0])

            if sim_games == [('Final Fantasy XII: The Zodiac Age', 0), ('Final Fantasy VIII Remastered', 0), ('Final Fantasy VII Remake', 0), ('Final Fantasy VII', 0), ('Final Fantasy Type-0 HD', 0)]:
                sim_games = False

        except Exception as e:
            sim_games = False

        return render_template('display_similar.html', title='Similar Games', game_name = name[0],sim_games = sim_games)
