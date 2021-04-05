import graphene
from graphene import relay, String
from graphene_sqlalchemy import SQLAlchemyConnectionField
from sqlalchemy.sql import func

from . import models, mutations
from .types import PostConnection, TagConnection
from .helpers import parse_date_or_none, convert_date_to_iso8601_string


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    posts = SQLAlchemyConnectionField(
        PostConnection, tag_name=String(), date=String()
    )
    tags = SQLAlchemyConnectionField(TagConnection)

    def resolve_posts(self, info, *args, tag_name=None, date=None, **kwargs):
        query = SQLAlchemyConnectionField.get_query(
            models.Post, info, *args, **kwargs
        )
        if tag_name:
            query = (
                query.join(models.posttags_table)
                .join(models.Tag)
                .filter(models.Tag.name == tag_name)
            )
        date = parse_date_or_none(date)
        if date:
            query = query.filter(
                func.date(models.Post.created_at)
                == convert_date_to_iso8601_string(date)
            )
        return query.all()

    def resolve_tags(self, info, *args, **kwargs):
        query = SQLAlchemyConnectionField.get_query(
            models.Tag, info, *args, **kwargs
        )
        return query.all()


class Mutation(graphene.ObjectType):
    auth = mutations.AuthMutation.Field()
    refresh = mutations.RefreshMutation.Field()
    create_post = mutations.CreatePost.Field()
    update_post = mutations.UpdatePost.Field()
    delete_post = mutations.DeletePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
