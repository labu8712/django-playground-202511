from typing import Literal

from django.shortcuts import get_object_or_404
from ninja import PatchDict, Query, Router
from ninja.errors import HttpError

from blog.models import Article
from blog.schemas import ArticleFilterSchema, ArticleIn, ArticleOut

router = Router()


@router.get("/articles", response=list[ArticleOut], auth=None)
def list_articles(
    request,
    filters: Query[ArticleFilterSchema],
    ordering: Literal["created_at", "-created_at", "title", "-title"] | None = None,
):
    articles = filters.filter(Article.objects.all())
    if ordering:
        articles = articles.order_by(ordering)

    return articles


@router.get(
    "/articles/{article_id}",
    response=ArticleOut,
    auth=None,
    openapi_extra={
        "responses": {
            404: {
                "description": "文章不存在",
            }
        }
    },
)
def get_article(request, article_id: int):
    return get_object_or_404(Article, id=article_id)


@router.post("/articles", response={201: ArticleOut})
def create_article(request, payload: ArticleIn):
    if not request.auth.has_perm("blog.add_article"):
        raise HttpError(403, "你沒有權限新增文章")

    article = Article.objects.create(
        **payload.dict(),
        created_by=request.auth,
    )
    return 201, article


@router.put("/articles/{article_id}", response=ArticleOut)
def update_article(request, article_id: int, payload: ArticleIn):
    if not request.auth.has_perm("blog.change_article"):
        raise HttpError(403, "你沒有權限編輯文章")

    article = get_object_or_404(Article, id=article_id)
    for attr, value in payload.dict().items():
        setattr(article, attr, value)

    article.save()
    return article


@router.patch("/articles/{article_id}", response=ArticleOut)
def partial_update_article(
    request,
    article_id: int,
    payload: PatchDict[ArticleIn],
):
    if not request.auth.has_perm("blog.change_article"):
        raise HttpError(403, "你沒有權限編輯文章")

    article = get_object_or_404(Article, id=article_id)
    for attr, value in payload.items():
        setattr(article, attr, value)

    article.save()
    return article


@router.delete("/articles/{article_id}", response={204: None})
def delete_article(request, article_id: int):
    if not request.auth.has_perm("blog.delete_article"):
        raise HttpError(403, "你沒有權限刪除文章")

    article = get_object_or_404(Article, id=article_id)
    article.delete()
    return 204, None
