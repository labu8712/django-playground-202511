from django.shortcuts import get_object_or_404, redirect, render

from blog.forms import ArticleForm
from blog.models import Article


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
    form = ArticleForm(request.POST or None)
    if form.is_valid():
        article = form.save()
        return redirect("blog:article_detail", article_id=article.id)

    return render(request, "blog/article_create.html", {"form": form})


def article_edit(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    form = ArticleForm(request.POST or None, instance=article)
    if form.is_valid():
        article = form.save()
        return redirect("blog:article_detail", article_id=article.id)

    return render(request, "blog/article_edit.html", {"form": form, "article": article})


def article_delete(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == "POST":
        article.delete()
        return redirect("blog:article_list")

    return render(request, "blog/article_delete.html", {"article": article})
