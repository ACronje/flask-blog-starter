from dateutil import parser as date_parser

import pytest
import flask
from sqlalchemy.exc import IntegrityError

from flask_blog import models
from flask_blog.database import db

NO_POSTS_MESSAGE = b"No posts here so far."


def authenticate_user_for_client(client):
    user = models.User(username="john")
    user.set_password("super")
    db.session.add(user)
    db.session.commit()
    client.post('/login', data=dict(username="john", password="super"))


def test_empty_db(client):
    rv = client.get("/")
    assert NO_POSTS_MESSAGE in rv.data


def test_create_post(app_context, client):
    authenticate_user_for_client(client)

    title = "Test Post"
    content = "This is a test"
    rv = client.post(
        "/create",
        data=dict(title=title, content=content),
        follow_redirects=True,
    )
    assert flask.request.path == "/"
    assert NO_POSTS_MESSAGE not in rv.data
    assert title.encode() in rv.data

    posts = models.Post.query.all()
    assert len(posts) == 1
    assert posts[0].title == title
    assert posts[0].content == content
    assert posts[0].tags == []

    tags = "tag1,tag2,tAg2,   tAG3   "
    rv = client.post(
        "/create",
        data=dict(title=title, content=content, tags=tags),
        follow_redirects=True,
    )
    assert models.Post.query.all()[-1].tag_names == ['tag1', 'tag2', 'tag3']


def test_edit_post(app_context, client):
    authenticate_user_for_client(client)

    post = models.Post(title="Test Post", content="This is a test")

    db.session.add(post)
    db.session.commit()

    client.post(
        f"{post.id}/edit",
        data=dict(title="New Title", content="New content"),
        follow_redirects=True,
    )

    posts = models.Post.query.all()
    assert len(posts) == 1
    assert posts[0].title == "New Title"
    assert posts[0].content == "New content"
    assert posts[0].tags == []

    tags = "tag1,tag2,tag2"
    client.post(
        f"{post.id}/edit",
        data=dict(title="New Title", content="New content", tags=tags),
        follow_redirects=True,
    )
    assert models.Post.query.all()[-1].tag_names == ['tag1', 'tag2']


def test_delete_post(app_context, client):
    authenticate_user_for_client(client)

    post = models.Post(title="Test Post", content="This is a test")

    db.session.add(post)
    db.session.commit()

    client.post(
        f"{post.id}/delete",
        data=dict(),
        follow_redirects=True,
    )

    posts = models.Post.query.all()
    assert len(posts) == 0


def test_create_tag(app_context, client):
    name = "Test Tag"
    tag = models.Tag(name=name)

    db.session.add(tag)
    db.session.commit()

    dupe_tag = models.Tag(name=name)

    db.session.add(dupe_tag)
    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()

    name_lowercase = "test tag"
    dupe_lowercase_tag = models.Tag(name=name_lowercase)

    db.session.add(dupe_lowercase_tag)
    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()

    name_with_whitespace = "  test tag  "
    dupe_whitespace_tag = models.Tag(name=name_with_whitespace)

    db.session.add(dupe_whitespace_tag)
    with pytest.raises(IntegrityError):
        db.session.commit()
    
    db.session.rollback()


def test_add_tags_to_post(app_context, client):
    post = models.Post(title="Test Post", content="This is a test")
    tag = models.Tag(name="Test Tag")
    post.tags.append(tag)

    db.session.add(post)
    db.session.commit()
    assert models.Post.query.filter_by(id=post.id).first().tags == models.Tag.query.filter_by(id=tag.id).all()
