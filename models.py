"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    first_name = db.Column(
        db.String(50),
        nullable=False,
        unique=True)
    last_name = db.Column(
        db.String(50),
        nullable=False,
        unique=True)
    image_url = db.Column(
        db.String(), 
        default="/static/default-user-image.png")

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    title = db.Column(
        db.String(50),
        nullable=False)
                
    content = db.Column(
        db.Text,
        nullable=False)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )

    user = db.relationship('User', backref='posts')


class Tag(db.Model):
    """Post."""

    __tablename__ = "tags"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)

    name = db.Column(
        db.String(50),
        nullable=False,
        unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        backref="tags"
    )

class PostTag(db.Model):
    """Post."""

    __tablename__ = "posts_tags"

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id', ondelete='CASCADE'),
        primary_key=True)

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey('tags.id', ondelete='CASCADE'),
        primary_key=True)
