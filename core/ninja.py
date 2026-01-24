from ninja import NinjaAPI

from blog.ninja import router as blog_router

api = NinjaAPI()
api.add_router("/blog", blog_router, tags=["文章"])


@api.get("/hello")
def hello(request):
    return {"message": "Hello, Django Ninja!"}
