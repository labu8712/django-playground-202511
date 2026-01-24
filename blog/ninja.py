from ninja import Router

from blog.models import Article

router = Router()


@router.get("/articles")
def list_articles(request):
    articles = Article.objects.all()
    return [
        {
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "is_published": article.is_published,
            "created_at": article.created_at,
        }
        for article in articles
    ]


@router.get("/articles/{article_id}")
def get_article(request, article_id: int):
    article = Article.objects.get(id=article_id)
    return {
        "id": article.id,
        "title": article.title,
        "content": article.content,
        "is_published": article.is_published,
        "created_at": article.created_at,
    }
