from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from blog.forms import ArticleForm
from blog.models import Article


def article_list(request):
    # 從 GET 參數取得篩選條件
    search = request.GET.get("search", "")
    author_id = request.GET.get("author", "")

    # 建立基本 QuerySet
    articles = Article.objects.select_related("author").prefetch_related("tags")

    # 根據搜尋關鍵字篩選標題
    if search:
        articles = articles.filter(title__icontains=search)

    # 根據作者篩選
    if author_id:
        articles = articles.filter(author_id=author_id)

    return render(
        request, "blog/article_list.html", {"articles": articles, "search": search}
    )


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
        messages.success(request, f"文章「{article.title}」已成功建立。")
        return redirect("blog:article_detail", article_id=article.id)

    return render(request, "blog/article_create.html", {"form": form})


def article_edit(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    form = ArticleForm(request.POST or None, instance=article)
    if form.is_valid():
        article = form.save()
        messages.success(request, f"文章「{article.title}」已成功更新。")
        return redirect("blog:article_detail", article_id=article.id)

    return render(request, "blog/article_edit.html", {"form": form, "article": article})


def article_delete(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == "POST":
        article.delete()
        messages.success(request, f"文章「{article.title}」已成功刪除。")
        return redirect("blog:article_list")

    return render(request, "blog/article_delete.html", {"article": article})
