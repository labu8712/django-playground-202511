from django.shortcuts import render

from blog.models import Article


def article_list(request):
    articles = Article.objects.all()
    return render(request, "blog/article_list.html", {"articles": articles})


def article_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    return render(request, "blog/article_detail.html", {"article": article})
