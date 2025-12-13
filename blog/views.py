from django.shortcuts import get_object_or_404, redirect, render

from blog.forms import ArticleForm
from blog.models import Article, Author


def article_list(request):
    articles = Article.objects.select_related("author").prefetch_related("tags")
    return render(request, "blog/article_list.html", {"articles": articles})


def article_detail(request, article_id):
    article = get_object_or_404(
        Article.objects.select_related("author").prefetch_related("tags"),
        id=article_id,
    )
    return render(request, "blog/article_detail.html", {"article": article})


def article_create(request):
    authors = Author.objects.all()

    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = Article.objects.create(
                title=form.cleaned_data["title"],
                content=form.cleaned_data["content"],
                author_id=form.cleaned_data["author"],
            )
            return redirect("blog:article_detail", article_id=article.id)
    else:
        form = ArticleForm()

    return render(
        request,
        "blog/article_create.html",
        {
            "form": form,
            "authors": authors,
        },
    )
