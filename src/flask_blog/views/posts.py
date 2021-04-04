from flask import Blueprint, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from sqlalchemy.sql import func

from ..database import db
from ..models import Post, Tag, posttags_table
from .helpers import (
    tags_from_form,
    parse_date_or_none,
    convert_date_to_iso8601_string,
)

posts = Blueprint("posts", __name__)


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
def delete(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)

    db.session.delete(post)
    db.session.commit()

    flash('"{}" was successfully deleted!'.format(post.id))
    return redirect(url_for("posts.index"))
