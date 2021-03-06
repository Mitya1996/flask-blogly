"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from verify_image import is_image_and_ready

app = Flask(__name__)

# DebugToolbarExtension code str8 from docs
app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:myPassword@localhost:5432/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    return redirect('/users')

@app.route('/users')
def read_users():
    users = User.query.order_by(User.last_name).all()
    return render_template('index.html', users=users)

@app.route('/users/<int:id>')
def read_user(id):
    user = User.query.get(id)
    return render_template('user.html', user=user)
    
@app.route('/users/<int:id>/edit')
def update_user_get(id):
    user = User.query.get(id)
    return render_template('edit-user.html', user=user)

@app.route('/users/<int:id>/edit', methods=['POST'])
def update_user_post(id):
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']

    user = User.query.get(id)
    user.first_name = first_name
    user.last_name = last_name
    if is_image_and_ready(image_url):
        user.image_url = image_url
    db.session.commit()
    return redirect(f'/users/{id}')

@app.route('/users/<int:id>/delete', methods=['POST'])
def delete_user(id):
    User.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(f'/users')

@app.route('/users/new')
def new_user_get():
    return render_template('new-user.html')

@app.route('/users/new', methods=['POST'])
def new_user_post():
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url'] 
    if not is_image_and_ready(image_url): #check if img valid
        image_url = None
    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()
    return redirect(f'/users/{user.id}')