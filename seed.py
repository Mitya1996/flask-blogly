"""Seed file to make sample data for blogly db."""

from models import User, Post, db
from app import app

def seed_db():
    # Create all tables
    db.drop_all()
    db.create_all()

    # If table isn't empty, empty it
    User.query.delete()
    Post.query.delete()

    # Add users
    user1 = User(first_name='John', last_name="Smith")
    user2 = User(first_name='Mary', last_name="Antonova")
    user3 = User(first_name='Charles', last_name="Rodriguez")

    # Add posts
    post1 = Post(title='My First Post', content='Hello world!', user_id=1)
    post2 = Post(title='Random Post', content='I love apples.\nRadio is loud.\nToday I will mop the floor.', user_id=1)
    post3 = Post(title='Love Story', content='What is love. Baby don''t hurt me. Lorem ipsum la la dum dee boop.\nWhat is love. Baby don''t hurt me. Lorem ipsum la la dum dee boop.', user_id=1)

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    db.session.add_all([post1, post2, post3])
    db.session.commit()

seed_db()