from datetime import datetime
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.exc import IntegrityError

from .database import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)
    tags = relationship("Tag", secondary=lambda: posttags_table)

    def __repr__(self):
        return "<Post id={}, title='{}'>".format(self.id, self.title)

    tag_names = association_proxy("tags", "name")


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(collation="NOCASE"), nullable=False, unique=True
    )

    def __repr__(self):
        return "<Tag id={}, name='{}'>".format(self.id, self.name)

    @validates("name")
    def normalize_name(self, key, value):
        return value.strip().lower()

    @classmethod
    def find_or_add_tags_by_name(cls, tag_names):
        tags = set()
        for tag_name in tag_names:
            try:
                tag = Tag(name=tag_name)
                db.session.add(tag)
                db.session.commit()
                tags.add(tag)
            except IntegrityError:
                # TODO: this rollback applies to other changes made
                # within same session if they have not been committed
                # maybe I should fix this?
                db.session.rollback()
                tags.add(cls.query.filter_by(name=tag_name).one())
        return list(tags)


posttags_table = db.Table(
    "posttags",
    db.Model.metadata,
    db.Column(
        "post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True
    ),
    db.Column(
        "tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True
    ),
)
