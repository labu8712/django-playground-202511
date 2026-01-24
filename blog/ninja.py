from django.shortcuts import get_object_or_404
from ninja import PatchDict, Router

from blog.models import Article
from blog.schemas import ArticleIn, ArticleOut

router = Router()


@router.get("/articles", response=list[ArticleOut], auth=None)
def list_articles(request):
    return Article.objects.all()


@router.get("/articles/{article_id}", response=ArticleOut, auth=None)
def get_article(request, article_id: int):
    return get_object_or_404(Article, id=article_id)


@router.post("/articles", response={201: ArticleOut})
def create_article(request, payload: ArticleIn):
    article = Article.objects.create(**payload.dict())
    return 201, article


@router.put("/articles/{article_id}", response=ArticleOut)
def update_article(request, article_id: int, payload: ArticleIn):
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
    article = get_object_or_404(Article, id=article_id)
    for attr, value in payload.items():
        setattr(article, attr, value)

    article.save()
    return article


@router.delete("/articles/{article_id}", response={204: None})
def delete_article(request, article_id: int):
    article = get_object_or_404(Article, id=article_id)
    article.delete()
    return 204, None
