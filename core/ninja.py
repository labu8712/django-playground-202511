from ninja import NinjaAPI
from ninja.security import HttpBearer
from rest_framework.authtoken.models import Token

from blog.ninja import router as blog_router


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            token_obj = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return None

        return token_obj.user


api = NinjaAPI(auth=AuthBearer())
api.add_router("/blog", blog_router, tags=["文章"])


@api.get("/hello")
def hello(request):
    return {"message": "Hello, Django Ninja!"}
