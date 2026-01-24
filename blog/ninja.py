from django.shortcuts import get_object_or_404
from ninja import Router

from blog.models import Article
from blog.schemas import ArticleIn, ArticleOut

router = Router()


@router.get("/articles", response=list[ArticleOut])
def list_articles(request):
    return Article.objects.all()


@router.get("/articles/{article_id}", response=ArticleOut)
def get_article(request, article_id: int):
    return get_object_or_404(Article, id=article_id)


@router.post("/articles", response={201: ArticleOut})
def create_article(request, payload: ArticleIn):
    article = Article.objects.create(**payload.dict())
    return 201, article
