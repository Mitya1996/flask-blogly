"""Seed file to make sample data for blogly db."""

from models import User, Post, Tag, PostTag, Comment, db
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
    db.session.add_all([user1, user2, user3])
    db.session.commit()

    # Add posts
    post1 = Post(title='My First Post', content='Hello world!', user_id=1)
    post2 = Post(title='Random Post', content='I love apples.\nRadio is loud.\nToday I will mop the floor.', user_id=1)
    post3 = Post(title='Love Story', content='What is love. Baby don''t hurt me. Lorem ipsum la la dum dee boop.\nWhat is love. Baby don''t hurt me. Lorem ipsum la la dum dee boop.', user_id=1)
    post4 = Post(title='I am Mary', content='I am the best user ever.\nThere is absolutely no user better than me.\nThat is because I am a gigachad female.\nRoflcopter soi soi soi.', user_id=2)
    post5 = Post(title='Armchairs', content='Have you ever thought about how no hay nadie sentado en esa silla. Porque?', user_id=2)
    post6 = Post(title='Eating Lunch', content='Davaite ne budem dratsya. Mojet bit ya seichas poidu pogulyat.\nVot eto prikol!!!\nDavaite ne budem dratsya. Mojet bit ya seichas poidu pogulyat.\nVot eto prikol!!!', user_id=2)
    db.session.add_all([post1, post2, post3, post4, post5, post6])
    db.session.commit()
 
    # Add tags
    tag1 = Tag(name='Funny')
    tag2 = Tag(name='Silly')
    tag3 = Tag(name='Dumb')
    db.session.add_all([tag1, tag2, tag3])
    db.session.commit()

    # Add post_tags
    post_tag1 = PostTag(post_id=6, tag_id=2)
    post_tag2 = PostTag(post_id=6, tag_id=3)
    post_tag3 = PostTag(post_id=3, tag_id=1)
    post_tag4 = PostTag(post_id=3, tag_id=2)
    post_tag5 = PostTag(post_id=2, tag_id=2)
    db.session.add_all([post_tag1, post_tag2, post_tag3, post_tag4, post_tag5])
    db.session.commit()

    comment1 = Comment(post_id=3, user_id=2, text="Wow what a great post!")
    comment2 = Comment(post_id=3, user_id=3, text="Dumb...")
    db.session.add_all([comment1, comment2])
    db.session.commit()


seed_db()