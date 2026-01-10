from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView

from blog.filters import ArticleFilter
from blog.forms import ArticleForm
from blog.models import Article


def article_list(request):
    filter_ = ArticleFilter(
        request.GET or None,
        queryset=Article.objects.select_related("author").prefetch_related("tags"),
    )
    return render(request, "blog/article_list.html", {"filter": filter_})


class ArticleDetailView(DetailView):
    model = Article
    pk_url_kwarg = "article_id"


@permission_required("blog.add_article", raise_exception=True)
def article_create(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.created_by = request.user
        article.save()
        messages.success(request, f"文章「{article.title}」已成功建立。")
        return redirect("blog:article_detail", article_id=article.id)

    return render(request, "blog/article_create.html", {"form": form})


@permission_required("blog.change_article", raise_exception=True)
def article_edit(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    if form.is_valid():
        article = form.save()
        messages.success(request, f"文章「{article.title}」已成功更新。")
        return redirect("blog:article_detail", article_id=article.id)

    return render(request, "blog/article_edit.html", {"form": form, "article": article})


@permission_required("blog.delete_article", raise_exception=True)
def article_delete(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == "POST":
        article.delete()
        messages.success(request, f"文章「{article.title}」已成功刪除。")
        return redirect("blog:article_list")

    return render(request, "blog/article_delete.html", {"article": article})


@permission_required("blog.delete_article", raise_exception=True)
def article_bulk_delete(request):
    if request.method == "POST":
        article_ids = request.POST.getlist("article_ids")
        if article_ids:
            deleted_count, _ = Article.objects.filter(id__in=article_ids).delete()
            messages.success(request, f"已成功刪除 {deleted_count} 篇文章")
        else:
            messages.warning(request, "請先選取至少一個要刪除的文章")

    return redirect("blog:article_list")
