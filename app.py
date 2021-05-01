"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag, Comment
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

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')
def homepage():
    latest_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('index.html', posts=latest_posts)

@app.route('/users')
def users():
    users = User.query.order_by(User.last_name).all()
    return render_template('users.html', users=users)

@app.route('/users/<int:id>')
def read_user(id):
    user = User.query.get_or_404(id)
    posts = user.posts[::-1] #reverse list to get first post at bottom
    return render_template('user.html', user=user, posts=posts)
    
@app.route('/users/<int:id>/edit')
def update_user_get(id):
    user = User.query.get_or_404(id)
    return render_template('edit-user.html', user=user)

@app.route('/users/<int:id>/edit', methods=['POST'])
def update_user_post(id):
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']

    user = User.query.get_or_404(id)
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
    return redirect(f'/')

@app.route('/users/new')
def new_user_get():
    return render_template('new-user.html')

@app.route('/users/new', methods=['POST'])
def new_user_post():
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']
    #verify valid input
    if not first_name:
        flash('The user must have a first name.')
        return redirect(f'/users/new')
    if not last_name:
        flash('The user must have a last name.')
        return redirect(f'/users/new')  

    if not is_image_and_ready(image_url): #check if img valid
        image_url = None
    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()
    return redirect(f'/users/{user.id}')

@app.route('/users/<int:id>/posts/new')
def new_post_get(id):
    user = User.query.get_or_404(id)
    tags = Tag.query.all()
    return render_template('new-post.html', user=user, tags=tags)

@app.route('/users/<int:id>/posts/new', methods=['POST'])
def new_post_post(id):
    title = request.form['post-title']
    content = request.form['post-content']
    tags_list = request.form.getlist('checkbox')
    #verify valid input
    if not title:
        flash('The post must have a title.')
        return redirect(f'/users/{id}/posts/new')
    if not content:
        flash('The post must have content.')
        return redirect(f'/users/{id}/posts/new')  
    #add post and tags  
    post = Post(title=title, content=content, user_id=id)        
    db.session.add(post)
    db.session.commit()
    if tags_list:
        for tag in tags_list:
            post_tag = PostTag(post_id=post.id, tag_id=int(tag))
            db.session.add(post_tag)
            db.session.commit()
    return redirect(f'/users/{id}')


@app.route('/posts/<int:id>')
def read_post(id):
    post = Post.query.get_or_404(id)
    comments = Comment.query.filter(Comment.post_id == id).order_by(Comment.created_at.desc()).all()
    all_users = User.query.all()
    return render_template('post.html', post=post, user=post.user, comments=comments, all_users=all_users)


@app.route('/posts/<int:id>/edit')
def edit_post(id):
    post = Post.query.get_or_404(id)
    tags = Tag.query.all()
    return render_template('edit-post.html', post=post, user=post.user, tags=tags)

@app.route('/posts/<int:id>/edit', methods=['POST']) ###
def edit_post_post(id):
    title = request.form['post-title']
    content = request.form['post-content']
    tags_list = request.form.getlist('checkbox')
    post = Post.query.get_or_404(id)
    post.title = title
    post.content = content
    db.session.commit()
    PostTag.query.filter(PostTag.post_id == id).delete() #delete any existing tags
    db.session.commit() #update tags
    if tags_list:
        for tag in tags_list:
            post_tag = PostTag(post_id=post.id, tag_id=int(tag))
            db.session.add(post_tag)
            db.session.commit()
    return redirect(f'/posts/{id}')

@app.route('/posts/<int:id>/delete', methods=['POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    user_id = post.user_id
    Post.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/tags')
def tags_read():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/new')
def tag_create_get():
    return render_template('new-tag.html')

@app.route('/tags/new', methods=['POST'])
def tag_create_post():
    name = request.form['tag-name']
    if not name:
        flash('Tag must not be empty.')
        return redirect(f'/tags/new')
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:id>')
def tag_read(id):
    tag = Tag.query.get(id)
    return render_template('tag.html', tag=tag, posts=tag.posts)

@app.route('/comments/new', methods=['POST'])
def new_comment():
    post_id = request.args['post-id']
    author = request.form['comment-author']
    text = request.form['comment-text']
    names_arr = author.split()
    #check validity
    try:
        first_name = names_arr[0]
        last_name = names_arr[1]
    except:
        flash('Post must be made by a valid user.')
        return redirect(f'/posts/{post_id}')
    user = User.query.filter(User.first_name == first_name, User.last_name == last_name).first()
    if not user:
        flash('Post must be made by a valid user.')
        return redirect(f'/posts/{post_id}')
    if not text:
        flash('Comment must not be empty.')
        return redirect(f'/posts/{post_id}')
    comment = Comment(post_id=post_id, user_id=user.id, text=text)
    db.session.add(comment)
    db.session.commit()
    return redirect(f'/posts/{post_id}')