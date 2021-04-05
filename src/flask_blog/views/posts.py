from flask import Blueprint, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_user, logout_user, login_required

from ..database import db
from ..models import Post, Tag, posttags_table, User
from ..helpers import (
    tags_from_form,
    parse_date_or_none,
    convert_date_to_iso8601_string,
)

posts = Blueprint("posts", __name__)


@posts.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("posts.index"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            flash("Username and password required")
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                # username already taken
                db.session.rollback()
            flash("A user has been created for you if one did not exist")
            return redirect(url_for("posts.login"))
    return render_template("register.html")


@posts.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("posts.index"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            flash("Username and password required")
        else:
            user = User.query.filter_by(username=username).first()
            if user is None or not user.check_password(password):
                flash("Invalid username or password")
                return redirect(url_for("posts.login"))
            login_user(user)
            flash("Login successful!")
            return redirect(url_for("posts.index"))
    return render_template("login.html")


@posts.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("posts.index"))


@posts.route("/")
def index():
    existing_querystring_dict = request.args.to_dict()
    date_filter = parse_date_or_none(request.args.get("date"))
    tag_filter = request.args.get("tag")

    posts_filter = Post.query
    if date_filter:
        posts_filter = posts_filter.filter(
            func.date(Post.created_at)
            == convert_date_to_iso8601_string(date_filter)
        )
    if tag_filter:
        posts_filter = (
            posts_filter.join(posttags_table)
            .join(Tag)
            .filter(Tag.name == tag_filter)
        )
    posts = posts_filter.all()
    tags = Tag.query.join(posttags_table).join(Post).all()
    dates = list(
        set(
            [
                convert_date_to_iso8601_string(row.created_at)
                for row in Post.query.with_entities(Post.created_at)
            ]
        )
    )

    return render_template(
        "index.html",
        posts=posts,
        tags=tags,
        dates=dates,
        existing_querystring_dict=existing_querystring_dict,
    )


@posts.route("/<int:post_id>")
def post(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)
    return render_template("post.html", post=post)


@posts.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        tag_names = tags_from_form(request.form)

        if not title:
            flash("Title is required!")
        else:
            new_post = Post(title=title, content=content)
            new_post.tags = Tag.find_or_add_tags_by_name(tag_names)

            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for("posts.index"))
    return render_template("create.html")


@posts.route("/<int:post_id>/edit", methods=("GET", "POST"))
@login_required
def edit(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        tag_names = tags_from_form(request.form)

        if not title:
            flash("Title is required!")
        else:
            post.tags = Tag.find_or_add_tags_by_name(tag_names)
            post.title = title
            post.content = content

            db.session.commit()

            return redirect(url_for("posts.index"))

    return render_template("edit.html", post=post)


@posts.route("/<int:post_id>/delete", methods=("POST",))
@login_required
def delete(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)

    db.session.delete(post)
    db.session.commit()

    flash('"{}" was successfully deleted!'.format(post.id))
    return redirect(url_for("posts.index"))
