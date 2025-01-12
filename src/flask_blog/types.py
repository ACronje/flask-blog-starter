from graphene import relay, List, String
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType

from . import models


def connection_field_factory(relationship, registry):
    model = relationship.mapper.entity
    model_type = registry.get_type_for_model(model)
    return SQLAlchemyConnectionField(model_type)


class PostNode(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node,)
        model = models.Post
        connection_field_factory = connection_field_factory

    tag_names = List(String)

    def resolve_tag_names(post, info):
        return post.tag_names


class TagNode(SQLAlchemyObjectType):
    class Meta:
        interfaces = (relay.Node,)
        model = models.Tag
        connection_field_factory = connection_field_factory


class PostConnection(relay.Connection):
    class Meta:
        node = PostNode


class TagConnection(relay.Connection):
    class Meta:
        node = TagNode
