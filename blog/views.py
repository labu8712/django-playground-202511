from django.shortcuts import get_object_or_404, render

from blog.models import Article


def article_list(request):
    articles = Article.objects.select_related("author").prefetch_related("tags")
    return render(request, "blog/article_list.html", {"articles": articles})


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, "blog/article_detail.html", {"article": article})
