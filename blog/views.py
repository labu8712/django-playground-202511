from django.shortcuts import render

from blog.models import Article


def article_list(request):
    articles = Article.objects.all()
    return render(request, "blog/article_list.html", {"articles": articles})
