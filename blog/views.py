from django.shortcuts import get_object_or_404, redirect, render

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
    errors = {}

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        author_id = request.POST.get("author")

        if not title:
            errors["title"] = "標題不能空白"
        elif len(title) > 200:
            errors["title"] = "標題最多 200 字元"

        if not content:
            errors["content"] = "內容不能空白"

        if not errors:
            article = Article.objects.create(
                title=title,
                content=content,
                author_id=author_id if author_id else None,
            )
            return redirect("blog:article_detail", article_id=article.id)

    return render(
        request,
        "blog/article_create.html",
        {
            "authors": authors,
            "errors": errors,
            "title": request.POST.get("title", ""),
            "content": request.POST.get("content", ""),
            "author_id": request.POST.get("author", ""),
        },
    )
