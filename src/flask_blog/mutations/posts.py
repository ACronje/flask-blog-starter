import graphene
from graphene import relay
from graphql_relay.node.node import from_global_id

from .. import models, types
from ..database import db


class CreatePostInput:
    title = graphene.String(required=True)
    content = graphene.String(required=True)
    tag_names = graphene.List(graphene.String, required=False)


class CreatePostSuccess(graphene.ObjectType):
    post = graphene.Field(types.PostNode, required=True)


class CreatePostOutput(graphene.Union):
    class Meta:
        types = (CreatePostSuccess,)


class CreatePost(relay.ClientIDMutation):
    Input = CreatePostInput
    Output = CreatePostOutput

    @classmethod
    def mutate_and_get_payload(cls, root, info, tag_names=None, **input):
        new_post = models.Post(**input)
        if tag_names is None:
            tag_names = []
        new_post.tags = models.Tag.find_or_add_tags_by_name(tag_names)

        db.session.add(new_post)
        db.session.commit()

        return CreatePostSuccess(post=new_post)


class UpdatePostInput:
    id = graphene.ID(required=True)
    title = graphene.String(required=True)
    content = graphene.String(required=True)
    tag_names = graphene.List(graphene.String)


class UpdatePostSuccess(graphene.ObjectType):
    post = graphene.Field(types.PostNode, required=True)


class UpdatePostFailed(graphene.ObjectType):
    reason = graphene.Field(types.String, required=True)


class UpdatePostOutput(graphene.Union):
    class Meta:
        types = (
            UpdatePostSuccess,
            UpdatePostFailed,
        )


class UpdatePost(relay.ClientIDMutation):
    Input = UpdatePostInput
    Output = UpdatePostOutput

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        id = from_global_id(input["id"])[-1]
        post = models.Post.query.get(id)
        if not post:
            return UpdatePostFailed(reason="Post not found")

        tag_names = input.get("tag_names", [])
        post.tags = models.Tag.find_or_add_tags_by_name(tag_names)
        post.title = input["title"]
        post.content = input["content"]

        db.session.commit()

        return UpdatePostSuccess(post=post)


class DeletePostInput:
    id = graphene.ID(required=True)


class DeletePostSuccess(graphene.ObjectType):
    post = graphene.Field(types.PostNode, required=True)


class DeletePostFailed(graphene.ObjectType):
    reason = graphene.Field(types.String, required=True)


class DeletePostOutput(graphene.Union):
    class Meta:
        types = (
            DeletePostSuccess,
            DeletePostFailed,
        )


class DeletePost(relay.ClientIDMutation):
    Input = DeletePostInput
    Output = DeletePostOutput

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        id = from_global_id(input["id"])[-1]
        post = models.Post.query.get(id)
        if not post:
            return DeletePostFailed(reason="Post not found")

        db.session.delete(post)
        db.session.commit()

        return DeletePostSuccess(post=post)
