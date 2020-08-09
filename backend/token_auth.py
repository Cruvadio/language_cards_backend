
# https://channels.readthedocs.io/en/latest/topics/authentication.html#custom-authentication
from urllib import parse

from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import User, AnonymousUser
from django.db import close_old_connections
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.tokens import AccessToken

from channels.db import database_sync_to_async

@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

@database_sync_to_async
def close_connections():
    close_old_connections()


class JWTAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):
        return JWTAuthMiddlewareInstance(scope, self)



class JWTAuthMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        query_string = self.scope["query_string"].decode()
        query_dict = dict(parse.parse_qsl(query_string))
        raw_token = query_dict.get("token")
        if raw_token:
            token = AccessToken(token=raw_token, verify=True)
            token_user = TokenUser(token)
            print(token_user)

            self.scope["user"] = await get_user(token_user.id)
        else:
            self.scope['user'] = AnonymousUser()
        inner = self.inner(self.scope)
        return await inner(receive, send)


JWTAuthMiddlewareStack = lambda inner: JWTAuthMiddleware(AuthMiddlewareStack(inner))