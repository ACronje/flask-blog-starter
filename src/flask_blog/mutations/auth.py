import graphene
from flask_graphql_auth import (
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    mutation_jwt_refresh_token_required,
)

from ..models import User


class AuthMutationSuccess(graphene.ObjectType):
    access_token = graphene.String()
    refresh_token = graphene.String()


class AuthMutationFailed(graphene.ObjectType):
    reason = graphene.Field(graphene.String, required=True)


class AuthMutationOutput(graphene.Union):
    class Meta:
        types = (
            AuthMutationSuccess,
            AuthMutationFailed,
        )


class AuthMutation(graphene.Mutation):
    class Arguments(object):
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    Output = AuthMutationOutput

    @classmethod
    def mutate(cls, _, info, username, password):
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            return AuthMutationFailed(
                reason="Username or password is incorrect"
            )

        return AuthMutationSuccess(
            access_token=create_access_token(username),
            refresh_token=create_refresh_token(username),
        )


class RefreshMutationSuccess(graphene.ObjectType):
    new_token = graphene.String()


class RefreshMutationFailed(graphene.ObjectType):
    reason = graphene.Field(graphene.String, required=True)


class RefreshMutationOutput(graphene.Union):
    class Meta:
        types = (
            AuthMutationSuccess,
            AuthMutationFailed,
        )


class RefreshMutation(graphene.Mutation):
    class Arguments(object):
        refresh_token = graphene.String(required=True)

    Output = RefreshMutationOutput

    @classmethod
    @mutation_jwt_refresh_token_required
    def mutate(self, _):
        current_user = get_jwt_identity()
        if not current_user:
            return RefreshMutationFailed(
                reason="Failed to authenticate user with token"
            )
        return RefreshMutationSuccess(
            new_token=create_access_token(identity=current_user)
        )
