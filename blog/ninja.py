from django.shortcuts import get_object_or_404
from ninja import Router

from blog.models import Article
from blog.schemas import ArticleOut

router = Router()


@router.get("/articles", response=list[ArticleOut])
def list_articles(request):
    return Article.objects.all()


@router.get("/articles/{article_id}", response=ArticleOut)
def get_article(request, article_id: int):
    return get_object_or_404(Article, id=article_id)
